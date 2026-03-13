#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Pipeline annotation v4 — gpt-4o-mini — Version robuste + parallèle
Repart TOUJOURS des données source brutes.
Charge les annotations existantes pour ne pas refaire ce qui a déjà marché.
Checkpoint toutes les 100 annotations.
Utilise ThreadPoolExecutor pour 8-10 requêtes concurrentes (~70-100 RPM).
"""

import hashlib
import json
import os
import sys
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import pandas as pd
from tqdm import tqdm

sys.path.insert(0, str(Path(__file__).resolve().parent))
from src.annotation.annotation_v4 import (
    BATCHES, BRIEFINGS, PERIOD_VARS, SYSTEM_PROMPT,
    check_coherence, format_user_message, parse_json_response,
)

# ── Configuration ────────────────────────────────────────────────────────────

MODEL = "gpt-4o-mini"
MAX_TOKENS = 1200
SLEEP_BETWEEN = 0.15        # petit sleep entre lancements de threads
SLEEP_ON_429 = 65           # secondes d'attente sur rate-limit
MAX_RETRIES = 3
CHECKPOINT_EVERY = 100      # sauvegarder toutes les N annotations
N_WORKERS = 5               # threads parallèles — 5×60/0.8s ≈ 375 RPM < limite 500 RPM

BLOCS = {
    "Gauche radicale": ["LFI-NFP", "LFI", "GDR"],
    "Gauche moderee":  ["SOC", "PS-NFP", "ECO", "ECO-NFP"],
    "Centre / Majorite": ["REN", "MODEM", "HOR", "EPR", "DEM"],
    "Droite":          ["LR", "RN", "UDR", "NI"],
}
GROUP_TO_BLOC = {g: b for b, gs in BLOCS.items() for g in gs}

# ── Helpers ──────────────────────────────────────────────────────────────────

def text_hash(text: str) -> str:
    """Fingerprint d'un texte pour dé-duplication."""
    return hashlib.md5(str(text)[:500].encode("utf-8", errors="replace")).hexdigest()


def load_source_data(data_dir: Path) -> pd.DataFrame:
    """Charge tweets + interventions, filtre, normalise."""
    tw = pd.read_parquet(data_dir / "tweets_v3_full_clean.parquet")
    iv = pd.read_parquet(data_dir / "interventions_v3_full_clean.parquet")

    tw["author"]     = tw["depute_name"].fillna(tw.get("username", ""))
    tw["group"]      = tw["groupe_politique"].fillna("UNKNOWN")
    tw["bloc"]       = tw["group"].map(GROUP_TO_BLOC).fillna("UNKNOWN")
    tw["date"]       = pd.to_datetime(tw["date_parsed"], errors="coerce")
    tw["text_clean"] = tw["text"]
    tw["arena"]      = "Twitter"

    iv["author"]     = iv.get("speaker_name", iv.get("matched_name", iv.get("AUTEUR", "")))
    iv["group"]      = iv["GROUPE"].fillna(iv.get("matched_group", "UNKNOWN"))
    iv["bloc"]       = iv["group"].map(GROUP_TO_BLOC).fillna("UNKNOWN")
    iv["date"]       = pd.to_datetime(iv["sitting_date"], errors="coerce")
    iv["text_clean"] = iv["cleaned_text"].fillna(iv.get("TEXTE", ""))
    iv["arena"]      = "AN"

    shared = ["author", "group", "bloc", "date", "text_clean",
              "stance_v3", "confidence_v3", "primary_frame_v3",
              "primary_target_v3", "is_off_topic_v3", "arena", "retweets", "likes"]
    for c in shared:
        if c not in tw.columns: tw[c] = 0 if c in ["retweets", "likes"] else None
        if c not in iv.columns: iv[c] = 0 if c in ["retweets", "likes"] else None

    tw_f = tw[
        (~tw["is_off_topic_v3"].fillna(False)) &
        (tw["confidence_v3"] >= 0.70) &
        (tw["bloc"] != "UNKNOWN") &
        tw["date"].notna()
    ]
    iv_f = iv[
        (~iv["is_off_topic_v3"].fillna(False)) &
        (iv["confidence_v3"] >= 0.70) &
        (iv["bloc"] != "UNKNOWN") &
        iv["date"].notna()
    ]

    df = pd.concat([tw_f[shared], iv_f[shared]], ignore_index=True)
    df_post = df[df["date"] >= pd.Timestamp("2023-10-07")].copy()
    df_post["text_hash"] = df_post["text_clean"].apply(text_hash)
    return df_post


