"""
Phase 1 : Extraction députés uniques
Analyse interventions_enriched.jsonl et extrait métadonnées
"""

import json
from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime

INPUT_PATH = Path("data/processed/interventions_enriched.jsonl")
OUTPUT_PATH = Path("data/interim/deputes_unique.json")

def normalize_name(name):
    """Normalise nom pour comparaisons"""
    if not name:
        return ""

    # Enlever accents
    replacements = {
        'é': 'e', 'è': 'e', 'ê': 'e', 'ë': 'e',
        'à': 'a', 'â': 'a', 'ä': 'a',
        'ù': 'u', 'û': 'u', 'ü': 'u',
        'ô': 'o', 'ö': 'o',
        'î': 'i', 'ï': 'i',
        'ç': 'c', 'ñ': 'n'
    }

    normalized = name.lower()
    for old, new in replacements.items():
        normalized = normalized.replace(old, new)

    return normalized.strip()

def calculate_priority_score(stats):
    """Score de priorité pour recherche Twitter"""
    # Plus d'interventions = plus prioritaire
    count_score = min(stats['count'] / 10 * 100, 100)
    return count_score

def main():
    print("="*70)
    print("PHASE 1 : EXTRACTION DÉPUTÉS UNIQUES")
    print("="*70)

    # Charger interventions
    interventions = []
    with open(INPUT_PATH, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    interventions.append(json.loads(line))
                except:
                    pass

    print(f"\n✅ {len(interventions)} interventions chargées")

    # Extraire orateurs uniques
    speaker_stats = defaultdict(lambda: {
        'count': 0,
        'group': None,
        'keywords': Counter(),
        'dates': []
    })

    for inter in interventions:
        # Plusieurs champs possibles pour le nom
        speaker = (
            inter.get('matched_name') or
            inter.get('speaker_name') or
            inter.get('orateur_nom_complet')
        )

        if not speaker:
            continue

        stats = speaker_stats[speaker]
        stats['count'] += 1
        stats['group'] = inter.get('matched_group') or inter.get('groupe')

        # Mots-clés mentionnés
        text = inter.get('raw_text', '').lower()
        for kw in ['gaza', 'palestine', 'israël', 'hamas', 'otage']:
            if kw in text:
                stats['keywords'][kw] += 1

        # Dates
        date = inter.get('sitting_date') or inter.get('date_seance')
        if date:
            stats['dates'].append(date)

    print(f"✅ {len(speaker_stats)} orateurs uniques identifiés")

    # Construire résultat
    deputes = []
    for name, stats in speaker_stats.items():
        priority = calculate_priority_score(stats)

        deputes.append({
            'name': name,
            'normalized_name': normalize_name(name),
            'group': stats['group'],
            'interventions_count': stats['count'],
            'priority_score': priority,
            'top_keywords': dict(stats['keywords'].most_common(3)),
            'first_intervention': min(stats['dates']) if stats['dates'] else None,
            'last_intervention': max(stats['dates']) if stats['dates'] else None
        })

    # Trier par priorité
    deputes.sort(key=lambda x: x['priority_score'], reverse=True)

    # Sauvegarder
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    result = {
        'extracted_at': datetime.now().isoformat(),
        'total_interventions': len(interventions),
        'unique_speakers': len(deputes),
        'deputes': deputes
    }

    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Résultat sauvegardé : {OUTPUT_PATH}")

    # Stats
    print(f"\n📊 TOP 10 DÉPUTÉS PRIORITAIRES :")
    for i, dep in enumerate(deputes[:10], 1):
        print(f"   {i:2}. {dep['name']:35} | {dep['group']:15} | {dep['interventions_count']:2} inter.")

    print("\n" + "="*70)
    print("✅ PHASE 1 TERMINÉE")
    print("="*70)

if __name__ == "__main__":
    main()
