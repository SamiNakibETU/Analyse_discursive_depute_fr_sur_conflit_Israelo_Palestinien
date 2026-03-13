# -*- coding: utf-8 -*-
"""
Annotation LLM V2 - Etat de l'art
================================
Methodes implementees:
- Chain-of-Thought (CoT) prompting
- Few-shot examples from human annotations
- Context-aware (groupe politique, periode)
- Calibrated confidence thresholds
- Structured output with reasoning trace

Reference: Mohammad et al. (2016), Kuccuk & Can (2022)
"""

import json
import sys
import time
from pathlib import Path
from typing import Optional
from dataclasses import dataclass
from enum import Enum

import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv
import os

sys.stdout.reconfigure(encoding='utf-8')

# Load environment
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
load_dotenv(PROJECT_ROOT / ".env")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class Stance(Enum):
    PRO_ISRAEL = -1
    NEUTRAL = 0
    PRO_PALESTINE = 1
    HORS_SUJET = None


@dataclass
class AnnotationResult:
    stance: int
    confidence: float
    reasoning: str
    key_indicators: list
    hors_sujet: bool
    target: Optional[str] = None
    framing: Optional[str] = None


# =============================================================================
# CONTEXT: French Political Landscape
# =============================================================================

POLITICAL_CONTEXT = """
## Contexte politique francais sur Gaza/Palestine

### Groupes parlementaires et positions typiques:
- **LFI-NFP / GDR / ECO-NFP**: Generalement critiques d'Israel, solidaires avec la population palestinienne. Utilisent des termes comme "genocide", "massacre", "punition collective", "droit international".
- **RN**: Position variable, souvent axee sur l'antisemitisme et la securite. Soutien a Israel contre le "terrorisme islamiste".
- **LR / EPR / MODEM**: Position equilibree officielle, "droit d'Israel a se defendre" + "aide humanitaire". Focus sur les otages.
- **PS-NFP**: Historiquement pro-solution deux Etats, critique des actions israeliennes depuis 2023.

### Indicateurs linguistiques cles:
**Pro-Palestine** (stance=1):
- "genocide", "nettoyage ethnique", "apartheid", "colonisation"
- "population civile gazaouie", "enfants de Gaza", "blocus"
- "droit international", "CIJ", "CPI", "crimes de guerre"
- "cessez-le-feu immediat", "reconnaissance Etat palestinien"
- Critique Netanyahu, gouvernement israelien d'extreme-droite

**Pro-Israel** (stance=-1):
- "droit de se defendre", "legitime defense"
- "terrorisme Hamas", "barbarie", "pogrom du 7 octobre"
- "otages", "liberer les otages", "BringThemHome"
- "antisemitisme", "haine antijuive"
- Defense inconditionnelle des actions militaires

**Neutre** (stance=0):
- Appel equilibre "paix juste et durable"
- Condamnation des deux cotes sans prendre position
- Questions procedurales, techniques
- Demande d'information sans jugement

### Pieges a eviter:
1. "Solution a deux Etats" SEULE = neutre, MAIS si utilisee pour defendre une position (ex: "LFI est pour 2 Etats donc pas antisemite") = defense de position
2. Condamnation du Hamas seule ≠ pro-Israel (peut etre contexte)
3. Mention des otages ≠ automatiquement pro-Israel
4. Critique de Netanyahu ≠ automatiquement pro-Palestine
"""

# =============================================================================
# FEW-SHOT EXAMPLES (from human annotations)
# =============================================================================