def load_existing_successes(parquet_path: Path) -> dict:
    """
    Retourne un dict {text_hash -> annotation_dict} pour les textes
    déjà annotés avec succès dans le parquet existant.
    """
    if not parquet_path.exists():
        return {}
    df = pd.read_parquet(parquet_path)
    # Vérifie si text_clean est présent
    if "text_clean" not in df.columns:
        return {}
    ann_cols = ["stance_v4", "ceasefire_call", "ceasefire_type",
                "target_primary", "frame_primary", "conditionality",
                "emotional_register", "key_demands", "reasoning_v4"]
    # Une annotation est un succès si stance_v4 est défini et pas NaN
    if "stance_v4" not in df.columns:
        return {}
    success_mask = df["stance_v4"].notna()
    successes = {}
    for _, row in df[success_mask].iterrows():
        h = text_hash(str(row.get("text_clean", "")))
        row_dict = row.to_dict()
        successes[h] = row_dict
    return successes


# ── Annotation single ────────────────────────────────────────────────────────

def annotate_one(client, row: pd.Series, batch_name: str) -> dict:
    """
    Annote un texte avec gpt-4o-mini.
    Retourne {"success": bool, "annotation": dict|None, "error": str|None}
    """
    user_msg = format_user_message(row, batch_name)
    last_err = ""

    for attempt in range(MAX_RETRIES):
        try:
            resp = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user",   "content": user_msg},
                ],
                response_format={"type": "json_object"},
                max_tokens=MAX_TOKENS,
            )
            choice = resp.choices[0]
            finish_reason = choice.finish_reason
            content = choice.message.content

            # Contenu filtré par la sécurité OpenAI
            if finish_reason == "content_filter":
                return {"success": False, "error": "content_filter", "annotation": None}

            # Refus explicite
            if not content and getattr(choice.message, "refusal", None):
                return {"success": False, "error": f"refusal: {choice.message.refusal}", "annotation": None}

            # Contenu vide — réessayer
            if not content:
                last_err = "empty_content"
                time.sleep(1.5)
                continue

            ann = parse_json_response(content)
            if not ann or not isinstance(ann, dict):
                last_err = f"parse_fail: {content[:200]}"
                # Réessayer si c'est potentiellement un JSON tronqué
                if attempt < MAX_RETRIES - 1:
                    time.sleep(1.0)
                    continue
                return {"success": False, "error": last_err, "annotation": None}

            # Normaliser stance_v4 (peut être float, string…)
            stance = ann.get("stance_v4", ann.get("stance"))
            if isinstance(stance, float):
                stance = int(stance)
            if isinstance(stance, str):
                try:
                    stance = int(float(stance))
                except ValueError:
                    pass
            ann["stance_v4"] = stance

            if stance not in (-2, -1, 0, 1, 2):
                last_err = f"invalid_stance: {stance}"
                if attempt < MAX_RETRIES - 1:
                    continue
                return {"success": False, "error": last_err, "annotation": None}

            # Compléter les champs manquants
            defaults = {
                "ceasefire_call": False,
                "ceasefire_type": None,
                "target_primary": "OTHER",
                "target_secondary": None,
                "frame_primary": "DIP",
                "conditionality": "balanced",
                "emotional_register": "neutral",
                "key_demands": [],
            }
            for k, v in defaults.items():
                if k not in ann:
                    ann[k] = v
            # Normaliser "none" → None et listes → string
            if ann.get("ceasefire_type") == "none":
                ann["ceasefire_type"] = None
            ts = ann.get("target_secondary")
            if isinstance(ts, list):
                ann["target_secondary"] = ts[0] if ts else None
            elif ts == "":
                ann["target_secondary"] = None
            # key_demands doit toujours être une liste
            kd = ann.get("key_demands", [])
            if not isinstance(kd, list):
                ann["key_demands"] = [kd] if kd else []

            ann["flags"] = check_coherence(ann)
            return {"success": True, "annotation": ann, "error": None}

        except Exception as e:
            err_str = str(e)
            last_err = err_str[:200]
            if "429" in err_str or "rate_limit" in err_str.lower():
                wait = SLEEP_ON_429 * (attempt + 1)
                print(f"\n  [429] Rate limit — attente {wait}s...", flush=True)
                time.sleep(wait)
            elif "503" in err_str or "500" in err_str or "timeout" in err_str.lower():
                time.sleep(5 * (attempt + 1))
            else:
                time.sleep(2 ** attempt)

    return {"success": False, "error": last_err, "annotation": None}


