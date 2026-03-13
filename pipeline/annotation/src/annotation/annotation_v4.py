# -*- coding: utf-8 -*-
"""
Pipeline d'annotation v4 — Ré-annotation par période pivot
Modèle : gpt-5-nano / gpt-4o-mini (json_object pour compatibilité maximale)
"""

import json
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd
from openai import OpenAI
from tqdm import tqdm

# =============================================================================
# CONFIGURATION
# =============================================================================

BLOCS = {
    "Gauche radicale": ["LFI-NFP", "LFI", "GDR"],
    "Gauche moderee": ["SOC", "PS-NFP", "ECO", "ECO-NFP"],
    "Centre / Majorite": ["REN", "MODEM", "HOR", "EPR", "DEM"],
    "Droite": ["LR", "RN", "UDR", "NI"],
}
GROUP_TO_BLOC = {g: b for b, gs in BLOCS.items() for g in gs}

BATCHES = {
    "CHOC": {"start": "2023-10-07", "end": "2023-11-15", "period_vars": "CHOC"},
    "POST_CIJ": {"start": "2024-01-26", "end": "2024-02-15", "period_vars": "POST_CIJ"},
    "RAFAH": {"start": "2024-05-01", "end": "2024-06-15", "period_vars": "RAFAH"},
    "POST_SINWAR": {"start": "2024-10-15", "end": "2024-10-31", "period_vars": "POST_SINWAR"},
    "MANDATS_CPI": {"start": "2024-11-21", "end": "2024-12-31", "period_vars": "MANDATS_CPI"},
    "CEASEFIRE_BREACH": {"start": "2025-01-01", "end": "2025-03-31", "period_vars": "CEASEFIRE_BREACH"},
    "NEW_OFFENSIVE": {"start": "2025-04-01", "end": "2025-06-30", "period_vars": "NEW_OFFENSIVE"},
}

PERIOD_VARS = {
    "CHOC": {
        "condemns_hamas_attack": "bool",
        "self_defense_mention": "bool",
        "proportionality_issue": "bool",
        "displacement_mention": "bool",
    },
    "POST_CIJ": {
        "icj_reference": "bool",
        "genocide_framing": "string — 'uses_term', 'rejects_term', 'quotes_icj', 'absent'",
        "icc_mention": "bool",
    },
    "RAFAH": {
        "rafah_reaction": "string | null — 'condemns_offensive', 'supports_operation', 'calls_restraint', 'absent'",
        "icc_mention": "bool",
        "genocide_framing": "string — 'uses_term', 'rejects_term', 'quotes_icj', 'absent'",
    },
    "POST_SINWAR": {
        "sinwar_reaction": "string | null — 'celebrates_elimination', 'irrelevant_for_peace', 'criticizes_assassination', 'absent'",
        "famine_mention": "bool",
        "ethnic_cleansing_frame": "bool",
    },
    "MANDATS_CPI": {
        "icc_warrants_position": "string — 'support_enforcement', 'oppose_warrants', 'acknowledge_without_position', 'absent'",
        "genocide_framing": "string — 'uses_term', 'rejects_term', 'quotes_icj', 'absent'",
    },
    "CEASEFIRE_BREACH": {
        "ceasefire_breach_blame": "string | null — 'blames_israel', 'blames_hamas', 'blames_both', 'absent'",
        "reconstruction_mention": "bool",
        "two_state_mention": "bool",
    },
    "NEW_OFFENSIVE": {
        "conquest_framing": "bool — le texte mentionne-t-il 'conquête' ou annexion de Gaza ?",
        "state_recognition_mention": "bool",
        "transpartisan_convergence": "bool — le texte reflète-t-il une position partagée au-delà du clivage habituel ?",
    },
}