FEW_SHOT_EXAMPLES = """
## Exemples annotes par un expert humain

### Exemple 1: Pro-Israel (stance=-1)
TEXTE: "N'oublions pas, n'oublions jamais. Solidarite avec les familles des victimes. #7octobre #BringThemHome"
GROUPE: EPR
ANALYSE:
- Focus exclusif sur les victimes israeliennes du 7 octobre
- Hashtag #BringThemHome = campagne pro-otages
- Aucune mention des victimes palestiniennes
- Framing memoriel israelien
STANCE: -1 (Pro-Israel)
CONFIANCE: 0.85

### Exemple 2: Pro-Palestine (stance=1)
TEXTE: "Le genocide en cours a Gaza doit cesser. La communaute internationale est complice de ce massacre. Cessez-le-feu maintenant!"
GROUPE: LFI-NFP
ANALYSE:
- Utilisation du terme "genocide" = qualification juridique forte
- "massacre" = condamnation des actions israeliennes
- Critique de la communaute internationale
- Demande de cessez-le-feu = position palestinienne
STANCE: 1 (Pro-Palestine)
CONFIANCE: 0.95

### Exemple 3: Neutre (stance=0)
TEXTE: "La France appelle a une solution a deux Etats, seule voie vers une paix juste et durable au Proche-Orient."
GROUPE: EPR
ANALYSE:
- Position officielle francaise equilibree
- Pas de critique explicite d'un camp
- "Paix juste et durable" = formulation diplomatique neutre
STANCE: 0 (Neutre)
CONFIANCE: 0.90

### Exemple 4: Pro-Palestine SUBTIL (stance=1)
TEXTE: "LFI est pour une solution a 2 Etats ce qui implique l'existence de l'Etat d'Israel. Vous m'accorderez qu'avec le gouvernement Netanyahu, que je condamne, c'est complique."
GROUPE: LFI-NFP
AUTEUR: Depute LFI
ANALYSE:
- Contexte: defense contre accusations d'antisemitisme
- "gouvernement Netanyahu que je condamne" = critique explicite
- La solution 2 Etats est utilisee pour DEFENDRE la position LFI
- Le but rhetorique est de legitimer les critiques envers Israel
STANCE: 1 (Pro-Palestine) - car l'argumentation defend une position critique d'Israel
CONFIANCE: 0.75

### Exemple 5: Hors sujet
TEXTE: "L'ordre du jour appelle la discussion de la proposition de loi sur les retraites..."
GROUPE: Presidence
ANALYSE:
- Texte procedural
- Aucun rapport avec le conflit Gaza/Palestine
- Meme si filtre par mots-cles, pas pertinent
HORS_SUJET: True
"""

# =============================================================================
# MAIN PROMPT
# =============================================================================

SYSTEM_PROMPT = f"""Tu es un expert en analyse du discours politique francais, specialise dans l'etude des positionnements sur le conflit israelo-palestinien.

{POLITICAL_CONTEXT}

{FEW_SHOT_EXAMPLES}

## Instructions d'annotation

Tu dois analyser chaque texte en suivant ces etapes:

### Etape 1: Verification pertinence
- Le texte parle-t-il reellement du conflit Gaza/Palestine/Israel?
- Si non → HORS_SUJET = true, arreter l'analyse

### Etape 2: Identification des indicateurs
- Lister les mots/expressions cles
- Identifier le framing utilise (humanitaire, securitaire, juridique, etc.)
- Noter le groupe politique de l'auteur (contexte, pas determinant)

### Etape 3: Analyse du positionnement
- Quelle est l'INTENTION rhetorique du texte?
- Qui est critique? Qui est soutenu?
- Y a-t-il une asymetrie dans le traitement des parties?

### Etape 4: Classification
- -1: Pro-Israel (soutient Israel, critique Hamas/Palestine, focus securite/otages)
- 0: Neutre (equilibre, appel a la paix sans prendre parti, procedural)
- 1: Pro-Palestine (critique Israel, solidarite Gaza, focus humanitaire/juridique)

### Etape 5: Calibration confiance
- 0.9-1.0: Position tres explicite, sans ambiguite
- 0.7-0.9: Position claire mais avec quelques nuances
- 0.5-0.7: Position implicite ou contexte ambigu
- <0.5: Incertitude elevee, peut-etre neutre par defaut

## IMPORTANT
- Ne pas sur-neutraliser: si un texte defend clairement un camp, classifier comme tel
- Tenir compte du CONTEXTE et de l'INTENTION, pas seulement des mots
- Le groupe politique informe mais ne determine pas la stance
- Un depute LFI peut faire une declaration neutre, un depute RN peut critiquer Netanyahu
"""

USER_PROMPT_TEMPLATE = """Analyse ce texte et fournis ton annotation au format JSON.

---
TEXTE: {text}
SOURCE: {source}
AUTEUR: {author}
GROUPE POLITIQUE: {group}
DATE: {date}
PERIODE: {period}
---

Reponds UNIQUEMENT avec un JSON valide de cette structure:
{{
    "hors_sujet": boolean,
    "stance": -1 | 0 | 1 | null,
    "confidence": 0.0-1.0,
    "reasoning": "Analyse detaillee en 2-3 phrases",
    "key_indicators": ["mot1", "mot2", ...],
    "target": "Israel" | "Palestine" | "Hamas" | "France" | "International" | null,
    "framing": "HUM" | "SEC" | "LEG" | "DIP" | "MOR" | null
}}

Rappel framing:
- HUM = Humanitaire (victimes civiles, aide)
- SEC = Securitaire (terrorisme, defense)
- LEG = Juridique (droit international, CIJ, CPI)
- DIP = Diplomatique (relations, reconnaissance)
- MOR = Moral (justice, valeurs)
"""


