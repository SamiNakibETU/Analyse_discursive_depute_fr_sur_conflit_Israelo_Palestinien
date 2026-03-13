# -*- coding: utf-8 -*-
"""
Compare les annotations manuelles avec les predictions LLM.
Calcule les metriques d'accord (accuracy, kappa, matrice de confusion).
"""

import sys
from pathlib import Path

import pandas as pd
import numpy as np

sys.stdout.reconfigure(encoding='utf-8')


def load_annotations():
    """Charge les annotations manuelles et LLM."""
    manual_file = Path("data/annotated/to_annotate/annotation_v2.xlsx")
    llm_file = Path("data/annotated/predictions/annotation_llm.xlsx")
    
    if not llm_file.exists():
        print(f"ERREUR: {llm_file} n'existe pas encore")
        print("Attendre la fin de run_llm_annotation.py")
        return None, None
    
    manual = pd.read_excel(manual_file)
    llm = pd.read_excel(llm_file)
    
    return manual, llm


def calculate_agreement(manual_df, llm_df):
    """Calcule les metriques d'accord entre annotations manuelles et LLM."""
    
    # Extraire les lignes annotees manuellement
    manual_annotated = manual_df[
        manual_df["STANCE"].notna() & 
        (manual_df["STANCE"].astype(str).str.strip() != "")
    ].copy()
    
    if len(manual_annotated) == 0:
        print("Aucune annotation manuelle trouvee")
        return
    
    print(f"Annotations manuelles: {len(manual_annotated)}")
    
    # Recuperer les predictions LLM correspondantes
    llm_predictions = llm_df.loc[manual_annotated.index, "stance_llm"]
    manual_values = manual_annotated["STANCE"].astype(float)
    
    # Filtrer les valeurs valides
    valid_mask = llm_predictions.notna() & manual_values.notna()
    manual_valid = manual_values[valid_mask]
    llm_valid = llm_predictions[valid_mask]
    
    if len(manual_valid) == 0:
        print("Pas assez de donnees pour comparer")
        return
    
    print(f"Paires valides pour comparaison: {len(manual_valid)}")
    
    # 1. Accuracy exacte
    exact_match = (manual_valid == llm_valid).sum()
    accuracy = exact_match / len(manual_valid)
    print(f"\n=== ACCORD EXACT ===")
    print(f"Accuracy: {accuracy:.1%} ({exact_match}/{len(manual_valid)})")
    
    # 2. Accord a +/- 1 (tolerance)
    close_match = (abs(manual_valid - llm_valid) <= 1).sum()
    accuracy_close = close_match / len(manual_valid)
    print(f"Accord (+/- 1): {accuracy_close:.1%} ({close_match}/{len(manual_valid)})")
    
    # 3. Matrice de confusion
    print(f"\n=== MATRICE DE CONFUSION ===")
    print("(Lignes = Manuel, Colonnes = LLM)")
    
    confusion = pd.crosstab(
        manual_valid, 
        llm_valid,
        rownames=["Manuel"],
        colnames=["LLM"]
    )
    print(confusion)
    
    # 4. Cohen's Kappa
    try:
        from sklearn.metrics import cohen_kappa_score, classification_report
        kappa = cohen_kappa_score(manual_valid, llm_valid)
        print(f"\n=== COHEN'S KAPPA ===")
        print(f"Kappa: {kappa:.3f}")
        
        if kappa < 0.2:
            interpretation = "Accord faible"
        elif kappa < 0.4:
            interpretation = "Accord modere"
        elif kappa < 0.6:
            interpretation = "Accord substantiel"
        else:
            interpretation = "Accord fort"
        print(f"Interpretation: {interpretation}")
        
        # Classification report
        print(f"\n=== RAPPORT DETAILLE ===")
        labels = [-1, 0, 1]
        target_names = ["Pro-Israel", "Neutre", "Pro-Palestine"]
        print(classification_report(manual_valid, llm_valid, labels=labels, target_names=target_names, zero_division=0))
        
    except ImportError:
        print("sklearn non installe - pas de kappa calcule")
    
    # 5. Analyse des desaccords
    print(f"\n=== DESACCORDS ===")
    disagreements = manual_annotated[valid_mask & (manual_valid != llm_valid)]
    
    if len(disagreements) > 0:
        print(f"Nombre de desaccords: {len(disagreements)}")
        print("\nExemples de desaccords:")
        
        for i, (idx, row) in enumerate(disagreements.head(5).iterrows()):
            text = str(row["TEXTE"])[:100].replace("\n", " ")
            manual_stance = manual_values.loc[idx]
            llm_stance = llm_predictions.loc[idx]
            
            print(f"\n{i+1}. [{row['SOURCE']}] {row['AUTEUR'][:25] if pd.notna(row['AUTEUR']) else '?'}")
            print(f"   Manuel: {manual_stance} | LLM: {llm_stance}")
            print(f"   '{text}...'")
    
    # 6. Analyse par confiance LLM
    if "confidence_llm" in llm_df.columns:
        print(f"\n=== ACCORD PAR CONFIANCE LLM ===")
        for conf in ["high", "medium", "low"]:
            conf_mask = valid_mask & (llm_df.loc[manual_annotated.index, "confidence_llm"] == conf)
            if conf_mask.sum() > 0:
                conf_accuracy = (manual_values[conf_mask] == llm_predictions[conf_mask]).mean()
                print(f"  {conf}: {conf_accuracy:.1%} (n={conf_mask.sum()})")


def main():
    manual, llm = load_annotations()
    if manual is None:
        return
    
    print("="*60)
    print("COMPARAISON ANNOTATIONS MANUELLES vs LLM")
    print("="*60)
    
    calculate_agreement(manual, llm)
    
    print("\n" + "="*60)
    print("RECOMMANDATION")
    print("="*60)
    print("""
Si l'accord est:
- > 80% : Le LLM est fiable, utiliser ses predictions
- 60-80% : Verifier manuellement les cas a faible confiance
- < 60% : Revoir le prompt ou annoter plus de donnees
    """)


if __name__ == "__main__":
    main()