BRIEFINGS = {
    "CHOC": """CONTEXTE : Le 7 octobre 2023, le Hamas lance une attaque sans précédent contre Israël, tuant environ 1 200 personnes et prenant 251 otages. Israël déclare la guerre et impose un blocus total sur Gaza (eau, électricité, nourriture, fuel). Le 13 octobre, l'armée ordonne l'évacuation de 1,1 million de personnes du nord de Gaza. Le 17 octobre, une explosion à l'hôpital Al-Ahli fait entre 100 et 300 morts — l'attribution reste disputée. Le 27 octobre, l'AG de l'ONU adopte une résolution appelant à une « trêve humanitaire immédiate ». Le même jour, Israël lance l'offensive terrestre. Le 15 novembre, l'armée assiège l'hôpital Al-Shifa.
En France, la Gauche (LFI, Verts, PCF) appelle rapidement au cessez-le-feu. Le gouvernement Macron condamne le Hamas et appelle au « respect du droit international humanitaire ». La Droite (LR, RN) reste fermement pro-Israël.
ATTENTION : (1) Distingue les textes du 7-10 oct. (consensus) des textes du 15 oct.+ (polarisation). (2) « Cessez-le-feu » est un marqueur fort. (3) « Droit de se défendre » est quasi-universel au début mais disparaît chez la Gauche.""",
    "POST_CIJ": """CONTEXTE : Le 26 janvier 2024, la CIJ rend une ordonnance dans l'affaire Afrique du Sud c. Israël, ordonnant des mesures pour prévenir le génocide à Gaza. Le terme « génocide » entre dans le débat politique français comme concept juridique. Le 29 février, au moins 120 personnes sont tuées dans une file d'aide à Gaza (« massacre de la farine »).
ATTENTION : (1) La CIJ est la rupture clé — note si le député mentionne la CIJ, le « génocide » (registre : juridique, accusatoire, rejeté). (2) Le shift vers le frame juridique (LEG) est le signal principal. (3) Des députés du Centre peuvent dire « droit international » sans dire « génocide » — c'est significatif.""",
    "RAFAH": """CONTEXTE : Mai 2024, Israël lance une offensive sur Rafah malgré les avertissements internationaux. 1M+ de déplacés doivent fuir à nouveau. Le 20 mai, le procureur de la CPI demande des mandats d'arrêt contre Netanyahu et Gallant + leaders Hamas. Le 28 mai, un bombardement sur un camp de déplacés à Rafah tue 45 personnes brûlées vives. À l'AN, Chatelain (Écolo) dénonce une « guerre d'extermination ». Attal appelle au cessez-le-feu + libération des otages.
ATTENTION : (1) Test de convergence : des députés Centre/Majorité adoptent-ils « cessez-le-feu » ? (2) La CPI crée un nouveau clivage. (3) L'indignation après Barkasat est-elle transpartisane ?""",
    "POST_SINWAR": """CONTEXTE : Le 16 octobre 2024, Israël tue Yahya Sinwar, leader du Hamas et cerveau du 7 octobre. La Droite interprète comme une victoire, la Gauche dit que ça ne change rien pour les civils. Depuis début octobre, le nord de Gaza est sous siège total, vidé de sa population.
ATTENTION : (1) La réaction à Sinwar est un test de positionnement parfait. (2) « Nettoyage ethnique » émerge chez la Gauche. (3) Volume potentiellement faible — chaque texte compte.""",
    "MANDATS_CPI": """CONTEXTE : Le 21 novembre 2024, la CPI émet des mandats d'arrêt contre Netanyahu et Gallant pour crimes de guerre (famine comme arme, attaques sur civils). Un mandat aussi contre Deif (Hamas). Un Comité de l'ONU conclut que la guerre est « cohérente avec le génocide ». Le 11 décembre, l'AG ONU vote à 158 voix un cessez-le-feu « immédiat, inconditionnel et permanent ».
ATTENTION : (1) Les mandats CPI forcent un positionnement binaire — capturer la position exacte. (2) « Génocide » est adossé à un rapport onusien. (3) Certains députés LR peuvent prendre leurs distances avec Israël.""",
    "CEASEFIRE_BREACH": """CONTEXTE : Janvier 2025, premier cessez-le-feu (phase 1 : échanges d'otages, retrait partiel). Mars 2025, Israël rompt le cessez-le-feu par une attaque surprise. Les hostilités reprennent.
ATTENTION : (1) Qui blâme qui pour la rupture ? Variable la plus discriminante. (2) Le retour de la guerre après un cessez-le-feu peut radicaliser ou lasser. (3) Knowledge cutoff de GPT-5 mini = mai 2024, il NE CONNAÎT PAS ces événements — ce briefing est essentiel.""",
    "NEW_OFFENSIVE": """CONTEXTE : Avril-mai 2025, Israël annonce la « conquête de Gaza » avec déplacement assumé vers le sud. Depuis mars, aucune aide humanitaire ne parvient à Gaza. Le 6 mai à l'AN, le ministre Barrot déclare « Rien ne peut justifier de tels actes » sous les applaudissements transpartisans (Dem, LFI, SOC, EcoS, GDR). La France prépare une conférence pour la reconnaissance de l'État de Palestine.
ATTENTION : (1) L'applaudissement transpartisan est un signal fort — la convergence se voit-elle dans les tweets ? (2) « Conquête » et « déplacement assumé » sont des termes nouveaux. (3) Reconnaissance de l'État de Palestine — sujet chez le Centre/Droite ?""",
}

