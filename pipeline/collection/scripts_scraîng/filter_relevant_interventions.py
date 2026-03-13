#!/usr/bin/env python3
"""
Filtre les interventions pour ne garder que celles vraiment liées à Gaza/Palestine.

Probleme: Des mots génériques comme "hopital", "sanctions", "reconnaissance" 
captent des discussions sans lien avec Gaza/Palestine.

Solution: Exiger AU MOINS un mot-clé directement lié au conflit.
"""

import json
import sys
from pathlib import Path
from collections import defaultdict

# Mots-clés OBLIGATOIRES (au moins un doit être présent)
REQUIRED_KEYWORDS = {
    # Lieux spécifiques
    "gaza", "bande de gaza", "palestine", "israel", "cisjordanie", 
    "rafah", "khan younis", "jerusalem", "tel aviv",
    
    # Acteurs spécifiques
    "hamas", "hezbollah", "netanyahu", "netanyahou", "tsahal", "idf",
    "palestinien", "palestinienne", "palestiniens", "palestiniennes",
    "israelien", "israelienne", "israeliens", "israeliennes",
    "autorite palestinienne", "fatah", "unrwa",
    
    # Concepts spécifiques au conflit
    "7 octobre", "sept octobre", "cessez le feu", "cessez-le-feu",
    "etat palestinien", "solution a deux etats", "deux etats",
    "conflit israelopalestinien",
    
    # Termes politiques liés
    "sionisme", "sioniste", "antisionisme", "antisioniste",
}


def load_interventions(path: Path) -> list:
    interventions = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            interventions.append(json.loads(line))
    return interventions


def is_relevant(intervention: dict) -> bool:
    """Vérifie si l'intervention a au moins un mot-clé Gaza/Palestine obligatoire."""
    keywords = set(kw.lower() for kw in intervention.get("keyword_hits", []))
    return bool(keywords & REQUIRED_KEYWORDS)


def main():
    print("=" * 60)
    print("FILTRAGE DES INTERVENTIONS PERTINENTES")
    print("=" * 60)
    
    base_path = Path(__file__).parent.parent
    input_path = base_path / "data" / "processed" / "interventions_enriched.jsonl"
    output_path = base_path / "data" / "processed" / "interventions_gaza_filtered.jsonl"
    
    # Charger
    print(f"\n[1] Chargement: {input_path}")
    interventions = load_interventions(input_path)
    print(f"    {len(interventions)} interventions totales")
    
    # Filtrer
    print("\n[2] Filtrage (mot-clé Gaza/Palestine obligatoire)...")
    relevant = [i for i in interventions if is_relevant(i)]
    excluded = len(interventions) - len(relevant)
    
    print(f"    Pertinentes: {len(relevant)}")
    print(f"    Exclues: {excluded} ({excluded * 100 // len(interventions)}%)")
    
    # Stats sur les interventions filtrées
    print("\n[3] Analyse des interventions pertinentes...")
    
    # Par groupe
    by_group = defaultdict(int)
    for i in relevant:
        group = i.get("matched_group") or "Non identifié"
        by_group[group] += 1
    
    print("\n    Par groupe politique:")
    for group, count in sorted(by_group.items(), key=lambda x: -x[1])[:10]:
        print(f"      {group}: {count}")
    
    # Par période
    before_7oct = sum(1 for i in relevant if i["sitting_date"] < "2023-10-07")
    after_7oct = len(relevant) - before_7oct
    
    print(f"\n    Avant 7 octobre 2023: {before_7oct}")
    print(f"    Après 7 octobre 2023: {after_7oct}")
    if before_7oct > 0:
        print(f"    Ratio: {after_7oct / before_7oct:.1f}x plus après")
    
    # Mots-clés les plus fréquents
    all_keywords = defaultdict(int)
    for i in relevant:
        for kw in i.get("keyword_hits", []):
            all_keywords[kw] += 1
    
    print("\n    Top 10 mots-clés:")
    for kw, count in sorted(all_keywords.items(), key=lambda x: -x[1])[:10]:
        print(f"      {kw}: {count}")
    
    # Sauvegarder
    print(f"\n[4] Sauvegarde: {output_path}")
    with open(output_path, "w", encoding="utf-8") as f:
        for i in relevant:
            f.write(json.dumps(i, ensure_ascii=False) + "\n")
    
    # Résumé
    print("\n" + "=" * 60)
    print("RÉSUMÉ")
    print("=" * 60)
    print(f"Interventions totales: {len(interventions)}")
    print(f"Interventions Gaza/Palestine: {len(relevant)}")
    print(f"Taux de pertinence: {len(relevant) * 100 // len(interventions)}%")
    print(f"\nFichier filtré: {output_path}")
    
    return output_path


if __name__ == "__main__":
    main()