# ── Batch principal ──────────────────────────────────────────────────────────

def run_batch(batch_name: str, source_df: pd.DataFrame,
              output_dir: Path, client, dry_run: bool = False) -> None:
    """Lance l'annotation d'un batch complet."""
    from openai import OpenAI  # import local pour avoir client disponible

    config   = BATCHES[batch_name]
    start    = pd.Timestamp(config["start"])
    end      = pd.Timestamp(config["end"])
    batch_df = source_df[
        (source_df["date"] >= start) & (source_df["date"] <= end)
    ].copy().reset_index(drop=True)

    if len(batch_df) == 0:
        print(f"  Batch {batch_name}: aucun texte dans la fenêtre.")
        return

    out_path = output_dir / f"annotations_v4_{batch_name}.parquet"
    log_path = output_dir / f"annotation_v4_{batch_name}_log2.jsonl"
    fail_path = output_dir / f"annotation_v4_{batch_name}_failures2.jsonl"

    # Charger les annotations déjà réussies (pour ne pas refaire le travail)
    existing_successes = load_existing_successes(out_path)
    print(f"  Batch {batch_name}: {len(batch_df):,} textes dans la fenêtre, "
          f"{len(existing_successes):,} déjà annotés.")

    # Identifier les textes à annoter
    to_annotate = []
    already_done = []
    for idx, row in batch_df.iterrows():
        h = row["text_hash"]
        if h in existing_successes:
            already_done.append((idx, existing_successes[h]))
        else:
            to_annotate.append((idx, row))

    print(f"  -> {len(to_annotate):,} textes restants a annoter.")
    if dry_run:
        return

    if len(to_annotate) == 0:
        print(f"  Batch {batch_name}: tout est déjà annoté !")
        return

    # Annoter les textes manquants — ThreadPoolExecutor pour parallélisme
    new_results = []
    lock = threading.Lock()
    n_ok, n_fail = 0, 0
    progress = tqdm(total=len(to_annotate), desc=f"Batch {batch_name}")

    def _annotate_task(args):
        idx, row = args
        return idx, row, annotate_one(client, row, batch_name)

    with ThreadPoolExecutor(max_workers=N_WORKERS) as executor:
        futures = {executor.submit(_annotate_task, (idx, row)): idx
                   for idx, row in to_annotate}

        done_count = 0
        for future in as_completed(futures):
            idx, row, res = future.result()
            row_dict = row.to_dict()

            with lock:
                if res["success"] and res["annotation"]:
                    ann = res["annotation"]
                    for k, v in ann.items():
                        if k != "flags":
                            row_dict[k] = v
                    row_dict["reasoning_v4"] = ann.get("reasoning", "")
                    row_dict["flags"]        = ann.get("flags", [])
                    n_ok += 1
                    with open(log_path, "a", encoding="utf-8") as f:
                        entry = {"idx": int(idx), "stance_v4": ann.get("stance_v4"), "batch": batch_name}
                        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
                else:
                    row_dict["annotation_failed"] = True
                    row_dict["flags"]             = [res.get("error", "unknown")]
                    n_fail += 1
                    with open(fail_path, "a", encoding="utf-8") as f:
                        entry = {"idx": int(idx), "error": res.get("error", "unknown")}
                        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

                new_results.append((idx, row_dict))
                done_count += 1
                progress.update(1)

                # Checkpoint
                if done_count % CHECKPOINT_EVERY == 0:
                    _save_checkpoint(batch_df, already_done, new_results, out_path)
                    progress.write(f"  [checkpoint {done_count}/{len(to_annotate)}] OK:{n_ok} Fail:{n_fail}")

    progress.close()

    # Sauvegarde finale
    _save_checkpoint(batch_df, already_done, new_results, out_path)
    pct = 100 * n_ok / max(1, len(to_annotate))
    print(f"  Batch {batch_name} terminé : {n_ok}/{len(to_annotate)} OK ({pct:.1f}%), "
          f"{n_fail} échecs.")