SYSTEM_PROMPT = """Tu es un analyste politique spécialisé dans le discours parlementaire français sur le conflit israélo-palestinien. Tu annotes des textes (tweets et interventions à l'Assemblée nationale) de députés français.

TÂCHE : Pour chaque texte, produis une annotation structurée en JSON. Tu dois RAISONNER AVANT DE CLASSER — le champ "reasoning" est obligatoire et doit expliquer ta classification en 2-3 phrases.

ÉCHELLE DE STANCE (stance_v4) :
-2 = Pro-Israël fort : soutien explicite aux opérations militaires, défense inconditionnelle, dénonciation du Hamas comme seul responsable, rejet des critiques internationales
-1 = Pro-Israël modéré : reconnaissance du droit de se défendre, solidarité avec Israël, mais avec nuances (appel à la retenue, mention des civils, conditions)
 0 = Neutre/équilibré : mention des deux côtés, appel à la paix sans prendre parti, positionnement strictement diplomatique, ou texte trop ambigu pour trancher
+1 = Pro-Palestinien modéré : appel au cessez-le-feu, préoccupation humanitaire dominante, critique de la riposte israélienne sans vocabulaire radical
+2 = Pro-Palestinien fort : dénonciation du « génocide », appel à des sanctions/embargo, critique systémique d'Israël, vocabulaire de solidarité militante

RÈGLES DE CALIBRATION CRITIQUES :
1. Un texte qui condamne le Hamas ET appelle au cessez-le-feu n'est PAS automatiquement neutre. Évalue le poids relatif : si 80% du texte concerne les souffrances palestiniennes avec une phrase de condamnation du Hamas en introduction, c'est +1 ou +2.
2. « Cessez-le-feu » seul = au minimum +1, SAUF si explicitement conditionné à la destruction du Hamas (alors -1 ou 0).
3. « Droit de se défendre » sans aucune nuance = -1 minimum. Avec « mais proportionné » = 0.
4. La mention de « génocide » place quasi-systématiquement à +2, sauf citation neutre du terme juridique (CIJ).
5. Un texte qui ne parle QUE des otages sans mentionner Gaza = -1.
6. Un texte purement procédural ou institutionnel = 0.
7. Quand le texte est une question parlementaire, annote la POSITION du questionneur, pas la neutralité apparente de la question.

CEASEFIRE_TYPE :
- "unconditional" : cessez-le-feu immédiat, sans conditions préalables
- "conditional_hostages" : cessez-le-feu lié à la libération des otages
- "conditional_other" : cessez-le-feu avec autres conditions (désarmement Hamas, etc.)
- "humanitarian_pause" : pause humanitaire temporaire, pas un cessez-le-feu

CONDITIONALITY :
- "absolute" : position tranchée sans réserve
- "conditional" : position avec réserves explicites (« MAIS »)
- "balanced" : effort explicite de présenter les deux côtés

EMOTIONAL_REGISTER :
- "anger" : colère, accusation véhémente
- "grief" : tristesse, deuil, compassion
- "indignation" : dénonciation morale
- "fear" : inquiétude sécuritaire
- "solidarity" : soutien, fraternité
- "neutral" : ton factuel, diplomatique
- "defiance" : défi, provocation politique

EXEMPLES D'ANNOTATION :

EXEMPLE 1 — Pro-PAL fort (LFI, Twitter)
Texte : "Bombardements sur Rafah. Des enfants brûlés vifs. Netanyahou est un criminel de guerre. La France doit reconnaître l'État de Palestine et imposer un embargo sur les armes. #FreePalestine"
{"reasoning": "Vocabulaire de dénonciation véhémente ('criminel de guerre', 'enfants brûlés vifs'), demandes maximalistes (embargo, reconnaissance), hashtag militant. Position pro-PAL forte sans nuance.", "stance_v4": 2, "ceasefire_call": false, "ceasefire_type": null, "target_primary": "NETANYAHU", "target_secondary": "FRANCE_GOV", "frame_primary": "HUM", "conditionality": "absolute", "emotional_register": "anger", "key_demands": ["state_recognition", "arms_embargo"]}

EXEMPLE 2 — Centre/modéré avec concession (Renaissance, AN)
Texte : "La France a condamné avec la plus grande fermeté les actes terroristes du Hamas. Israël a le droit de se défendre. Mais ce droit ne saurait s'exercer au mépris du droit international humanitaire. C'est pourquoi nous appelons à un cessez-le-feu et à la libération immédiate de tous les otages."
{"reasoning": "Structure concessionnelle : condamnation Hamas + droit de se défendre MAIS droit international + cessez-le-feu. Le 'mais' est le pivot. Cessez-le-feu couplé aux otages → conditionnel.", "stance_v4": 0, "ceasefire_call": true, "ceasefire_type": "conditional_hostages", "target_primary": "HAMAS", "target_secondary": "ISRAEL_GOV", "frame_primary": "DIP", "conditionality": "conditional", "emotional_register": "neutral", "key_demands": ["ceasefire", "hostage_release"]}

EXEMPLE 3 — Pro-ISR fort (RN, Twitter)
Texte : "Le Hamas est une organisation terroriste islamiste. Ceux qui manifestent en France pour la 'Palestine' soutiennent le terrorisme. Israël se bat pour sa survie, comme nous devrions nous battre contre l'islamisme sur notre sol."
{"reasoning": "Amalgame manifestants/terroristes, cadrage sécuritaire domestique, aucune mention des civils palestiniens. Soutien inconditionnel + instrumentalisation intérieure.", "stance_v4": -2, "ceasefire_call": false, "ceasefire_type": null, "target_primary": "HAMAS", "target_secondary": null, "frame_primary": "SEC", "conditionality": "absolute", "emotional_register": "defiance", "key_demands": []}

EXEMPLE 4 — Ambigu (Gauche modérée, AN)
Texte : "Je veux redire ici notre solidarité avec les familles des otages. Leur douleur est insupportable. Il faut que le Hamas libère les otages. Et il faut que les bombardements cessent. Les enfants de Gaza n'ont pas choisi cette guerre."
{"reasoning": "Commence par les otages, mais consacre un poids égal aux bombardements et enfants de Gaza. L'appel à l'arrêt des bombardements est une forme implicite de cessez-le-feu. Conclusion pèse sur le sort des Palestiniens.", "stance_v4": 1, "ceasefire_call": true, "ceasefire_type": "conditional_hostages", "target_primary": "HAMAS", "target_secondary": "ISRAEL_ARMY", "frame_primary": "HUM", "conditionality": "balanced", "emotional_register": "grief", "key_demands": ["ceasefire", "hostage_release"]}

EXEMPLE 5 — Purement procédural
Texte : "Question au gouvernement sur la politique française au Moyen-Orient. La conférence humanitaire pour Gaza se tiendra à Paris le 9 novembre."
{"reasoning": "Texte purement informatif sans positionnement.", "stance_v4": 0, "ceasefire_call": false, "ceasefire_type": null, "target_primary": "FRANCE_GOV", "target_secondary": null, "frame_primary": "DIP", "conditionality": "balanced", "emotional_register": "neutral", "key_demands": []}

IMPORTANT : Réponds UNIQUEMENT avec un objet JSON valide. Pas de texte avant ou après. Champs obligatoires : reasoning, stance_v4 (-2 à +2), ceasefire_call, ceasefire_type, target_primary, target_secondary, frame_primary, conditionality, emotional_register, key_demands (liste).
"""

