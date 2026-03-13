import json
import os

# Le chemin de base est le répertoire 'config' où ce fichier se trouve
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

def load_json_config(filename):
    """Charge un fichier de configuration JSON."""
    path = os.path.join(BASE_DIR, filename)
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Erreur: Le fichier de configuration {filename} est introuvable.")
        return None
    except json.JSONDecodeError:
        print(f"Erreur: Le fichier {filename} n'est pas un JSON valide.")
        return None

def load_keywords():
    """Charge les mots-clés."""
    return load_json_config("keywords.json")

def load_selectors():
    """Charge les sélecteurs CSS."""
    return load_json_config("selectors.json")

def load_locuteur_selectors():
    """Charge les sélecteurs pour les locuteurs."""
    return load_json_config("locuteur_selectors.json")

def load_db_config():
    """Retourne la configuration de la base de données."""
    # Le nom de la DB est maintenant défini ici pour être cohérent
    return {"db_name": os.path.join(PROJECT_ROOT, "AN_Gaza.db")}

def load_urls():
    """Charge les URLs de base pour le scraping."""
    # Cette configuration était implicite, la rendre explicite est plus propre.
    return [
        {
            "legislature": 16,
            "base_url": "https://www.assemblee-nationale.fr/dyn/16/comptes-rendus/seance",
            "start_date": "2023-10-07",
            "end_date": "2024-06-09"
        },
        {
            "legislature": 17,
            "base_url": "https://www.assemblee-nationale.fr/dyn/17/comptes-rendus/seance",
            "start_date": "2024-07-18",
            "end_date": "2024-07-20" # A ajuster
        }
    ]

if __name__ == "__main__":
    # Test de chargement
    keywords = load_keywords()
    selectors = load_selectors()
    db_config = load_db_config()
    urls = load_urls()
    print("Mots-clés:", keywords)
    print("Sélecteurs:", selectors)
    print("Config DB:", db_config)
    print("URLs:", urls) 