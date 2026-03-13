#!/usr/bin/env python3
"""
Script pour construire une liste propre des deputes avec leurs comptes Twitter.

Sources utilisees:
1. Interventions AN enrichies (pour avoir les deputes actifs sur Gaza)
2. API nosdeputes.fr (pour les comptes Twitter officiels)
3. Fichier de configuration manuel pour corrections
"""

import json
import sys
import re
from pathlib import Path
from collections import defaultdict

# Import urllib pour API
import urllib.request
import urllib.error


def load_interventions(path: Path) -> list:
    """Charge les interventions enrichies."""
    interventions = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            interventions.append(json.loads(line))
    return interventions


def extract_unique_deputes(interventions: list) -> dict:
    """Extrait les deputes uniques avec leurs stats."""
    deputes = defaultdict(lambda: {
        "name": "",
        "group": "",
        "intervention_count": 0,
        "legislature": None,
        "source": ""
    })
    
    for interv in interventions:
        name = interv.get("matched_name") or interv.get("speaker_name", "")
        if not name or name.lower() in ["", "n/a", "présidence de séance"]:
            continue
        
        group = interv.get("matched_group", "")
        leg = interv.get("matched_legislature")
        source = interv.get("matched_source", "")
        
        # Cle unique = nom normalise
        key = name.lower().strip()
        
        deputes[key]["name"] = name
        deputes[key]["intervention_count"] += 1
        
        if group:
            deputes[key]["group"] = group
        if leg:
            deputes[key]["legislature"] = leg
        if source:
            deputes[key]["source"] = source
    
    return dict(deputes)


def fetch_nosdeputes_twitter(legislature: int = 17) -> dict:
    """
    Recupere les comptes Twitter depuis nosdeputes.fr API.
    Retourne un dict {nom_slug: twitter_handle}
    """
    print(f"[INFO] Fetching nosdeputes.fr API (legislature {legislature})...")
    
    url = f"https://www.nosdeputes.fr/deputes/json"
    
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode("utf-8"))
    except Exception as e:
        print(f"[WARN] Erreur API nosdeputes.fr: {e}")
        return {}
    
    twitter_mapping = {}
    for entry in data.get("deputes", []):
        dep = entry.get("depute", {})
        twitter = dep.get("twitter", "")
        if twitter:
            # Normaliser le nom
            nom = dep.get("nom", "")
            slug = dep.get("slug", "")
            
            # Nettoyer le handle Twitter
            twitter = twitter.strip().lstrip("@").lower()
            
            twitter_mapping[nom.lower()] = {
                "twitter": twitter,
                "slug": slug,
                "groupe": dep.get("groupe_sigle", ""),
                "nom_complet": nom
            }
    
    print(f"[INFO] {len(twitter_mapping)} deputes avec Twitter trouves")
    return twitter_mapping


def normalize_name(name: str) -> str:
    """Normalise un nom pour le matching."""
    import unicodedata
    # Supprimer les titres
    name = re.sub(r"^(M\.|Mme|M |Mme )", "", name, flags=re.IGNORECASE).strip()
    # Normaliser les accents
    name = unicodedata.normalize("NFD", name)
    name = "".join(c for c in name if not unicodedata.combining(c))
    return name.lower().strip()


def match_deputes_to_twitter(deputes: dict, twitter_data: dict) -> list:
    """
    Associe les deputes aux comptes Twitter.
    """
    results = []
    matched = 0
    unmatched = []
    
    for key, dep_info in deputes.items():
        name = dep_info["name"]
        normalized = normalize_name(name)
        
        twitter_handle = None
        source = "not_found"
        
        # Chercher correspondance directe
        if normalized in twitter_data:
            twitter_handle = twitter_data[normalized]["twitter"]
            source = "nosdeputes_exact"
        else:
            # Chercher correspondance partielle
            for tw_name, tw_info in twitter_data.items():
                if normalized in tw_name or tw_name in normalized:
                    twitter_handle = tw_info["twitter"]
                    source = "nosdeputes_partial"
                    break
        
        result = {
            "depute_name": name,
            "normalized_name": normalized,
            "group": dep_info["group"],
            "intervention_count": dep_info["intervention_count"],
            "twitter_handle": twitter_handle,
            "twitter_source": source
        }
        
        if twitter_handle:
            matched += 1
        else:
            unmatched.append(name)
        
        results.append(result)
    
    # Trier par nombre d'interventions (les plus actifs en premier)
    results.sort(key=lambda x: x["intervention_count"], reverse=True)
    
    print(f"[INFO] {matched}/{len(deputes)} deputes avec Twitter trouve")
    print(f"[INFO] Top 10 sans Twitter: {unmatched[:10]}")
    
    return results


def main():
    print("=" * 60)
    print("CONSTRUCTION LISTE DEPUTES-TWITTER")
    print("=" * 60)
    
    base_path = Path(__file__).parent.parent
    
    # 1. Charger les interventions
    interv_path = base_path / "data" / "processed" / "interventions_enriched.jsonl"
    if not interv_path.exists():
        print(f"[ERROR] Fichier interventions non trouve: {interv_path}")
        sys.exit(1)
    
    print(f"\n[1] Chargement interventions: {interv_path}")
    interventions = load_interventions(interv_path)
    print(f"    {len(interventions)} interventions chargees")
    
    # 2. Extraire deputes uniques
    print("\n[2] Extraction deputes uniques...")
    deputes = extract_unique_deputes(interventions)
    print(f"    {len(deputes)} deputes uniques")
    
    # 3. Recuperer Twitter depuis nosdeputes.fr
    print("\n[3] Recuperation comptes Twitter...")
    twitter_data = fetch_nosdeputes_twitter()
    
    # 4. Matcher
    print("\n[4] Matching deputes <-> Twitter...")
    results = match_deputes_to_twitter(deputes, twitter_data)
    
    # 5. Sauvegarder
    output_path = base_path / "data" / "interim" / "deputes_twitter_clean.json"
    output = {
        "generated_at": __import__("datetime").datetime.now().isoformat(),
        "total_deputes": len(results),
        "with_twitter": len([r for r in results if r["twitter_handle"]]),
        "deputes": results
    }
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"\n[5] Sauvegarde: {output_path}")
    
    # Stats
    print("\n" + "=" * 60)
    print("STATISTIQUES")
    print("=" * 60)
    print(f"Total deputes actifs sur Gaza: {len(results)}")
    print(f"Avec compte Twitter trouve: {output['with_twitter']}")
    print(f"Sans compte Twitter: {len(results) - output['with_twitter']}")
    
    print("\nTop 10 deputes (par interventions):")
    for i, dep in enumerate(results[:10], 1):
        tw = f"@{dep['twitter_handle']}" if dep['twitter_handle'] else "?"
        print(f"  {i}. {dep['depute_name']} ({dep['group']}) - {dep['intervention_count']} interv - {tw}")
    
    return output_path


if __name__ == "__main__":
    main()