# JSON Schema pour structured outputs (mode json_schema)
# Note: OpenAI strict mode n'accepte pas additionalProperties, on définit tout explicitement
GLOBAL_SCHEMA = {
    "type": "object",
    "properties": {
        "reasoning": {"type": "string", "description": "2-3 phrases expliquant la classification"},
        "stance_v4": {"type": "integer", "enum": [-2, -1, 0, 1, 2]},
        "ceasefire_call": {"type": "boolean"},
        "ceasefire_type": {
            "type": "string",
            "enum": ["unconditional", "conditional_hostages", "conditional_other", "humanitarian_pause", "none"],
            "description": "null si ceasefire_call=false, sinon une des valeurs",
        },
        "target_primary": {"type": "string"},
        "target_secondary": {"type": "string", "description": "chaîne vide si pas de cible secondaire"},
        "frame_primary": {"type": "string", "enum": ["HUM", "SEC", "LEG", "DIP", "MOR", "DOM", "SOL"]},
        "conditionality": {"type": "string", "enum": ["absolute", "conditional", "balanced"]},
        "emotional_register": {
            "type": "string",
            "enum": ["anger", "grief", "indignation", "fear", "solidarity", "neutral", "defiance"],
        },
        "key_demands": {"type": "array", "items": {"type": "string"}},
    },
    "required": [
        "reasoning", "stance_v4", "ceasefire_call", "ceasefire_type",
        "target_primary", "target_secondary", "frame_primary",
        "conditionality", "emotional_register", "key_demands",
    ],
    "additionalProperties": False,
}


