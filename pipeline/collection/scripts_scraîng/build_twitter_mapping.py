"""Builds a Twitter handle mapping for Assembl?e nationale speakers."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List

ENRICHED_PATH = Path("FINAL/data/processed/interventions_enriched.jsonl")
OUTPUT_PATH = Path("FINAL/config/twitter_handles.json")

# Courtesy list of prominent deputies / members with verified Twitter handles.
KNOWN_HANDLES: Dict[str, str] = {
    # Gouvernement / Renaissance
    "Emmanuel Macron": "EmmanuelMacron",
    "Gabriel Attal": "GabrielAttal",
    "Elisabeth Borne": "Elisabeth_Borne",
    "Aurore Berg?": "auroreberge",
    "Cl?ment Beaune": "CBeaune",
    "Ya?l Braun-Pivet": "YaelBRAUNPIVET",
    "Olivier V?ran": "olivierveran",
    # LFI-NFP
    "Jean-Luc M?lenchon": "JLMelenchon",
    "Mathilde Panot": "MathildePanot",
    "Manuel Bompard": "mbompard",
    "Dani?le Obono": "Deputee_Obono",
    "Cl?mence Guett?": "ClemenceGuette",
    "Fran?ois Ruffin": "Francois_Ruffin",
    "Ugo Bernalicis": "Ugobernal",
    # PS-NFP
    "Olivier Faure": "faureolivier",
    "Val?rie Rabault": "valrabault",
    "Boris Vallaud": "BorisVallaud",
    "Laurent Baumel": "laurentbaumel",
    # ?cologistes
    "Marine Tondelier": "marinetondelier",
    "Cyrielle Chatelain": "CChatelain38",
    "Sandrine Rousseau": "sandrousseau",
    "Julien Bayou": "julienbayou",
    # RN
    "Marine Le Pen": "MLP_officiel",
    "Jordan Bardella": "J_Bardella",
    "S?bastien Chenu": "sebchenu",
    "Philippe Ballard": "BallardPhilippe",
    # LR
    "?ric Ciotti": "ECiotti",
    "Annie Genevard": "A_Genevard",
    "Aur?lien Pradi?": "AurelienPradie",
    # Horizons / Modem
    "Edouard Philippe": "EPhilippe_LH",
    "G?rald Darmanin": "GDarmanin",
    "Fran?ois Bayrou": "bayrou",
    # Autres personnalit?s souvent cit?es
    "Yael Braun-Pivet": "YaelBRAUNPIVET",
    "Olivier Faure": "faureolivier",
    "Fabien Roussel": "Fabien_Roussel",
    "Andr? Chassaigne": "AndreChassaigne",
    # S?nateurs / personnalit?s ext?rieures utiles
    "Jean-Yves Le Drian": "JY_LeDrian",
    "Nicolas Dupont-Aignan": "dupontaignan",
    "Fran?ois Hollande": "fhollande",
}


def load_interventions(path: Path) -> List[Dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(f"Fichier introuvable: {path}")
    interventions: List[Dict[str, str]] = []
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                interventions.append(json.loads(line))
            except json.JSONDecodeError as exc:
                print(f"[WARN] Ligne illisible: {exc}")
    return interventions


def extract_unique_speakers(interventions: List[Dict[str, dict]]) -> Dict[str, Dict[str, str]]:
    speakers: Dict[str, Dict[str, str]] = {}
    for record in interventions:
        matched_name = record.get("matched_name") or record.get("speaker_name")
        if not matched_name:
            continue
        if matched_name in speakers:
            continue
        speakers[matched_name] = {
            "displayName": matched_name,
            "group": record.get("matched_group"),
            "metadata": record.get("matched_metadata", {}),
        }
    return speakers


def apply_manual_handles(speakers: Dict[str, Dict[str, str]]) -> Dict[str, Dict[str, str]]:
    added = 0
    for name, handle in KNOWN_HANDLES.items():
        if name in speakers:
            speakers[name]["twitter"] = handle
            added += 1
        else:
            # allow rough matching ignoring accents/case
            normalized = name.lower().replace("?", "e").replace("?", "a").replace("?", "e")
            for candidate in speakers:
                simplified = candidate.lower().replace("?", "e").replace("?", "a").replace("?", "e")
                if normalized == simplified:
                    speakers[candidate]["twitter"] = handle
                    added += 1
                    break
    print(f"[INFO] Handles ajout?s manuellement: {added}")
    return speakers


def export_mapping(speakers: Dict[str, Dict[str, str]], output: Path) -> None:
    mapping = {}
    for name, data in speakers.items():
        handle = data.get("twitter")
        if handle:
            mapping[name] = handle
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(mapping, ensure_ascii=False, indent=2), encoding="utf-8")
    coverage = len(mapping) / max(1, len(speakers)) * 100
    print(f"[INFO] {len(mapping)} comptes mapp?s sur {len(speakers)} intervenants ({coverage:.1f}%).")
    print(f"[INFO] Mapping sauvegard? dans {output}")


def main() -> None:
    interventions = load_interventions(ENRICHED_PATH)
    print(f"[INFO] Interventions charg?es: {len(interventions)}")
    speakers = extract_unique_speakers(interventions)
    print(f"[INFO] Orateurs uniques: {len(speakers)}")
    speakers = apply_manual_handles(speakers)
    export_mapping(speakers, OUTPUT_PATH)


if __name__ == "__main__":
    main()
