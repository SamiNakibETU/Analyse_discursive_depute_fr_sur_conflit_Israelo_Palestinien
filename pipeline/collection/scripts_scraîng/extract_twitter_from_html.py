"""
Extrait les comptes Twitter officiels depuis le fichier HTML de l'Assemblée Nationale
"""

import re
import json
from pathlib import Path
from html.parser import HTMLParser

INPUT_HTML = Path(r"D:\Users\Proprietaire\Desktop\Projets\Revirement_politique_fr_gaza\twitter_account_deputé.html")
OUTPUT_JSON = Path("config/twitter_handles_assemblee.json")
EXISTING_MAPPING = Path("config/twitter_handles.json")

class TwitterExtractor(HTMLParser):
    """Parse HTML et extrait nom député + compte Twitter"""

    def __init__(self):
        super().__init__()
        self.deputes = {}
        self.current_depute = None
        self.in_depute_link = False
        self.in_twitter_link = False

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)

        # Lien vers fiche député
        if tag == 'a' and 'href' in attrs_dict:
            href = attrs_dict['href']

            # Fiche député
            if '/deputes/fiche/OMC_' in href:
                self.in_depute_link = True
                self.current_depute = None

            # Compte Twitter
            elif 'twitter.com' in href:
                self.in_twitter_link = True
                # Extraire @username depuis URL
                twitter_url = href
                # Format: https://twitter.com/@username/ ou https://twitter.com/username/
                match = re.search(r'twitter\.com/(@?\w+)', twitter_url)
                if match and self.current_depute:
                    username = match.group(1).replace('@', '')
                    self.deputes[self.current_depute] = username

    def handle_data(self, data):
        # Nom du député
        if self.in_depute_link:
            # Format: "M. Nom Prénom" ou "Mme Nom Prénom"
            data = data.strip()
            if data:
                # Enlever "M. " ou "Mme "
                name = re.sub(r'^(M\.|Mme)\s+', '', data)
                self.current_depute = name
                self.in_depute_link = False

    def handle_endtag(self, tag):
        if tag == 'a':
            self.in_twitter_link = False

def normalize_name(name):
    """Normalise nom pour matching"""
    # Enlever accents
    replacements = {
        'é': 'e', 'è': 'e', 'ê': 'e', 'ë': 'e',
        'à': 'a', 'â': 'a', 'ä': 'a',
        'ù': 'u', 'û': 'u', 'ü': 'u',
        'ô': 'o', 'ö': 'o',
        'î': 'i', 'ï': 'i',
        'ç': 'c'
    }

    normalized = name.lower()
    for old, new in replacements.items():
        normalized = normalized.replace(old, new)

    return normalized

def load_existing_mapping():
    """Charge mapping existant"""
    try:
        with open(EXISTING_MAPPING, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}

def main():
    print("="*70)
    print("EXTRACTION COMPTES TWITTER DEPUIS HTML ASSEMBLÉE NATIONALE")
    print("="*70)

    # Parse HTML
    with open(INPUT_HTML, 'r', encoding='utf-8') as f:
        html_content = f.read()

    parser = TwitterExtractor()
    parser.feed(html_content)

    print(f"\n✅ {len(parser.deputes)} comptes Twitter extraits du HTML")

    # Charger mapping existant
    existing = load_existing_mapping()
    print(f"✅ {len(existing)} comptes dans mapping existant")

    # Fusionner (HTML prioritaire car officiel)
    merged = existing.copy()
    new_count = 0
    updated_count = 0

    for depute, username in parser.deputes.items():
        if depute not in merged:
            new_count += 1
        elif merged[depute] != username:
            updated_count += 1
        merged[depute] = username

    print(f"\n📊 Résumé:")
    print(f"   Nouveaux comptes : {new_count}")
    print(f"   Comptes mis à jour : {updated_count}")
    print(f"   Total final : {len(merged)}")

    # Sauvegarder mapping HTML séparé
    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(parser.deputes, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Comptes HTML sauvegardés : {OUTPUT_JSON}")

    # Mettre à jour mapping principal
    with open(EXISTING_MAPPING, 'w', encoding='utf-8') as f:
        json.dump(merged, f, indent=2, ensure_ascii=False)

    print(f"✅ Mapping fusionné sauvegardé : {EXISTING_MAPPING}")

    # Exemples
    print(f"\n📋 EXEMPLES COMPTES TROUVÉS (10 premiers) :")
    for i, (name, username) in enumerate(list(parser.deputes.items())[:10], 1):
        print(f"   {i:2}. {name:35} → @{username}")

    print("\n" + "="*70)
    print("✅ TERMINÉ")
    print("="*70)
    print(f"\n💡 Prochaine étape : Relancer Phase 2 pour skip les députés mappés")
    print(f"   python scripts/phase2_generate_candidates.py")

if __name__ == "__main__":
    main()