def build_json_schema_for_batch(batch_name: str) -> Dict:
    """Construit le schéma JSON avec les variables spécifiques au batch."""
    import copy
    schema = copy.deepcopy(GLOBAL_SCHEMA)
    schema["additionalProperties"] = True  # pour les vars période
    period_vars = PERIOD_VARS.get(BATCHES[batch_name]["period_vars"], {})
    for var_name, var_desc in period_vars.items():
        if "bool" in var_desc.lower():
            schema["properties"][var_name] = {"type": "boolean"}
        else:
            schema["properties"][var_name] = {"type": "string"}
        schema["required"].append(var_name)
    return schema


def format_user_message(row: pd.Series, batch_name: str) -> str:
    """Formate le message utilisateur pour l'API."""
    briefing = BRIEFINGS.get(batch_name, "")
    period_vars = PERIOD_VARS.get(BATCHES[batch_name]["period_vars"], {})
    period_desc = "\n".join(f"- {k}: {v}" for k, v in period_vars.items())

    depute_name = row.get("depute_name", row.get("author", row.get("speaker_name", row.get("AUTEUR", "Inconnu"))))
    groupe = row.get("groupe_politique", row.get("group", row.get("GROUPE", "Inconnu")))
    bloc = row.get("bloc", GROUP_TO_BLOC.get(groupe, "UNKNOWN"))
    registre = "tweet" if row.get("arena", "") == "Twitter" else "intervention AN"
    date = str(row.get("date", row.get("date_parsed", row.get("sitting_date", ""))))[:10]
    text = row.get("text", row.get("text_clean", row.get("cleaned_text", row.get("TEXTE", ""))))

    return f"""{briefing}

VARIABLES SPÉCIFIQUES À ANNOTER POUR CETTE PÉRIODE (en plus des variables globales) :
{period_desc}

Député : {depute_name}
Groupe : {groupe} (bloc : {bloc})
Registre : {registre}
Date : {date}

TEXTE :
\"\"\"
{text}
\"\"\"

Réponds UNIQUEMENT en JSON valide. Inclus les variables globales ET les variables spécifiques à la période."""


