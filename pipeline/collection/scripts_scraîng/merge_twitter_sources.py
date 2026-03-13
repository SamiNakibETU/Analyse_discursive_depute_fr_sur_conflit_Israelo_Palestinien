#!/usr/bin/env python3
"""
Fusionne les différentes sources de comptes Twitter des députés.

Sources:
1. twitter_account_deputés_2023_2024.txt (législature 16)
2. députés_twitter accout_2024-now.txt (législature 17)
3. API nosdeputes.fr (backup)
4. Liste des députés des interventions AN
"""

import json
import re
import unicodedata
from pathlib import Path
from collections import defaultdict


def normalize_name(name: str) -> str:
    """Normalise un nom pour le matching."""
    # Supprimer les titres
    name = re.sub(r"^(M\.|Mme|M |Mme )", "", name, flags=re.IGNORECASE).strip()
    # Normaliser les accents
    name = unicodedata.normalize("NFD", name)
    name = "".join(c for c in name if not unicodedata.combining(c))
    return name.lower().strip()


def extract_twitter_handle(url: str) -> str | None:
    """Extrait le handle Twitter d'une URL."""
    if not url or url.strip() == "":
        return None
    
    url = url.strip()
    
    # Patterns courants
    patterns = [
        r"twitter\.com/@?([a-zA-Z0-9_]+)",
        r"x\.com/@?([a-zA-Z0-9_]+)",
        r"@([a-zA-Z0-9_]+)",
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url, re.IGNORECASE)
        if match:
            handle = match.group(1).strip("/").lower()
            # Ignorer les handles invalides
            if handle and handle not in ["twitter", "x", "com"]:
                return handle
    
    return None


def parse_csv_file(filepath: Path) -> dict:
    """Parse un fichier CSV de députés -> Twitter."""
    mapping = {}
    
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    # Skip header
    for line in lines[1:]:
        line = line.strip()
        if not line:
            continue
        
        parts = line.split(",")
        if len(parts) < 3:
            continue
        
        name = parts[0].strip()
        twitter_url = parts[2].strip() if len(parts) > 2 else ""
        
        handle = extract_twitter_handle(twitter_url)
        if handle:
            normalized = normalize_name(name)
            mapping[normalized] = {
                "name": name,
                "twitter": handle
            }
    
    return mapping


def load_interventions_deputes(filepath: Path) -> list:
    """Charge les députés depuis les interventions enrichies."""
    deputes = defaultdict(lambda: {"name": "", "group": "", "count": 0})
    
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            data = json.loads(line)
            name = data.get("matched_name") or data.get("speaker_name", "")
            if not name or name.lower() in ["", "n/a", "présidence de séance"]:
                continue
            
            normalized = normalize_name(name)
            deputes[normalized]["name"] = name
            deputes[normalized]["group"] = data.get("matched_group", "")
            deputes[normalized]["count"] += 1
    
    return dict(deputes)


def load_corrections(filepath: Path) -> dict:
    """Charge les corrections manuelles."""
    if not filepath.exists():
        return {}
    
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    return data.get("corrections", {})


