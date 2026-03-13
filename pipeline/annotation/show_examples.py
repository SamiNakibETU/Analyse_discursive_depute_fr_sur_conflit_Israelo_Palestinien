import pandas as pd
df = pd.read_parquet('data/annotated/tweets_preannotated.parquet')

print('=== EXEMPLES PRO-ISRAEL (-1) ===')
for _, row in df[df['stance_llm'] == -1].head(2).iterrows():
    print(f"@{row['username']} ({row['groupe_politique']})")
    print(f"Confidence: {row['confidence_llm']}")
    text = row['text'][:250].replace('\n', ' ')
    print(f"Text: {text}...")
    print()

print('=== EXEMPLES NEUTRE (0) ===')
for _, row in df[df['stance_llm'] == 0].head(2).iterrows():
    print(f"@{row['username']} ({row['groupe_politique']})")
    print(f"Confidence: {row['confidence_llm']}")
    text = row['text'][:250].replace('\n', ' ')
    print(f"Text: {text}...")
    print()

print('=== EXEMPLES PRO-PALESTINE (1) ===')
for _, row in df[df['stance_llm'] == 1].head(2).iterrows():
    print(f"@{row['username']} ({row['groupe_politique']})")
    print(f"Confidence: {row['confidence_llm']}")
    text = row['text'][:250].replace('\n', ' ')
    print(f"Text: {text}...")
    print()
