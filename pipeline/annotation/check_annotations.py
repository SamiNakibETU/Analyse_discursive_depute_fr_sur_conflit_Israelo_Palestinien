# -*- coding: utf-8 -*-
import pandas as pd
import sys
sys.stdout.reconfigure(encoding='utf-8')

df = pd.read_excel('data/annotated/to_annotate/annotation_v2.xlsx')

print('=== ETAT DE L ANNOTATION ===')
print(f'Total lignes: {len(df)}')

# Colonnes en majuscules (comme dans le fichier)
annot_cols = ['STANCE', 'INTENSITE', 'CIBLE', 'CADRAGE', 'NOTES', 'HORS_SUJET']
print('\n=== COLONNES D ANNOTATION ===')
for col in annot_cols:
    if col in df.columns:
        non_null = df[col].notna()
        if df[col].dtype == 'object':
            non_empty = df[col].fillna('').astype(str).str.strip() != ''
            non_null = non_empty
        count = non_null.sum()
        print(f'{col}: {count} annotes ({count/len(df)*100:.1f}%)')
        if count > 0 and count < 50:
            vals = df.loc[non_null, col].value_counts().to_dict()
            print(f'  -> Valeurs: {vals}')

# Voir les lignes annotees
print('\n=== LIGNES ANNOTEES ===')
has_stance = df['STANCE'].notna() & (df['STANCE'].fillna('').astype(str).str.strip() != '')
has_hs = df['HORS_SUJET'].notna()

annotated_mask = has_stance | has_hs
annotated = df[annotated_mask]

print(f'Lignes avec annotation: {len(annotated)}')

if len(annotated) > 0:
    print('\nExemples:')
    for i, row in annotated.head(15).iterrows():
        auteur = str(row['AUTEUR'])[:25] if pd.notna(row['AUTEUR']) else '?'
        texte = str(row['TEXTE'])[:80].replace('\n', ' ') if pd.notna(row['TEXTE']) else ''
        stance = row['STANCE'] if pd.notna(row['STANCE']) else ''
        hs = row['HORS_SUJET'] if pd.notna(row['HORS_SUJET']) else ''
        print(f"[{row['SOURCE']}] {auteur}")
        print(f"  Stance: {stance} | Hors-sujet: {hs}")
        print(f"  '{texte}...'")
        print()
