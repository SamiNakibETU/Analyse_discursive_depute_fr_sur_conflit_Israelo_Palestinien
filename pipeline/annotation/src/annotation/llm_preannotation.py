"""
Pre-annotation automatique via LLM (OpenAI GPT-4 ou Anthropic Claude).

Ce script genere des annotations de stance automatiques pour accelerer
le processus d'annotation manuelle.
"""

import json
import logging
import os
import time
from pathlib import Path
from typing import Optional, Literal

import pandas as pd
from tqdm import tqdm
from dotenv import load_dotenv

# Charger le fichier .env
PROJECT_ROOT_PARENT = Path(__file__).parent.parent.parent.parent
load_dotenv(PROJECT_ROOT_PARENT / ".env")

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).parent.parent.parent


STANCE_PROMPT = """Tu es un expert en analyse du discours politique francais.

Classifie le positionnement (stance) de ce texte concernant le conflit Gaza/Palestine.

Echelle:
- PRO_ISRAEL (-1): Soutien explicite a Israel, critique du Hamas/Palestine, defense du droit a se defendre
- NEUTRE (0): Position equilibree, appel a la paix sans blame clair, position institutionnelle
- PRO_PALESTINE (1): Critique explicite d'Israel, soutien a la cause palestinienne, utilisation de termes comme genocide/apartheid

Texte a analyser:
"{text}"

Reponds UNIQUEMENT avec un JSON de cette forme:
{{"stance": -1|0|1, "confidence": "high"|"medium"|"low", "keywords": ["mot1", "mot2"]}}
"""


def classify_with_openai(
    text: str,
    model: str = "gpt-4o-mini",
    api_key: Optional[str] = None
) -> dict:
    """Classification via OpenAI API."""
    try:
        from openai import OpenAI
    except ImportError:
        raise ImportError("pip install openai")
    
    client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
    
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "Tu es un assistant specialise en analyse politique."},
            {"role": "user", "content": STANCE_PROMPT.format(text=text[:2000])}
        ],
        temperature=0.1,
        max_tokens=150
    )
    
    content = response.choices[0].message.content.strip()
    
    # Parser le JSON
    try:
        # Nettoyer la reponse
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        elif "```" in content:
            content = content.split("```")[1].split("```")[0]
        
        result = json.loads(content)
        return {
            "stance": result.get("stance", 0),
            "confidence": result.get("confidence", "low"),
            "keywords": result.get("keywords", []),
            "raw_response": content
        }
    except json.JSONDecodeError:
        logger.warning(f"Failed to parse JSON: {content}")
        return {"stance": 0, "confidence": "low", "keywords": [], "raw_response": content}


def classify_with_anthropic(
    text: str,
    model: str = "claude-3-haiku-20240307",
    api_key: Optional[str] = None
) -> dict:
    """Classification via Anthropic API."""
    try:
        import anthropic
    except ImportError:
        raise ImportError("pip install anthropic")
    
    client = anthropic.Anthropic(api_key=api_key or os.getenv("ANTHROPIC_API_KEY"))
    
    response = client.messages.create(
        model=model,
        max_tokens=150,
        messages=[
            {"role": "user", "content": STANCE_PROMPT.format(text=text[:2000])}
        ]
    )
    
    content = response.content[0].text.strip()
    
    try:
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        elif "```" in content:
            content = content.split("```")[1].split("```")[0]
        
        result = json.loads(content)
        return {
            "stance": result.get("stance", 0),
            "confidence": result.get("confidence", "low"),
            "keywords": result.get("keywords", []),
            "raw_response": content
        }
    except json.JSONDecodeError:
        logger.warning(f"Failed to parse JSON: {content}")
        return {"stance": 0, "confidence": "low", "keywords": [], "raw_response": content}


def classify_with_ollama(
    text: str,
    model: str = "mistral",
    base_url: str = "http://localhost:11434"
) -> dict:
    """Classification via Ollama (local)."""
    import requests
    
    response = requests.post(
        f"{base_url}/api/generate",
        json={
            "model": model,
            "prompt": STANCE_PROMPT.format(text=text[:2000]),
            "stream": False,
            "options": {"temperature": 0.1}
        }
    )
    
    content = response.json().get("response", "").strip()
    
    try:
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        elif "```" in content:
            content = content.split("```")[1].split("```")[0]
        
        # Chercher le JSON dans la reponse
        import re
        json_match = re.search(r'\{[^}]+\}', content)
        if json_match:
            result = json.loads(json_match.group())
            return {
                "stance": result.get("stance", 0),
                "confidence": result.get("confidence", "low"),
                "keywords": result.get("keywords", []),
                "raw_response": content
            }
    except (json.JSONDecodeError, AttributeError):
        pass
    
    logger.warning(f"Failed to parse response: {content[:100]}")
    return {"stance": 0, "confidence": "low", "keywords": [], "raw_response": content}