def _normalize_df_for_parquet(df: pd.DataFrame) -> pd.DataFrame:
    """Normalise les types pour éviter les erreurs pyarrow (listes/strings mélangés)."""
    for col in ["target_secondary", "ceasefire_type"]:
        if col in df.columns:
            df[col] = df[col].apply(
                lambda x: x[0] if isinstance(x, list) and x
                else (None if isinstance(x, list) else x)
            )
    for col in ["key_demands", "flags"]:
        if col in df.columns:
            df[col] = df[col].apply(
                lambda x: x if isinstance(x, list)
                else ([] if x is None or (isinstance(x, float) and pd.isna(x)) else [str(x)])
            )
    return df


def _save_checkpoint(batch_df: pd.DataFrame, already_done: list,
                     new_results: list, out_path: Path) -> None:
    """Fusionne les annotations existantes + nouvelles et sauvegarde."""
    rows = []
    for idx, ann_dict in already_done:
        rows.append(ann_dict)
    for idx, row_dict in new_results:
        rows.append(row_dict)
    if rows:
        df = pd.DataFrame(rows)
        df = _normalize_df_for_parquet(df)
        df.to_parquet(out_path, index=False)


# ── Entry point ──────────────────────────────────────────────────────────────

def main():
    import argparse
    from openai import OpenAI

    parser = argparse.ArgumentParser(description="Annotation v4 avec gpt-4o-mini (version robuste)")
    parser.add_argument("--batch", choices=list(BATCHES.keys()) + ["all"], default="all")
    parser.add_argument("--dry-run", action="store_true", help="Affiche les effectifs sans annoter")
    parser.add_argument("--data-dir",   default="data/annotated/predictions")
    parser.add_argument("--output-dir", default="outputs")
    args = parser.parse_args()

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("ERREUR: OPENAI_API_KEY non défini.")
        sys.exit(1)

    data_dir   = Path(args.data_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    if not (data_dir / "tweets_v3_full_clean.parquet").exists():
        print(f"ERREUR: données source introuvables dans {data_dir}")
        sys.exit(1)

    print(f"Chargement des données source depuis {data_dir}...")
    source_df = load_source_data(data_dir)
    print(f"Corpus post-7 oct: {len(source_df):,} textes")

    client = OpenAI(api_key=api_key)

    batches_to_run = list(BATCHES.keys()) if args.batch == "all" else [args.batch]

    for batch_name in batches_to_run:
        print(f"\n{'='*60}")
        print(f"BATCH: {batch_name}")
        run_batch(batch_name, source_df, output_dir, client, dry_run=args.dry_run)

    print("\n\nTOUT TERMINÉ.")
    # Résumé final
    print("\n=== RÉSUMÉ ===")
    for batch_name in batches_to_run:
        p = output_dir / f"annotations_v4_{batch_name}.parquet"
        if p.exists():
            df = pd.read_parquet(p)
            ok = df["stance_v4"].notna().sum() if "stance_v4" in df.columns else 0
            print(f"  {batch_name}: {ok}/{len(df)} annotés avec succès")


if __name__ == "__main__":
    main()
