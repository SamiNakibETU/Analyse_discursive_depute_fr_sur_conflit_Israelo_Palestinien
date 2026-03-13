"""
Phase 2 : Génération candidats usernames Twitter
"""

import json
from pathlib import Path
from datetime import datetime

INPUT_PATH = Path("data/interim/deputes_unique.json")
MAPPING_PATH = Path("config/twitter_handles.json")
OUTPUT_PATH = Path("data/interim/twitter_candidates.json")

def normalize_for_username(text):
    """Normalise pour username Twitter (sans accents, minuscules)"""
    replacements = {
        'é': 'e', 'è': 'e', 'ê': 'e', 'ë': 'e',
        'à': 'a', 'â': 'a', 'ä': 'a',
        'ù': 'u', 'û': 'u', 'ü': 'u',
        'ô': 'o', 'ö': 'o',
        'î': 'i', 'ï': 'i',
        'ç': 'c', 'ñ': 'n',
        '-': '', "'": '', ' ': ''
    }

    normalized = text.lower()
    for old, new in replacements.items():
        normalized = normalized.replace(old, new)

    return normalized

def generate_username_candidates(name):
    """
    Génère candidats possibles pour username Twitter

    Patterns testés :
    - PrenomNom (GabrielAttal, ElisaMartinGre)
    - NomPrenom (AttalGabriel)
    - Prenom_Nom (gabriel_attal, elisa_martin_gre)
    - InitialeNom (GAttal, jnbarrot)
    - prenomnom (gabrielattal, benjaminhaddad)
    """

    parts = name.split()
    if len(parts) < 2:
        return []

    prenom = normalize_for_username(parts[0])
    nom = normalize_for_username(parts[-1])

    # Si nom composé (ex: Jean-Luc), prendre première partie + initiales
    if '-' in parts[0]:
        prenom_parts = parts[0].split('-')
        prenom_short = normalize_for_username(prenom_parts[0])
        # Initiales composées (Jean-Noël → jn)
        initiales_composees = ''.join([p[0] for p in prenom_parts if p])
    else:
        prenom_short = prenom
        initiales_composees = prenom[0] if prenom else ''

    candidates = set()

    # Pattern 1 : PrenomNom capitalisé
    candidates.add(f"{prenom.capitalize()}{nom.capitalize()}")

    # Pattern 2 : NomPrenom capitalisé
    candidates.add(f"{nom.capitalize()}{prenom.capitalize()}")

    # Pattern 3 : prenom_nom underscore
    candidates.add(f"{prenom}_{nom}")
    candidates.add(f"{prenom}.{nom}")

    # Pattern 4 : InitialeNom (majuscule ET minuscule)
    if prenom:
        candidates.add(f"{prenom[0].upper()}{nom.capitalize()}")
        candidates.add(f"{prenom[0].lower()}{nom.lower()}")  # NOUVEAU: jnbarrot
    if prenom_short:
        candidates.add(f"{prenom_short[0].upper()}{nom.capitalize()}")

    # Pattern 5 : Initiales composées + nom (Jean-Noël Barrot → jnbarrot)
    if initiales_composees and len(initiales_composees) > 1:
        candidates.add(f"{initiales_composees.lower()}{nom.lower()}")
        candidates.add(f"{initiales_composees.upper()}{nom.capitalize()}")

    # Pattern 6 : prenomnom minuscule (benjaminhaddad)
    candidates.add(f"{prenom}{nom}")
    candidates.add(f"{prenom.lower()}{nom.lower()}")

    # Pattern 7 : Nom seul
    candidates.add(nom.capitalize())
    candidates.add(nom.lower())

    # Pattern 8 : Variations géographiques (ElisaMartinGre, ElisaMartin38)
    suffixes_geo = ['Gre', '38', '69', '75', 'Paris']
    for suffix in suffixes_geo:
        candidates.add(f"{prenom.capitalize()}{nom.capitalize()}{suffix}")
        candidates.add(f"{prenom}_{nom}_{suffix.lower()}")

    # Pattern 9 : Variations avec underscore
    candidates.add(f"{prenom}_{nom}".replace('-', ''))

    return sorted(list(candidates))

def load_existing_mapping():
    """Charge mapping existant"""
    try:
        with open(MAPPING_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}

def main():
    print("="*70)
    print("PHASE 2 : GÉNÉRATION CANDIDATS USERNAMES")
    print("="*70)

    # Charger députés
    with open(INPUT_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    deputes = data['deputes']
    print(f"\n✅ {len(deputes)} députés chargés")

    # Charger mapping existant
    existing = load_existing_mapping()
    print(f"✅ {len(existing)} handles déjà mappés")

    # Générer candidats pour députés non mappés
    candidates_list = []

    for dep in deputes:
        name = dep['name']

        # Skip si déjà mappé
        if name in existing:
            print(f"⏭️  {name:40} | Déjà mappé: @{existing[name]}")
            continue

        # Générer candidats
        candidates = generate_username_candidates(name)

        candidates_list.append({
            'depute_name': name,
            'normalized_name': dep['normalized_name'],
            'group': dep['group'],
            'priority_score': dep['priority_score'],
            'interventions_count': dep['interventions_count'],
            'username_candidates': candidates,
            'status': 'to_validate'
        })

        print(f"✅ {name:40} | {len(candidates)} candidats")

    print(f"\n✅ {len(candidates_list)} députés à valider")

    # Sauvegarder
    result = {
        'generated_at': datetime.now().isoformat(),
        'total_deputes': len(deputes),
        'already_mapped': len(existing),
        'to_find': len(candidates_list),
        'candidates': candidates_list
    }

    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Candidats sauvegardés : {OUTPUT_PATH}")

    # Exemples
    print(f"\n📋 EXEMPLES CANDIDATS (Top 5) :")
    for i, cand in enumerate(candidates_list[:5], 1):
        print(f"\n   {i}. {cand['depute_name']}")
        print(f"      Candidats : {', '.join(cand['username_candidates'][:4])}")

    print("\n" + "="*70)
    print("✅ PHASE 2 TERMINÉE")
    print("="*70)

if __name__ == "__main__":
    main()