def main():
    print("=" * 60)
    print("FUSION DES SOURCES TWITTER")
    print("=" * 60)
    
    # Workspace root (4 levels up from pipeline/collection/scripts_scraîng/)
    base_path = Path(__file__).resolve().parent.parent.parent.parent

    # 1. Charger les sources externes
    print("\n[1] Chargement des fichiers sources...")
    
    twitter_sources = base_path / "config" / "twitter_sources"
    file_2023_2024 = twitter_sources / "twitter_account_deputés_2023_2024.txt"
    file_2024_now = twitter_sources / "députés_twitter accout_2024-now.txt"
    
    twitter_2023 = {}
    twitter_2024 = {}
    
    if file_2023_2024.exists():
        twitter_2023 = parse_csv_file(file_2023_2024)
        print(f"    2023-2024: {len(twitter_2023)} comptes trouvés")
    else:
        print(f"    [!] Fichier non trouvé: {file_2023_2024}")
    
    if file_2024_now.exists():
        twitter_2024 = parse_csv_file(file_2024_now)
        print(f"    2024-now: {len(twitter_2024)} comptes trouvés")
    else:
        print(f"    [!] Fichier non trouvé: {file_2024_now}")
    
    # 2. Fusionner (2024 a priorité car plus récent)
    print("\n[2] Fusion des sources...")
    all_twitter = {**twitter_2023, **twitter_2024}  # 2024 écrase 2023
    print(f"    Total unique: {len(all_twitter)} comptes")
    
    # 3. Charger les députés des interventions
    print("\n[3] Chargement des députés des interventions AN...")
    interv_path = base_path / "pipeline" / "collection" / "data" / "processed" / "interventions_gaza_filtered.jsonl"

    if not interv_path.exists():
        interv_path = base_path / "pipeline" / "collection" / "data" / "processed" / "interventions_enriched.jsonl"
    
    deputes = load_interventions_deputes(interv_path)
    print(f"    {len(deputes)} députés uniques dans les interventions")
    
    # 4. Charger les corrections manuelles
    print("\n[4] Chargement des corrections manuelles...")
    corrections_path = base_path / "pipeline" / "collection" / "config" / "twitter_corrections.json"
    corrections = load_corrections(corrections_path)
    print(f"    {len(corrections)} corrections chargées")
    
    # 5. Matcher
    print("\n[5] Matching députés <-> Twitter...")
    results = []
    matched = 0
    unmatched = []
    
    for normalized, dep_info in deputes.items():
        twitter_handle = None
        source = "not_found"
        
        # 1. D'abord vérifier les corrections manuelles
        if normalized in corrections:
            if corrections[normalized]:  # Si pas null
                twitter_handle = corrections[normalized].lower()
                source = "manual_correction"
            else:
                # Explicitement pas de Twitter
                source = "no_twitter_confirmed"
        
        # 2. Sinon chercher correspondance exacte dans les CSV
        elif normalized in all_twitter:
            twitter_handle = all_twitter[normalized]["twitter"]
            source = "csv_exact"
        
        # 3. NE PAS faire de matching partiel par nom de famille (trop d'erreurs)
        
        result = {
            "depute_name": dep_info["name"],
            "normalized_name": normalized,
            "group": dep_info["group"],
            "intervention_count": dep_info["count"],
            "twitter_handle": twitter_handle,
            "twitter_source": source
        }
        
        if twitter_handle:
            matched += 1
        elif source != "no_twitter_confirmed":
            unmatched.append(dep_info["name"])
        
        results.append(result)
    
    # Trier par nombre d'interventions
    results.sort(key=lambda x: x["intervention_count"], reverse=True)
    
    print(f"\n    Matched: {matched}/{len(deputes)}")
    print(f"    Non matched: {len(unmatched)}")
    
    # 6. Afficher les non-matchés importants (>5 interventions)
    print("\n[6] Députés sans Twitter (>5 interventions):")
    for r in results:
        if not r["twitter_handle"] and r["intervention_count"] > 5:
            print(f"    - {r['depute_name']} ({r['group']}) - {r['intervention_count']} interv")
    
    # 7. Sauvegarder
    output_path = base_path / "pipeline" / "collection" / "data" / "interim" / "deputes_twitter_merged.json"
    output = {
        "generated_at": __import__("datetime").datetime.now().isoformat(),
        "sources": [
            str(file_2023_2024),
            str(file_2024_now)
        ],
        "total_deputes": len(results),
        "with_twitter": matched,
        "without_twitter": len(unmatched),
        "deputes": results
    }
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"\n[7] Sauvegardé: {output_path}")
    
    # 8. Stats
    print("\n" + "=" * 60)
    print("RÉSUMÉ")
    print("=" * 60)
    print(f"Total députés: {len(results)}")
    print(f"Avec Twitter: {matched} ({matched * 100 // len(results)}%)")
    print(f"Sans Twitter: {len(unmatched)}")
    
    print("\nTop 15 députés (par interventions):")
    for i, dep in enumerate(results[:15], 1):
        tw = f"@{dep['twitter_handle']}" if dep['twitter_handle'] else "???"
        print(f"  {i:2}. {dep['depute_name'][:25]:<25} ({dep['group']:<10}) - {dep['intervention_count']:3} interv - {tw}")
    
    return output_path


if __name__ == "__main__":
    main()