def check_coherence(ann: Dict) -> List[str]:
    """Retourne une liste de flags d'incohérence."""
    flags = []
    if ann.get("ceasefire_call") and ann.get("stance_v4") == -2:
        flags.append("INCOHERENT: ceasefire + stance=-2")
    reasoning = ann.get("reasoning", "").lower()
    if "génocide" in reasoning or "genocide" in reasoning:
        if ann.get("stance_v4", 0) < 1:
            flags.append("CHECK: génocide in reasoning but stance < 1")
    if ann.get("stance_v4") == 2 and ann.get("frame_primary") == "SEC":
        flags.append("UNUSUAL: pro-PAL fort + SEC frame")
    if ann.get("ceasefire_type") and not ann.get("ceasefire_call"):
        flags.append("INCOHERENT: ceasefire_type set but ceasefire_call=false")
    return flags


def parse_json_response(text: str) -> Optional[Dict]:
    """Parse la réponse JSON, gère markdown, guillemets typographiques, etc."""
    if not text or not isinstance(text, str):
        return None
    text = text.strip()
    # Enlever ```json ... ``` ou ``` ... ```
    if "```" in text:
        match = re.search(r"```(?:json)?\s*([\s\S]*?)```", text)
        if match:
            text = match.group(1).strip()
    # Extraire un objet JSON avec regex si le texte contient du bruit
    json_match = re.search(r"\{[\s\S]*\}", text)
    if json_match:
        text = json_match.group(0)
    # Remplacer guillemets typographiques par guillemets droits
    text = text.replace(""", '"').replace(""", '"').replace("'", "'").replace("'", "'")
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None


def annotate_single(
    client: OpenAI,
    row: pd.Series,
    batch_name: str,
    model: str = "gpt-5-nano",
    max_retries: int = 3,
) -> Dict[str, Any]:
    """Annote un seul texte. Utilise json_object (compatible tous modèles)."""
    import time
    user_msg = format_user_message(row, batch_name)

    for attempt in range(max_retries):
        try:
            # json_object au lieu de json_schema : gpt-5-nano peut ne pas supporter json_schema
            kwargs = {
                "model": model,
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_msg},
                ],
                "response_format": {"type": "json_object"},
            }
            # GPT-5 : max_completion_tokens plus élevé (modèle reasoning utilise tokens pour raisonner avant la sortie)
            if model.startswith("gpt-5"):
                kwargs["max_completion_tokens"] = 4000
            else:
                kwargs["max_tokens"] = 1000
            response = client.chat.completions.create(**kwargs)
            msg = response.choices[0].message
            content = msg.content
            # GPT-5 peut retourner content vide si refusal
            if not content and hasattr(msg, "refusal") and msg.refusal:
                return {"success": False, "error": f"refusal: {str(msg.refusal)[:150]}", "annotation": None, "raw": None}
            ann = parse_json_response(content)
            if ann and isinstance(ann, dict):
                stance = ann.get("stance_v4", ann.get("stance"))
                if stance is not None and stance in (-2, -1, 0, 1, 2):
                    if "stance_v4" not in ann:
                        ann["stance_v4"] = stance
                    # Compléter les champs manquants (json_object peut omettre)
                    for k, default in [("ceasefire_call", False), ("ceasefire_type", None), ("target_primary", "OTHER"),
                                       ("target_secondary", None), ("frame_primary", "DIP"), ("conditionality", "balanced"),
                                       ("emotional_register", "neutral"), ("key_demands", [])]:
                        if k not in ann:
                            ann[k] = default
                    flags = check_coherence(ann)
                    ann["flags"] = flags
                    return {"success": True, "annotation": ann, "raw": content}
            # Parse échoué ou structure invalide
            err_preview = (str(content)[:300] if content else "empty")
            return {"success": False, "error": f"parse_fail: {err_preview}", "annotation": None, "raw": content}
        except Exception as e:
            err_str = str(e)
            if attempt < max_retries - 1:
                if "429" in err_str or "rate_limit" in err_str.lower():
                    time.sleep(65)
                else:
                    time.sleep(2**attempt)
            if attempt == max_retries - 1:
                return {"success": False, "error": err_str[:300], "annotation": None, "raw": None}
    return {"success": False, "error": "max_retries", "annotation": None, "raw": None}


