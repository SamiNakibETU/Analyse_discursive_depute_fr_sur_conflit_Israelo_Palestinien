#!/usr/bin/env python3
"""
Test du système de matching de mots-clés.
Vérifie que le bug du regex word boundary est corrigé.
"""

import sys
from pathlib import Path

# Ajouter le chemin du module
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from final_pipeline.keywords import KeywordConfig, KeywordMatcher
from final_pipeline.utils.text import prepare_for_matching


def test_keyword_matching():
    """Test le matching des mots-clés."""
    
    # Charger la config
    config_path = Path(__file__).parent.parent / "config" / "keywords.json"
    config = KeywordConfig.load(config_path)
    matcher = KeywordMatcher(config)
    
    print("=" * 60)
    print("TEST DU SYSTÈME DE MATCHING DE MOTS-CLÉS")
    print("=" * 60)
    
    # Tests de mots simples
    test_cases = [
        # (texte, mots-clés attendus minimum)
        ("Gaza est un ghetto", ["gaza"]),
        ("L'armée israélienne bombarde", ["israelienne"]),
        ("Les Palestiniens souffrent", ["palestiniens"]),
        ("Netanyahu refuse le cessez-le-feu", ["netanyahu", "cessez le feu"]),
        ("Israël et la Palestine", ["israel", "palestine"]),
        ("Le Hamas a attaqué", ["hamas"]),
        ("La bande de Gaza est assiégée", ["bande de gaza", "gaza"]),
        ("Proche-Orient en crise", ["proche orient"]),
        ("Le 7 octobre 2023", ["7 octobre"]),
        ("L'UNRWA est menacée", ["unrwa"]),
        ("Crimes de guerre à Rafah", ["crimes de guerre", "rafah"]),
        ("Reconnaissance de l'État palestinien", ["etat palestinien"]),
        ("Aide humanitaire bloquée", ["aide humanitaire"]),
        ("Les otages doivent être libérés", ["otages"]),
        ("Génocide en cours", ["genocide"]),
        ("Colonisation en Cisjordanie", ["colonisation", "cisjordanie"]),
    ]
    
    all_passed = True
    
    for text, expected_keywords in test_cases:
        normalized = prepare_for_matching(text)
        found = matcher.find_matches(text)
        
        # Vérifier que tous les mots-clés attendus sont trouvés
        missing = [kw for kw in expected_keywords if kw not in found]
        
        status = "[OK]" if not missing else "[FAIL]"
        print(f"\n{status} Texte: \"{text}\"")
        print(f"   Normalisé: \"{normalized}\"")
        print(f"   Trouvé: {found}")
        
        if missing:
            print(f"   [!] MANQUANT: {missing}")
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("[OK] TOUS LES TESTS PASSENT !")
    else:
        print("[FAIL] CERTAINS TESTS ECHOUENT - Verifier le code de matching")
    print("=" * 60)
    
    return all_passed


def show_all_keywords():
    """Affiche tous les mots-clés configurés."""
    config_path = Path(__file__).parent.parent / "config" / "keywords.json"
    config = KeywordConfig.load(config_path)
    
    print("\n[MOTS-CLES CONFIGURES]:")
    print("-" * 40)
    
    for category, keywords in config.categories.items():
        print(f"\n{category.upper()} ({len(keywords)} termes):")
        for kw in keywords:
            print(f"  - {kw}")
    
    print(f"\nPHRASES ({len(config.phrases)} termes):")
    for phrase in config.phrases:
        print(f"  - {phrase}")


if __name__ == "__main__":
    show_all_keywords()
    print("\n")
    success = test_keyword_matching()
    sys.exit(0 if success else 1)

