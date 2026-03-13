# -*- coding: utf-8 -*-
"""
Lance la pre-annotation LLM sur le fichier d'annotation Excel.
"""

import json
import os
import sys
import time
from pathlib import Path

import pandas as pd
from tqdm import tqdm
from dotenv import load_dotenv

# Charger .env
load_dotenv(Path(__file__).parent.parent / ".env")

sys.stdout.reconfigure(encoding='utf-8')

STANCE_PROMPT = """Tu es un expert en analyse du discours politique francais sur le conflit Israel-Palestine.

Classifie le positionnement (stance) de ce texte.

Contexte: {context}
Auteur: {author} ({group})
Source: {source}

Texte:
"{text}"

Echelle de stance:
- PRO_ISRAEL (-1): Soutien explicite a Israel, critique du Hamas, defense du droit a se defendre, focus sur le 7 octobre/otages
- NEUTRE (0): Position equilibree, appel a la paix sans blame clair, position institutionnelle, ou sujet hors conflit
- PRO_PALESTINE (1): Critique explicite d'Israel/Netanyahu, soutien aux Palestiniens, termes comme genocide/apartheid/colonisation

Reponds UNIQUEMENT avec un JSON:
{{"stance": -1|0|1, "confidence": "high"|"medium"|"low", "reasoning": "explication courte", "hors_sujet": true|false}}
"""


def classify_text(client, text: str, context: str, author: str, group: str, source: str) -> dict:
    """Classifie un texte via OpenAI."""
    prompt = STANCE_PROMPT.format(
        text=text[:2500],
        context=context or "Aucun",
        author=author or "Inconnu",
        group=group or "Inconnu",
        source=source or "Inconnu"
    )
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Tu es un assistant specialise en analyse politique. Reponds uniquement en JSON valide."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
            max_tokens=200
        )
        
        content = response.choices[0].message.content.strip()
        
        # Nettoyer et parser
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        elif "```" in content:
            content = content.split("```")[1].split("```")[0]
        
        result = json.loads(content)
        return {
            "stance_llm": result.get("stance", 0),
            "confidence_llm": result.get("confidence", "low"),
            "reasoning_llm": result.get("reasoning", ""),
            "hors_sujet_llm": result.get("hors_sujet", False),
            "error": None
        }
        
    except json.JSONDecodeError as e:
        return {
            "stance_llm": None,
            "confidence_llm": "error",
            "reasoning_llm": f"JSON parse error: {content[:100]}",
            "hors_sujet_llm": None,
            "error": str(e)
        }
    except Exception as e:
        return {
            "stance_llm": None,
            "confidence_llm": "error",
            "reasoning_llm": "",
            "hors_sujet_llm": None,
            "error": str(e)
        }


def main():
    from openai import OpenAI
    
    # Charger le fichier d'annotation
    input_file = Path("data/annotated/to_annotate/annotation_v2.xlsx")
    output_file = Path("data/annotated/predictions/annotation_llm.xlsx")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"Chargement de {input_file}...")
    df = pd.read_excel(input_file)
    print(f"Total: {len(df)} textes a annoter")
    
    # Initialiser le client OpenAI
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("ERREUR: OPENAI_API_KEY non trouvee")
        sys.exit(1)
    
    client = OpenAI(api_key=api_key)
    
    # Pre-annoter chaque texte
    results = []
    errors = 0
    
    for idx, row in tqdm(df.iterrows(), total=len(df), desc="Pre-annotation LLM"):
        text = row.get("TEXTE", "")
        
        if pd.isna(text) or str(text).strip() == "":
            results.append({
                "stance_llm": None,
                "confidence_llm": "error",
                "reasoning_llm": "Texte vide",
                "hors_sujet_llm": None,
                "error": "empty"
            })
            continue
        
        result = classify_text(
            client=client,
            text=str(text),
            context=str(row.get("CONTEXTE", "")),
            author=str(row.get("AUTEUR", "")),
            group=str(row.get("GROUPE", "")),
            source=str(row.get("SOURCE", ""))
        )
        
        results.append(result)
        
        if result.get("error"):
            errors += 1
        
        # Rate limiting
        time.sleep(0.3)
    
    # Ajouter les resultats au DataFrame
    results_df = pd.DataFrame(results)
    df_annotated = pd.concat([df, results_df], axis=1)
    
    # Sauvegarder
    df_annotated.to_excel(output_file, index=False)
    print(f"\nSauvegarde: {output_file}")
    
    # Stats
    print("\n=== RESULTATS ===")
    print(f"Total: {len(df)}")
    print(f"Erreurs: {errors}")
    
    stance_counts = results_df["stance_llm"].value_counts()
    print(f"\nDistribution stance LLM:")
    print(f"  Pro-Israel (-1): {stance_counts.get(-1, 0)}")
    print(f"  Neutre (0): {stance_counts.get(0, 0)}")
    print(f"  Pro-Palestine (1): {stance_counts.get(1, 0)}")
    
    confidence_counts = results_df["confidence_llm"].value_counts()
    print(f"\nConfiance:")
    for conf, count in confidence_counts.items():
        print(f"  {conf}: {count}")
    
    hs_counts = results_df["hors_sujet_llm"].value_counts()
    print(f"\nHors-sujet detectes: {hs_counts.get(True, 0)}")


if __name__ == "__main__":
    main()