def annotate_text(
    text: str,
    source: str = "Unknown",
    author: str = "Unknown",
    group: str = "Unknown",
    date: str = "Unknown",
    period: str = "Unknown",
    model: str = "gpt-4o-mini",
    max_retries: int = 3
) -> AnnotationResult:
    """Annotate a single text with chain-of-thought reasoning."""
    
    user_prompt = USER_PROMPT_TEMPLATE.format(
        text=text[:2000],  # Truncate very long texts
        source=source,
        author=author,
        group=group,
        date=date,
        period=period
    )
    
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.1,  # Low temperature for consistency
                max_tokens=500,
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            
            return AnnotationResult(
                stance=result.get("stance"),
                confidence=result.get("confidence", 0.5),
                reasoning=result.get("reasoning", ""),
                key_indicators=result.get("key_indicators", []),
                hors_sujet=result.get("hors_sujet", False),
                target=result.get("target"),
                framing=result.get("framing")
            )
            
        except json.JSONDecodeError as e:
            if attempt < max_retries - 1:
                time.sleep(1)
                continue
            return AnnotationResult(
                stance=0,
                confidence=0.0,
                reasoning=f"JSON parse error: {e}",
                key_indicators=[],
                hors_sujet=False
            )
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(2)
                continue
            return AnnotationResult(
                stance=0,
                confidence=0.0,
                reasoning=f"API error: {e}",
                key_indicators=[],
                hors_sujet=False
            )


def annotate_dataframe(
    df: pd.DataFrame,
    text_col: str = "TEXTE",
    source_col: str = "SOURCE",
    author_col: str = "AUTEUR",
    group_col: str = "GROUPE",
    date_col: str = "DATE",
    period_col: str = "PERIODE",
    model: str = "gpt-4o-mini",
    progress_callback=None
) -> pd.DataFrame:
    """Annotate a full dataframe."""
    
    results = []
    total = len(df)
    
    for idx, row in df.iterrows():
        result = annotate_text(
            text=str(row.get(text_col, "")),
            source=str(row.get(source_col, "Unknown")),
            author=str(row.get(author_col, "Unknown")),
            group=str(row.get(group_col, "Unknown")),
            date=str(row.get(date_col, "Unknown")),
            period=str(row.get(period_col, "Unknown")),
            model=model
        )
        
        results.append({
            "stance_llm_v2": result.stance,
            "confidence_v2": result.confidence,
            "reasoning_v2": result.reasoning,
            "indicators_v2": json.dumps(result.key_indicators, ensure_ascii=False),
            "hors_sujet_v2": result.hors_sujet,
            "target_v2": result.target,
            "framing_v2": result.framing
        })
        
        if progress_callback:
            progress_callback(idx + 1, total)
        
        # Rate limiting
        time.sleep(0.5)
    
    result_df = pd.DataFrame(results)
    return pd.concat([df.reset_index(drop=True), result_df], axis=1)


# =============================================================================
# CLI
# =============================================================================

if __name__ == "__main__":
    from tqdm import tqdm
    import argparse
    
    parser = argparse.ArgumentParser(description="LLM Annotation V2")
    parser.add_argument("--input", required=True, help="Input Excel/Parquet file")
    parser.add_argument("--output", required=True, help="Output file")
    parser.add_argument("--sample", type=int, default=None, help="Sample size")
    parser.add_argument("--model", default="gpt-4o-mini", help="OpenAI model")
    
    args = parser.parse_args()
    
    # Load data
    input_path = Path(args.input)
    if input_path.suffix == ".xlsx":
        df = pd.read_excel(input_path)
    elif input_path.suffix == ".parquet":
        df = pd.read_parquet(input_path)
    else:
        df = pd.read_csv(input_path)
    
    print(f"Loaded {len(df)} rows")
    
    # Sample if requested
    if args.sample and args.sample < len(df):
        df = df.sample(args.sample, random_state=42)
        print(f"Sampled to {len(df)} rows")
    
    # Annotate with progress bar
    pbar = tqdm(total=len(df), desc="Annotating")
    
    def update_progress(current, total):
        pbar.update(1)
    
    result_df = annotate_dataframe(
        df,
        model=args.model,
        progress_callback=update_progress
    )
    
    pbar.close()
    
    # Save
    output_path = Path(args.output)
    if output_path.suffix == ".xlsx":
        result_df.to_excel(output_path, index=False)
    elif output_path.suffix == ".parquet":
        result_df.to_parquet(output_path, index=False)
    else:
        result_df.to_csv(output_path, index=False)
    
    print(f"\nSaved to {output_path}")
    
    # Stats
    print("\n=== RESULTATS ===")
    print(f"Hors sujet: {result_df['hors_sujet_v2'].sum()}")
    valid = result_df[~result_df['hors_sujet_v2']]
    print(f"\nDistribution stance:")
    print(valid['stance_llm_v2'].value_counts().sort_index())
    print(f"\nConfiance moyenne: {valid['confidence_v2'].mean():.2f}")