def annotate_batch(
    df: pd.DataFrame,
    batch_name: str,
    output_dir: Path,
    model: str = "gpt-5-nano",
    concurrency: int = 8,
    log_jsonl: bool = True,
) -> pd.DataFrame:
    """Annote un batch (séquentiel, client synchrone — évite Event loop is closed sur Windows)."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY non défini. Définissez-la avec os.environ['OPENAI_API_KEY'] = 'sk-...'")

    client = OpenAI(api_key=api_key)
    log_path = output_dir / f"annotation_v4_{batch_name}_log.jsonl"
    fail_log_path = output_dir / f"annotation_v4_{batch_name}_failures.jsonl"

    results = []
    for idx, row in tqdm(df.iterrows(), total=len(df), desc=f"Batch {batch_name}"):
        res = annotate_single(client, row, batch_name, model=model)
        if log_jsonl and res.get("raw"):
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(json.dumps({"idx": int(idx), "raw": res["raw"][:500] if res["raw"] else ""}, ensure_ascii=False) + "\n")
        if not res["success"]:
            with open(fail_log_path, "a", encoding="utf-8") as f:
                f.write(json.dumps({"idx": int(idx), "error": res.get("error", "")[:200]}, ensure_ascii=False) + "\n")
        results.append((idx, res))

    results.sort(key=lambda x: x[0])
    rows_out = []
    global_keys = {"reasoning", "stance_v4", "ceasefire_call", "ceasefire_type", "target_primary",
                   "target_secondary", "frame_primary", "conditionality", "emotional_register", "key_demands"}
    for idx, res in results:
        row = df.loc[idx].to_dict()
        if res["success"] and res["annotation"]:
            ann = res["annotation"]
            for k, v in ann.items():
                if k == "flags":
                    continue
                # Normaliser ceasefire_type "none" -> None
                if k == "ceasefire_type" and v == "none":
                    v = None
                if k == "target_secondary" and v == "":
                    v = None
                row[k] = v
            row["reasoning_v4"] = ann.get("reasoning")
            row["flags"] = ann.get("flags", [])
        else:
            row["annotation_failed"] = True
            row["flags"] = [res.get("error", "unknown")]
        rows_out.append(row)

    out_df = pd.DataFrame(rows_out)
    out_path = output_dir / f"annotations_v4_{batch_name}.parquet"
    out_df.to_parquet(out_path, index=False)
    return out_df


def run_annotation_batch_sync(
    df: pd.DataFrame,
    batch_name: str,
    output_dir: str = "outputs",
    model: str = "gpt-5-nano",
    concurrency: int = 8,
) -> pd.DataFrame:
    """Lance l'annotation d'un batch (séquentiel, stable sur Windows)."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    return annotate_batch(df, batch_name, output_path, model=model, concurrency=concurrency)
