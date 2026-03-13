# -*- coding: utf-8 -*-
"""
Lance l'annotation LLM V2 sur le fichier d'annotation et compare avec les annotations humaines.
"""
import sys
sys.path.insert(0, str(__file__).replace("run_annotation_v2.py", ""))

import pandas as pd
from pathlib import Path
from tqdm import tqdm

sys.stdout.reconfigure(encoding='utf-8')

from src.annotation.llm_annotation_v2 import annotate_dataframe

def main():
    print("="*60)
    print("ANNOTATION LLM V2 - ETAT DE L'ART")
    print("="*60)
    
    # Load the annotation file
    input_file = Path("data/annotated/predictions/annotation_llm.xlsx")
    df = pd.read_excel(input_file, sheet_name="Sheet1")
    
    print(f"\nCharge: {len(df)} textes")
    print(f"Colonnes: {list(df.columns)[:10]}...")
    
    # Progress bar
    pbar = tqdm(total=len(df), desc="Annotation V2")
    
    def update_progress(current, total):
        pbar.n = current
        pbar.refresh()
    
    # Run annotation
    result_df = annotate_dataframe(
        df,
        text_col="TEXTE",
        source_col="SOURCE",
        author_col="AUTEUR",
        group_col="GROUPE",
        date_col="DATE",
        period_col="PERIODE",
        model="gpt-4o-mini",
        progress_callback=update_progress
    )
    
    pbar.close()
    
    # Save
    output_file = Path("data/annotated/predictions/annotation_llm_v2.xlsx")
    result_df.to_excel(output_file, index=False)
    print(f"\nSauvegarde: {output_file}")
    
    # Compare with human annotations
    print("\n" + "="*60)
    print("COMPARAISON AVEC ANNOTATIONS HUMAINES")
    print("="*60)
    
    # Only rows with human annotations
    human_annotated = result_df[result_df['STANCE'].notna()].copy()
    
    if len(human_annotated) > 0:
        print(f"\nTextes annotes par humain: {len(human_annotated)}")
        
        # V1 vs Human
        v1_accord = (human_annotated['STANCE'] == human_annotated['stance_llm']).mean() * 100
        print(f"\nAccord LLM V1 vs Humain: {v1_accord:.1f}%")
        
        # V2 vs Human
        v2_accord = (human_annotated['STANCE'] == human_annotated['stance_llm_v2']).mean() * 100
        print(f"Accord LLM V2 vs Humain: {v2_accord:.1f}%")
        
        # Detailed comparison
        print("\n--- Comparaison detaillee ---")
        for _, row in human_annotated.iterrows():
            human = int(row['STANCE'])
            v1 = int(row['stance_llm']) if pd.notna(row['stance_llm']) else None
            v2 = row['stance_llm_v2']
            
            v1_ok = "OK" if human == v1 else "X"
            v2_ok = "OK" if human == v2 else "X"
            
            text_preview = str(row['TEXTE'])[:60].replace('\n', ' ')
            print(f"\n[{row['GROUPE']}] {text_preview}...")
            print(f"  HUMAIN={human} | V1={v1} [{v1_ok}] | V2={v2} [{v2_ok}]")
            if human != v2:
                print(f"  V2 reasoning: {row.get('reasoning_v2', 'N/A')[:100]}...")
        
        # Confusion matrices
        print("\n--- Matrice de confusion V1 ---")
        print(pd.crosstab(human_annotated['STANCE'], human_annotated['stance_llm'], 
                          rownames=['HUMAIN'], colnames=['LLM_V1']))
        
        print("\n--- Matrice de confusion V2 ---")
        print(pd.crosstab(human_annotated['STANCE'], human_annotated['stance_llm_v2'], 
                          rownames=['HUMAIN'], colnames=['LLM_V2']))
        
        # Improvement analysis
        v1_errors = human_annotated[human_annotated['STANCE'] != human_annotated['stance_llm']]
        v2_fixed = v1_errors[v1_errors['STANCE'] == v1_errors['stance_llm_v2']]
        print(f"\nErreurs V1 corrigees par V2: {len(v2_fixed)}/{len(v1_errors)}")
    
    # Overall stats
    print("\n" + "="*60)
    print("STATISTIQUES GLOBALES V2")
    print("="*60)
    
    print(f"\nHors sujet detectes: {result_df['hors_sujet_v2'].sum()}")
    
    valid = result_df[~result_df['hors_sujet_v2']]
    print(f"\nDistribution stance V2:")
    print(valid['stance_llm_v2'].value_counts().sort_index())
    
    print(f"\nConfiance moyenne: {valid['confidence_v2'].mean():.2f}")
    print(f"Confiance mediane: {valid['confidence_v2'].median():.2f}")
    
    # By confidence
    high_conf = valid[valid['confidence_v2'] >= 0.8]
    med_conf = valid[(valid['confidence_v2'] >= 0.6) & (valid['confidence_v2'] < 0.8)]
    low_conf = valid[valid['confidence_v2'] < 0.6]
    
    print(f"\nPar niveau de confiance:")
    print(f"  High (>=0.8): {len(high_conf)} ({len(high_conf)/len(valid)*100:.1f}%)")
    print(f"  Medium (0.6-0.8): {len(med_conf)} ({len(med_conf)/len(valid)*100:.1f}%)")
    print(f"  Low (<0.6): {len(low_conf)} ({len(low_conf)/len(valid)*100:.1f}%)")
    
    print("\n" + "="*60)
    print("TERMINE")
    print("="*60)


if __name__ == "__main__":
    main()
