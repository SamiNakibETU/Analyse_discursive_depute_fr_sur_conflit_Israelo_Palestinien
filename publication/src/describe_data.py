# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 200)

# ── CORPUS V3 ──────────────────────────────────────────────────────────────────
print('=' * 70)
print('CORPUS V3 - BASELINE (corpus_v3.parquet)')
print('=' * 70)
v3 = pd.read_parquet('data/processed/corpus_v3.parquet')
print(f'Shape : {v3.shape[0]} lignes x {v3.shape[1]} colonnes')
print()
print('COLONNES DETAILLEES :')
for c in v3.columns:
    dtype = str(v3[c].dtype)
    nn = v3[c].notna().sum()
    try:
        sample = str(v3[c].dropna().iloc[0])[:70]
    except Exception:
        sample = 'N/A'
    print(f'  {c:<35} {dtype:<12} {nn:>6}/{len(v3)} non-null   ex: {sample}')

print()
print('STATS CLES :')
print(f'  Periode         : {v3["date"].min().date()} -> {v3["date"].max().date()}')
print(f'  Deputes uniques : {v3["author"].nunique()}')
print(f'  Twitter         : {(v3["arena"]=="Twitter").sum():,}')
print(f'  AN              : {(v3["arena"]=="AN").sum():,}')
print()
print('  Blocs:')
for b in ["Gauche radicale","Gauche moderee","Centre / Majorite","Droite"]:
    n = (v3["bloc"]==b).sum()
    print(f'    {b:<25} {n:>5} ({100*n/len(v3):.1f}%)')
print()
print('  stance_v3 distribution:')
for k, v in v3["stance_v3"].value_counts().sort_index().items():
    print(f'    {k:+.0f} : {v:>4} ({100*v/len(v3):.1f}%)')
print()
print('  confidence_v3:')
print(f'    mean={v3["confidence_v3"].mean():.3f}  min={v3["confidence_v3"].min():.2f}  max={v3["confidence_v3"].max():.2f}')
print()
print('  primary_frame_v3 (top 5):')
print(v3["primary_frame_v3"].value_counts().head(8).to_string())
print()
print('  primary_target_v3 (top 5):')
print(v3["primary_target_v3"].value_counts().head(8).to_string())

# ── CORPUS V4 ──────────────────────────────────────────────────────────────────
print()
print('=' * 70)
print('CORPUS V4 - ANNOTATIONS EVENEMENTIELLES (corpus_v4.parquet)')
print('=' * 70)
v4 = pd.read_parquet('data/processed/corpus_v4.parquet')
print(f'Shape : {v4.shape[0]} lignes x {v4.shape[1]} colonnes')
print()
print('COLONNES DETAILLEES :')
for c in v4.columns:
    dtype = str(v4[c].dtype)
    nn = v4[c].notna().sum()
    try:
        sample = str(v4[c].dropna().iloc[0])[:70]
    except Exception:
        sample = 'N/A'
    print(f'  {c:<38} {dtype:<12} {nn:>6}/{len(v4)} non-null   ex: {sample}')

print()
print('STATS CLES :')
print(f'  Deputes uniques : {v4["author"].nunique()}')
print()
print('  Repartition par batch:')
for b in ["CHOC","POST_CIJ","RAFAH","POST_SINWAR","MANDATS_CPI","CEASEFIRE_BREACH","NEW_OFFENSIVE"]:
    n = (v4["batch"]==b).sum()
    print(f'    {b:<20} {n:>5} textes')
print()
print('  stance_v4 distribution:')
for k, vv in v4["stance_v4"].value_counts().sort_index().items():
    print(f'    {k:+.0f} : {vv:>4} ({100*vv/len(v4):.1f}%)')
print()
print('  ceasefire_call:')
print(f'    True  : {v4["ceasefire_call"].sum():>4} ({100*v4["ceasefire_call"].mean():.1f}%)')
print(f'    False : {(~v4["ceasefire_call"]).sum():>4} ({100*(~v4["ceasefire_call"]).mean():.1f}%)')
print()
print('  ceasefire_type (quand ceasefire_call=True):')
ct = v4[v4["ceasefire_call"]==True]["ceasefire_type"].value_counts()
print(ct.to_string())
print()
print('  frame_primary (top 8):')
print(v4["frame_primary"].value_counts().head(8).to_string())
print()
print('  conditionality:')
print(v4["conditionality"].value_counts().to_string())
print()
print('  emotional_register:')
print(v4["emotional_register"].value_counts().to_string())
print()
print('  target_primary (top 10):')
print(v4["target_primary"].value_counts().head(10).to_string())
print()
print('  VARIABLES SPECIFIQUES PAR BATCH:')
period_vars = {
    'CHOC': ['condemns_hamas_attack','self_defense_mention','proportionality_issue','displacement_mention'],
    'POST_CIJ': ['icj_reference','genocide_framing','icc_mention'],
    'RAFAH': ['rafah_reaction','icc_mention','genocide_framing'],
    'POST_SINWAR': ['sinwar_reaction','famine_mention','ethnic_cleansing_frame'],
    'MANDATS_CPI': ['icc_warrants_position','genocide_framing'],
    'CEASEFIRE_BREACH': ['ceasefire_breach_blame','reconstruction_mention','two_state_mention'],
    'NEW_OFFENSIVE': ['conquest_framing','state_recognition_mention','transpartisan_convergence'],
}
for batch, vars_list in period_vars.items():
    sub = v4[v4["batch"]==batch]
    print(f'  [{batch}] {len(sub)} textes:')
    for var in vars_list:
        if var in sub.columns:
            vc = sub[var].value_counts()
            vc_str = ', '.join([f'{k}:{vv}' for k,vv in vc.items()])
            print(f'    {var:<35} {vc_str}')
