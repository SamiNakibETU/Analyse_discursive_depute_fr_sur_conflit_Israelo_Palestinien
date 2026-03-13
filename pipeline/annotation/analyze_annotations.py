# -*- coding: utf-8 -*-
"""Analyse des annotations manuelles vs LLM."""
import pandas as pd
import sys
sys.stdout.reconfigure(encoding='utf-8')

df = pd.read_excel('data/annotated/predictions/annotation_llm.xlsx', sheet_name='Sheet1')

# Colonnes: STANCE = humain, stance_llm = LLM
# Filtrer les lignes annotees manuellement
annotated = df[df['STANCE'].notna()].copy()
print(f"=== ANNOTATIONS MANUELLES: {len(annotated)} ===")
print()

print("Distribution STANCE (HUMAIN):")
print(annotated['STANCE'].value_counts().sort_index().to_string())
print()

print("Distribution stance_llm (LLM):")
print(annotated['stance_llm'].value_counts().sort_index().to_string())
print()

# Accord
annotated['accord'] = annotated['STANCE'] == annotated['stance_llm']
accord_pct = annotated['accord'].mean() * 100
print(f"Accord exact: {accord_pct:.1f}%")
print()

# Matrice de confusion
print("=== MATRICE DE CONFUSION ===")
confusion = pd.crosstab(annotated['STANCE'], annotated['stance_llm'], 
                        rownames=['HUMAIN'], colnames=['LLM'])
print(confusion.to_string())
print()

# Desaccords detailles
desaccords = annotated[~annotated['accord']]
print(f"=== DESACCORDS ({len(desaccords)}) ===")
for _, row in desaccords.iterrows():
    text_preview = str(row.get('TEXTE', ''))[:150].replace('\n', ' ')
    source = row.get('SOURCE', 'N/A')
    groupe = row.get('GROUPE', 'N/A')
    auteur = row.get('AUTEUR', 'N/A')
    reasoning = str(row.get('reasoning_llm', ''))[:100]
    print(f"\nLLM={int(row['stance_llm'])} vs HUMAIN={int(row['STANCE'])} [{source}] [{groupe}] [{auteur}]")
    print(f"  TEXTE: {text_preview}...")
    print(f"  NOTES HUMAIN: {row.get('NOTES', 'N/A')}")
    print(f"  REASONING LLM: {reasoning}...")

# Hors sujet
print()
print("=== HORS SUJET ===")
hs = df[df['HORS_SUJET'] == 1]
print(f"Total marques hors sujet par humain: {len(hs)}")
# Comparer avec LLM
hs_llm = df[df['hors_sujet_llm'] == True]
print(f"Total marques hors sujet par LLM: {len(hs_llm)}")

# Accord hors sujet
both_annotated = df[(df['HORS_SUJET'].notna()) | (df['hors_sujet_llm'].notna())]
if len(both_annotated) > 0:
    hs_accord = ((df['HORS_SUJET'] == 1) == (df['hors_sujet_llm'] == True)).sum()
    print(f"Accord sur hors sujet: {hs_accord}")

for _, row in hs.head(5).iterrows():
    text_preview = str(row.get('TEXTE', ''))[:100].replace('\n', ' ')
    llm_hs = row.get('hors_sujet_llm', False)
    print(f"  [LLM_HS={llm_hs}] {text_preview}...")

# Analyse par source
print()
print("=== ACCORD PAR SOURCE ===")
for source in annotated['SOURCE'].unique():
    sub = annotated[annotated['SOURCE'] == source]
    acc = sub['accord'].mean() * 100
    print(f"  {source}: {acc:.1f}% ({len(sub)} textes)")

# Analyse par groupe politique
print()
print("=== ACCORD PAR GROUPE POLITIQUE ===")
for groupe in annotated['GROUPE'].dropna().unique():
    sub = annotated[annotated['GROUPE'] == groupe]
    if len(sub) >= 2:
        acc = sub['accord'].mean() * 100
        print(f"  {groupe}: {acc:.1f}% ({len(sub)} textes)")

# Patterns dans les erreurs
print()
print("=== PATTERNS D'ERREURS ===")
# LLM dit pro-Palestine mais humain dit neutre ou pro-Israel
llm_too_propal = desaccords[(desaccords['stance_llm'] == 1) & (desaccords['STANCE'] <= 0)]
print(f"LLM sur-estime pro-Palestine: {len(llm_too_propal)}")

# LLM dit pro-Israel mais humain dit neutre ou pro-Palestine  
llm_too_proisr = desaccords[(desaccords['stance_llm'] == -1) & (desaccords['STANCE'] >= 0)]
print(f"LLM sur-estime pro-Israel: {len(llm_too_proisr)}")

# LLM dit neutre mais humain dit autre chose
llm_too_neutral = desaccords[desaccords['stance_llm'] == 0]
print(f"LLM trop neutre: {len(llm_too_neutral)}")

# Exemples de chaque type d'erreur
print()
print("=== EXEMPLES D'ERREURS PAR TYPE ===")

if len(llm_too_propal) > 0:
    print("\n-- LLM sur-estime pro-Palestine --")
    for _, row in llm_too_propal.head(3).iterrows():
        text = str(row.get('TEXTE', ''))[:120].replace('\n', ' ')
        print(f"  [{row['GROUPE']}] {text}...")
        print(f"    Notes: {row.get('NOTES', 'N/A')}")

if len(llm_too_proisr) > 0:
    print("\n-- LLM sur-estime pro-Israel --")
    for _, row in llm_too_proisr.head(3).iterrows():
        text = str(row.get('TEXTE', ''))[:120].replace('\n', ' ')
        print(f"  [{row['GROUPE']}] {text}...")
        print(f"    Notes: {row.get('NOTES', 'N/A')}")

if len(llm_too_neutral) > 0:
    print("\n-- LLM trop neutre --")
    for _, row in llm_too_neutral.head(3).iterrows():
        text = str(row.get('TEXTE', ''))[:120].replace('\n', ' ')
        print(f"  [{row['GROUPE']}] HUMAIN={int(row['STANCE'])} | {text}...")
        print(f"    Notes: {row.get('NOTES', 'N/A')}")

# Distribution par periode
print()
print("=== DISTRIBUTION PAR PERIODE ===")
for periode in annotated['PERIODE'].dropna().unique():
    sub = annotated[annotated['PERIODE'] == periode]
    if len(sub) >= 2:
        stance_dist = sub['STANCE'].value_counts().sort_index().to_dict()
        print(f"  {periode}: {stance_dist} ({len(sub)} textes)")