def preannotate_corpus(
    input_file: Path,
    output_file: Path,
    provider: Literal["openai", "anthropic", "ollama"] = "openai",
    model: Optional[str] = None,
    sample_size: Optional[int] = None,
    delay_between_calls: float = 0.5,
    api_key: Optional[str] = None
) -> pd.DataFrame:
    """
    Pre-annote un corpus avec un LLM.
    
    Args:
        input_file: Fichier Parquet d'entree
        output_file: Fichier de sortie
        provider: openai, anthropic, ou ollama
        model: Nom du modele (defaut selon provider)
        sample_size: Nombre de textes a annoter (None = tous)
        delay_between_calls: Delai entre appels API (rate limiting)
        api_key: Cle API (ou variable d'environnement)
    """
    logger.info(f"Loading corpus from {input_file}")
    df = pd.read_parquet(input_file)
    
    if sample_size and sample_size < len(df):
        df = df.sample(n=sample_size, random_state=42)
        logger.info(f"Sampled {sample_size} texts")
    
    # Selecteur de fonction
    if provider == "openai":
        classify_fn = lambda t: classify_with_openai(t, model or "gpt-4o-mini", api_key)
    elif provider == "anthropic":
        classify_fn = lambda t: classify_with_anthropic(t, model or "claude-3-haiku-20240307", api_key)
    elif provider == "ollama":
        classify_fn = lambda t: classify_with_ollama(t, model or "mistral")
    else:
        raise ValueError(f"Unknown provider: {provider}")
    
    # Pre-annotation
    results = []
    errors = 0
    
    for idx, row in tqdm(df.iterrows(), total=len(df), desc="Pre-annotating"):
        text = row.get("text", "")
        
        try:
            result = classify_fn(text)
            results.append({
                "original_index": idx,
                "stance_llm": result["stance"],
                "confidence_llm": result["confidence"],
                "keywords_llm": result["keywords"]
            })
        except Exception as e:
            logger.warning(f"Error at index {idx}: {e}")
            results.append({
                "original_index": idx,
                "stance_llm": None,
                "confidence_llm": "error",
                "keywords_llm": []
            })
            errors += 1
        
        time.sleep(delay_between_calls)
    
    # Fusionner avec les donnees originales
    results_df = pd.DataFrame(results)
    df = df.reset_index(drop=True)
    df = pd.concat([df, results_df.drop(columns=["original_index"])], axis=1)
    
    # Sauvegarder
    output_file.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(output_file, index=False)
    
    logger.info(f"Pre-annotation complete: {len(df)} texts")
    logger.info(f"Errors: {errors}")
    logger.info(f"Saved to {output_file}")
    
    # Stats
    if "stance_llm" in df.columns:
        stance_counts = df["stance_llm"].value_counts()
        logger.info(f"Distribution stance LLM:")
        logger.info(f"  Pro-Israel (-1): {stance_counts.get(-1, 0)}")
        logger.info(f"  Neutre (0): {stance_counts.get(0, 0)}")
        logger.info(f"  Pro-Palestine (1): {stance_counts.get(1, 0)}")
    
    return df


def main():
    """Point d'entree pour tests."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Pre-annotation LLM")
    parser.add_argument("--input", type=str, required=True, help="Fichier Parquet d'entree")
    parser.add_argument("--output", type=str, required=True, help="Fichier de sortie")
    parser.add_argument("--provider", choices=["openai", "anthropic", "ollama"], default="openai")
    parser.add_argument("--model", type=str, default=None)
    parser.add_argument("--sample", type=int, default=None)
    parser.add_argument("--delay", type=float, default=0.5)
    
    args = parser.parse_args()
    
    preannotate_corpus(
        input_file=Path(args.input),
        output_file=Path(args.output),
        provider=args.provider,
        model=args.model,
        sample_size=args.sample,
        delay_between_calls=args.delay
    )


if __name__ == "__main__":
    main()
