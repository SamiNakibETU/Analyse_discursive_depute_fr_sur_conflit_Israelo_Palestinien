#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test direct API gpt-4o-mini sur 5 textes du batch POST_CIJ."""
import os, sys, json, time
sys.path.insert(0, '.')
import pandas as pd
from openai import OpenAI

api_key = os.environ.get('OPENAI_API_KEY')
if not api_key:
    print('ERREUR: OPENAI_API_KEY non défini')
    sys.exit(1)

client = OpenAI(api_key=api_key)
df = pd.read_parquet('outputs/annotations_v4_POST_CIJ.parquet')

SYSTEM = """Tu es un analyste politique. Annote ce texte en JSON avec exactement ces champs:
{"reasoning": "string", "stance_v4": int -2 a +2, "ceasefire_call": bool, "ceasefire_type": "string ou null"}
Réponds UNIQUEMENT en JSON valide."""

for i in range(5):
    row = df.iloc[i]
    text = str(row.get('text_clean', ''))[:500]
    print(f'\n--- Test {i+1} ---')
    print(f'Texte ({len(text)} chars): {text[:100]}...')

    try:
        resp = client.chat.completions.create(
            model='gpt-4o-mini',
            messages=[
                {'role': 'system', 'content': SYSTEM},
                {'role': 'user', 'content': f'TEXTE:\n"""{text}"""\n\nReponds en JSON.'}
            ],
            response_format={'type': 'json_object'},
            max_tokens=400
        )
        choice = resp.choices[0]
        print(f'finish_reason: {choice.finish_reason}')
        print(f'content: {repr(choice.message.content)[:300]}')
        if choice.message.refusal:
            print(f'refusal: {choice.message.refusal}')
        # Parse
        try:
            parsed = json.loads(choice.message.content or '{}')
            print(f'stance_v4: {parsed.get("stance_v4")} | ceasefire_call: {parsed.get("ceasefire_call")}')
            print('→ SUCCESS')
        except Exception as pe:
            print(f'→ PARSE FAIL: {pe}')
    except Exception as e:
        print(f'ERREUR API: {str(e)[:300]}')

    time.sleep(0.5)

print('\nTest terminé.')
