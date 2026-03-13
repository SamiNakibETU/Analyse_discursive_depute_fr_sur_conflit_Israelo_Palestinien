"""
Parse le fichier Markdown avec les réseaux sociaux des députés
et extrait les noms pour recherche Twitter
"""

import re
import json
from pathlib import Path

INPUT_MD = Path(r"D:\Users\Proprietaire\Desktop\Projets\Revirement_politique_fr_gaza\twitter_account_député.md")
OUTPUT_JSON = Path("data/interim/deputes_from_markdown.json")
DEPUTES_UNIQUE = Path("data/interim/deputes_unique.json")

def parse_markdown_table(md_path):
    """Parse tableau Markdown et extrait noms députés"""

    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pattern pour lignes du tableau
    # | [M./Mme Nom](url) | réseaux |
    pattern = r'\|\s*\[(M\.|Mme)\s+([^\]]+)\]'

    deputes = []
    for match in re.finditer(pattern, content):
        civilite = match.group(1)
        nom_complet = match.group(2).strip()

        deputes.append({
            'nom_complet': nom_complet,
            'civilite': civilite
        })

    return deputes

def load_unique_deputes():
    """Charge députés déjà extraits de Phase 1"""
    try:
        with open(DEPUTES_UNIQUE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return {d['name']: d for d in data['deputes']}
    except:
        return {}

def main():
    print("="*70)
    print("PARSE MARKDOWN RÉSEAUX SOCIAUX")
    print("="*70)

    # Parse Markdown
    deputes_md = parse_markdown_table(INPUT_MD)
    print(f"\n✅ {len(deputes_md)} députés extraits du Markdown")

    # Load Phase 1 data
    deputes_phase1 = load_unique_deputes()
    print(f"✅ {len(deputes_phase1)} députés depuis Phase 1")

    # Match avec Phase 1
    matched = []
    not_in_phase1 = []

    for dep_md in deputes_md:
        nom = dep_md['nom_complet']

        if nom in deputes_phase1:
            # Trouvé dans Phase 1
            matched.append({
                'nom': nom,
                'civilite': dep_md['civilite'],
                'group': deputes_phase1[nom].get('group'),
                'interventions': deputes_phase1[nom].get('interventions_count', 0)
            })
        else:
            not_in_phase1.append(nom)

    print(f"\n✅ {len(matched)} députés matchés avec Phase 1")
    print(f"⚠️  {len(not_in_phase1)} députés non trouvés dans Phase 1")

    # Sauvegarder
    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)

    result = {
        'total_markdown': len(deputes_md),
        'matched_phase1': len(matched),
        'not_in_phase1': not_in_phase1[:10],  # Premiers 10
        'deputes': matched
    }

    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Sauvegardé: {OUTPUT_JSON}")

    # Exemples non trouvés
    if not_in_phase1:
        print(f"\n📋 Exemples députés dans Markdown mais PAS Phase 1:")
        for nom in not_in_phase1[:5]:
            print(f"   - {nom}")

    print("\n" + "="*70)
    print("✅ TERMINÉ")
    print("="*70)

if __name__ == "__main__":
    main()
