# -*- coding: utf-8 -*-
"""
Annotation LLM V3 - Etat de l'art academique
============================================
Ameliorations par rapport a V2:
1. Schema d'annotation multi-dimensionnel (stance + intensite + cible + frame)
2. Prompts differencies TWEETS vs INTERVENTIONS PARLEMENTAIRES
3. Echelle 5 points pour plus de nuance (-2, -1, 0, 1, 2)
4. Calibration confiance par seuils explicites
5. Chain-of-Thought structure en etapes
6. Few-shot dynamique selon le type de source

References academiques:
- Mohammad et al. (2016) "SemEval-2016 Task 6: Stance Detection"
- Kuccuk & Can (2020) "Stance Detection: A Survey"
- Aldayel & Magdy (2021) "Stance Detection on Social Media"
- Hroub & Waxman - Media framing Israel-Palestine
"""

import json
import sys
import time
import re
from pathlib import Path
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, asdict
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


# =============================================================================
# SCHEMA D'ANNOTATION ACADEMIQUE
# =============================================================================

class StanceScale(Enum):
    """Echelle 5 points inspiree de Likert pour plus de nuance."""
    STRONGLY_PRO_ISRAEL = -2   # Soutien explicite et fort a Israel
    LEAN_PRO_ISRAEL = -1       # Tendance pro-Israel, moins explicite
    NEUTRAL = 0                # Equilibre ou pas de position claire
    LEAN_PRO_PALESTINE = 1     # Tendance pro-Palestine, moins explicite
    STRONGLY_PRO_PALESTINE = 2 # Soutien explicite et fort a la Palestine


class FrameType(Enum):
    """Types de cadrage mediatique (Entman, 1993)."""
    HUMANITARIAN = "HUM"       # Victimes civiles, aide, souffrance
    SECURITY = "SEC"           # Terrorisme, defense, menaces
    LEGAL = "LEG"              # Droit international, CIJ, CPI, crimes
    DIPLOMATIC = "DIP"         # Relations internationales, reconnaissance
    MORAL = "MOR"              # Justice, valeurs, droits humains
    HISTORICAL = "HIS"         # Histoire du conflit, memoire
    ECONOMIC = "ECO"           # Sanctions, boycott, aide financiere


class TargetEntity(Enum):
    """Entites cibles du discours."""
    ISRAEL_GOV = "ISRAEL_GOV"           # Gouvernement/Etat d'Israel
    ISRAEL_PEOPLE = "ISRAEL_PEOPLE"     # Population israelienne/civils
    PALESTINE_GOV = "PALESTINE_GOV"     # AP/Hamas/Autorite palestinienne
    PALESTINE_PEOPLE = "PALESTINE_PEOPLE" # Population palestinienne/civils
    HAMAS = "HAMAS"                     # Hamas specifiquement
    NETANYAHU = "NETANYAHU"             # Netanyahu specifiquement
    INTERNATIONAL = "INTERNATIONAL"     # Communaute internationale
    FRANCE = "FRANCE"                   # Position francaise


@dataclass
class AnnotationResultV3:
    """Structure de resultat enrichie."""
    # Classification principale
    stance: int                    # -2 a 2
    intensity: str                 # "strong", "moderate", "weak"
    confidence: float              # 0.0 a 1.0
    
    # Dimensions supplementaires
    primary_target: Optional[str]  # Cible principale
    secondary_target: Optional[str]# Cible secondaire
    primary_frame: Optional[str]   # Cadrage principal
    secondary_frame: Optional[str] # Cadrage secondaire
    
    # Meta-annotations
    is_off_topic: bool            # Hors sujet
    is_ambiguous: bool            # Position ambigue
    has_both_sides: bool          # Mentionne les deux cotes
    
    # Explicabilite
    reasoning: str                # Raisonnement detaille
    key_indicators: List[str]     # Mots-cles identifies
    rhetorical_strategy: str      # Strategie rhetorique
    
    # Conversion 3 classes pour compatibilite
    @property
    def stance_3class(self) -> int:
        """Convertit en echelle -1/0/1 pour compatibilite."""
        if self.stance <= -1:
            return -1
        elif self.stance >= 1:
            return 1
        return 0


# =============================================================================
# CONTEXTE POLITIQUE ENRICHI
# =============================================================================

POLITICAL_CONTEXT = """
## Contexte politique francais sur Gaza/Palestine (2023-2025)

### Groupes parlementaires et positions typiques:

| Groupe | Position generale | Marqueurs typiques |
|--------|-------------------|-------------------|
| LFI-NFP | Critique forte d'Israel | genocide, apartheid, blocus, cessez-le-feu |
| GDR | Solidarite Palestine | droit international, occupation, colonisation |
| ECO-NFP | Pro-Palestine modere | aide humanitaire, solution politique |
| PS-NFP | Solution 2 Etats | equilibre, paix, diplomatie |
| MODEM/EPR | Position officielle FR | moderation, otages, aide humanitaire |
| REN/Ensemble | Position gouvernementale | droit de se defendre, otages, antisemitisme |
| LR | Pro-Israel modere | securite, terrorisme, otages |
| RN | Variable | antisemitisme, securite, islamisme |

### Chronologie des evenements cles:
- 7 octobre 2023: Attaque Hamas, debut de l'offensive israelienne
- Novembre 2023: Pause humanitaire, echanges otages
- Janvier 2024: Proces CIJ (genocide)
- Mai 2024: Offensive Rafah
- Novembre 2024: Mandat CPI contre Netanyahu
- Janvier 2025: Accord de cessez-le-feu

### Indicateurs linguistiques par stance:

**Fortement pro-Palestine (stance=2):**
- Termes: genocide, nettoyage ethnique, apartheid, crime contre l'humanite
- Appels: BDS, sanctions, expulsion ambassadeur
- Critique: sionisme, colonisation, occupation illegale

**Pro-Palestine modere (stance=1):**
- Termes: droit international, cessez-le-feu, aide humanitaire Gaza
- Critique: gouvernement Netanyahu, colons, blocus
- Soutien: reconnaissance Etat palestinien, CIJ, CPI

**Neutre (stance=0):**
- Position equilibree explicite
- Condamnation des deux cotes
- Appel a la paix sans parti pris
- Questions procedurales

**Pro-Israel modere (stance=-1):**
- Termes: droit de se defendre, liberer les otages
- Nuance: critique Hamas, soutien population israelienne
- Focus: antisemitisme, securite

**Fortement pro-Israel (stance=-2):**
- Defense inconditionnelle actions militaires
- Termes: terrorisme Hamas, pogrom, barbarie
- Critique: LFI, antisionisme=antisemitisme
- Negation des victimes civiles palestiniennes
"""

# =============================================================================
# PROMPTS DIFFERENCIES PAR SOURCE
# =============================================================================

SYSTEM_PROMPT_TWEETS = """Tu es un expert en analyse du discours politique sur les reseaux sociaux, specialise dans le conflit israelo-palestinien.

{political_context}

## Specificites des TWEETS de deputes:

### Caracteristiques:
- Format court (<280 caracteres), souvent incomplet
- Ton plus personnel et emotionnel qu'en hemicycle
- Peut inclure RT, replies, threads
- Hashtags significatifs (#Gaza, #BringThemHome, #Ceasefire)
- Emojis peuvent indiquer le ton (drapeaux, coeurs)
- Contexte souvent implicite (actualite du jour)

### Points d'attention:
1. Un RT sans commentaire = endossement du contenu
2. Les hashtags sont des marqueurs forts de position
3. Le ton informel peut masquer une position forte
4. Les threads doivent etre lus comme un ensemble
5. Les replies peuvent etre defensives (accusations d'antisemitisme)

### Pieges courants:
- Ironie/sarcasme difficile a detecter
- Citations sans approbation
- Partage d'info factuelle ≠ position
"""

SYSTEM_PROMPT_INTERVENTIONS = """Tu es un expert en analyse du discours parlementaire francais, specialise dans le conflit israelo-palestinien.

{political_context}

## Specificites des INTERVENTIONS a l'Assemblee nationale:

### Caracteristiques:
- Discours formel, structure argumentative
- Contrainte institutionnelle (reglement, temps de parole)
- Peut etre une question au gouvernement, un debat, une explication de vote
- Langage diplomatique, euphemismes
- Contexte explicite (seance, ordre du jour)

### Points d'attention:
1. Le format (QAG, motion, debat) influence le ton
2. Les formules de politesse masquent parfois des critiques
3. Les references juridiques sont significatives (CIJ, CPI)
4. Les votes mentionnes sont des indicateurs forts
5. Les interruptions/reactions notees peuvent etre significatives

### Pieges courants:
- Langage diplomatique ≠ neutralite
- Citation gouvernement ≠ approbation
- Question rhetorique = position deguisee
- "Equilibre" affiche peut masquer un biais
"""

# =============================================================================
# FEW-SHOT EXAMPLES
# =============================================================================

FEW_SHOT_TWEETS = """
## Exemples d'annotation de TWEETS

### Exemple 1: Fortement pro-Palestine (stance=2)
TWEET: "Le genocide en cours a Gaza doit cesser. 40 000 morts. La communaute internationale est complice. #StopGenocide #Ceasefire"
AUTEUR: @JLMelenchon | GROUPE: LFI-NFP
ANALYSE:
- Utilisation explicite de "genocide" (qualification juridique maximale)
- Chiffre des victimes pour impact emotionnel
- "complice" = accusation forte de la communaute internationale
- Hashtags militants #StopGenocide
STANCE: 2 | INTENSITE: strong | CONFIANCE: 0.95
FRAME: HUM+LEG | TARGET: INTERNATIONAL

### Exemple 2: Pro-Palestine modere (stance=1)
TWEET: "Le droit international doit s'appliquer. La CIJ a parle. Cessez-le-feu maintenant et aide humanitaire pour Gaza."
AUTEUR: @deputePS | GROUPE: PS-NFP
ANALYSE:
- Reference au droit international (cadrage juridique)
- Mention CIJ = legitimation juridique
- Demande cessez-le-feu (position palestinienne)
- Pas de terme extreme comme "genocide"
STANCE: 1 | INTENSITE: moderate | CONFIANCE: 0.85
FRAME: LEG+HUM | TARGET: ISRAEL_GOV

### Exemple 3: Neutre (stance=0)
TWEET: "Rencontre avec l'ambassadeur d'Israel pour discuter de la situation au Proche-Orient et des voies vers la paix."
AUTEUR: @deputeMODEM | GROUPE: MODEM
ANALYSE:
- Compte-rendu factuel d'activite
- "voies vers la paix" = formulation diplomatique neutre
- Pas de jugement sur le conflit
STANCE: 0 | INTENSITE: weak | CONFIANCE: 0.90
FRAME: DIP | TARGET: None

### Exemple 4: Pro-Israel modere (stance=-1)
TWEET: "Pensees pour les familles des otages. La France doit agir pour leur liberation. #BringThemHome"
AUTEUR: @deputeREN | GROUPE: REN
ANALYSE:
- Focus exclusif sur les otages israeliens
- Hashtag #BringThemHome = campagne pro-Israel
- Pas de mention des victimes palestiniennes
- "Liberation" implique action contre Hamas
STANCE: -1 | INTENSITE: moderate | CONFIANCE: 0.80
FRAME: HUM | TARGET: HAMAS

### Exemple 5: Fortement pro-Israel (stance=-2)
TWEET: "Le 7 octobre est un pogrom. Ceux qui refusent de le dire sont complices. L'antisionisme est le nouvel antisemitisme."
AUTEUR: @deputeLR | GROUPE: LR
ANALYSE:
- "pogrom" = cadrage historique fort
- "complices" = accusation de ceux qui nuancent
- Equation antisionisme=antisemitisme
- Aucune mention du contexte ou des victimes palestiniennes
STANCE: -2 | INTENSITE: strong | CONFIANCE: 0.90
FRAME: HIS+MOR | TARGET: PALESTINE_GOV
"""

FEW_SHOT_INTERVENTIONS = """
## Exemples d'annotation d'INTERVENTIONS PARLEMENTAIRES

### Exemple 1: Fortement pro-Palestine (stance=2)
INTERVENTION: "Monsieur le ministre, apres 6 mois de bombardements, 35 000 morts dont 14 000 enfants, la Cour internationale de Justice evoque un risque plausible de genocide. Quand la France votera-t-elle des sanctions contre le gouvernement Netanyahu?"
AUTEUR: Depute LFI | SEANCE: QAG
ANALYSE:
- Enumeration detaillee des victimes (cadrage humanitaire)
- Reference CIJ = legitimation juridique
- Demande de sanctions = action concrete contre Israel
- Question rhetorique = position deguisee
STANCE: 2 | INTENSITE: strong | CONFIANCE: 0.95
FRAME: HUM+LEG | TARGET: ISRAEL_GOV, FRANCE

### Exemple 2: Pro-Palestine modere (stance=1)
INTERVENTION: "La France doit reconnaitre l'Etat de Palestine. C'est une question de coherence avec notre attachement au droit international et a la solution a deux Etats."
AUTEUR: Depute PS | SEANCE: Debat
ANALYSE:
- Demande reconnaissance Palestine (position pro-palestinienne)
- Reference droit international
- Solution 2 Etats = cadre diplomatique accepte
- Ton modere, argumentaire juridique
STANCE: 1 | INTENSITE: moderate | CONFIANCE: 0.85
FRAME: DIP+LEG | TARGET: FRANCE

### Exemple 3: Neutre officiel (stance=0)
INTERVENTION: "La France condamne les attaques terroristes du Hamas et appelle Israel a respecter le droit international humanitaire. Nous soutenons une solution a deux Etats."
AUTEUR: Ministre AE | SEANCE: QAG
ANALYSE:
- Condamnation equilibree des deux cotes
- Position officielle gouvernementale
- "Respecter le DIH" = critique implicite mais mesuree
STANCE: 0 | INTENSITE: moderate | CONFIANCE: 0.85
FRAME: DIP | TARGET: None

### Exemple 4: Pro-Israel modere (stance=-1)
INTERVENTION: "Je rappelle que 240 otages ont ete enleves le 7 octobre, dont des citoyens francais. Israel a le droit de se defendre contre le terrorisme."
AUTEUR: Depute REN | SEANCE: QAG
ANALYSE:
- Focus sur les otages
- "droit de se defendre" = formule pro-Israel standard
- Qualification "terrorisme" pour Hamas
- Pas de mention des victimes palestiniennes
STANCE: -1 | INTENSITE: moderate | CONFIANCE: 0.85
FRAME: SEC | TARGET: HAMAS

### Exemple 5: Fortement pro-Israel (stance=-2)
INTERVENTION: "Ceux qui manifestent avec des drapeaux palestiniens soutiennent objectivement le Hamas. L'antisemitisme se repand dans notre pays sous couvert d'antisionisme."
AUTEUR: Depute RN | SEANCE: Debat
ANALYSE:
- Amalgame manifestants pro-Palestine = pro-Hamas
- Equation antisionisme = antisemitisme
- Aucune reconnaissance de la cause palestinienne
- Cadrage securitaire/moral
STANCE: -2 | INTENSITE: strong | CONFIANCE: 0.90
FRAME: SEC+MOR | TARGET: PALESTINE_PEOPLE
"""

# =============================================================================
# USER PROMPT TEMPLATE
# =============================================================================

USER_PROMPT_TEMPLATE = """Analyse ce texte selon le schema d'annotation academique.

---
TYPE: {source_type}
TEXTE: {text}
AUTEUR: {author}
GROUPE POLITIQUE: {group}
DATE: {date}
PERIODE: {period}
CONTEXTE ADDITIONNEL: {context}
---

## Instructions d'analyse en etapes

### Etape 1: Pertinence
Le texte traite-t-il du conflit Gaza/Palestine/Israel?
- Si hors sujet → is_off_topic: true, arreter

### Etape 2: Identification des elements
- Mots-cles et expressions significatifs
- Entites mentionnees (Israel, Palestine, Hamas, Netanyahu, etc.)
- Type de cadrage (humanitaire, securitaire, juridique, etc.)

### Etape 3: Analyse de la position
- Quelle est l'INTENTION rhetorique?
- Y a-t-il une asymetrie dans le traitement?
- Le groupe politique est un INDICE, pas un determinant

### Etape 4: Classification sur echelle 5 points
- -2: Fortement pro-Israel (defense inconditionnelle, negation victimes palestiniennes)
- -1: Pro-Israel modere (focus otages/securite, critique Hamas)
- 0: Neutre (equilibre explicite, pas de position claire)
- 1: Pro-Palestine modere (critique Israel, soutien humanitaire Gaza)
- 2: Fortement pro-Palestine (genocide, sanctions, BDS)

### Etape 5: Evaluation intensite et confiance
- Intensite: "strong" (position explicite), "moderate" (position claire), "weak" (implicite)
- Confiance: 0.9+ (sans ambiguite), 0.7-0.9 (claire), 0.5-0.7 (ambigue)

## Format de reponse (JSON strict)

```json
{{
    "is_off_topic": boolean,
    "is_ambiguous": boolean,
    "has_both_sides": boolean,
    "stance": -2|-1|0|1|2,
    "intensity": "strong"|"moderate"|"weak",
    "confidence": 0.0-1.0,
    "primary_target": "ISRAEL_GOV"|"ISRAEL_PEOPLE"|"PALESTINE_GOV"|"PALESTINE_PEOPLE"|"HAMAS"|"NETANYAHU"|"INTERNATIONAL"|"FRANCE"|null,
    "secondary_target": string|null,
    "primary_frame": "HUM"|"SEC"|"LEG"|"DIP"|"MOR"|"HIS"|"ECO"|null,
    "secondary_frame": string|null,
    "key_indicators": ["mot1", "mot2", ...],
    "rhetorical_strategy": "description courte de la strategie",
    "reasoning": "Analyse detaillee en 3-4 phrases justifiant la classification"
}}
```

IMPORTANT: Reponds UNIQUEMENT avec le JSON, sans texte avant ou apres.
"""


# =============================================================================
# FONCTION D'ANNOTATION
# =============================================================================

def annotate_text_v3(
    text: str,
    source_type: str = "tweet",  # "tweet" ou "intervention"
    author: str = "Unknown",
    group: str = "Unknown",
    date: str = "Unknown",
    period: str = "Unknown",
    context: str = "",
    model: str = "gpt-4o-mini",
    max_retries: int = 3
) -> AnnotationResultV3:
    """Annotate a single text with V3 schema."""
    
    # Select appropriate system prompt
    if source_type.lower() in ["intervention", "an", "assemblee", "parlementaire"]:
        system_content = SYSTEM_PROMPT_INTERVENTIONS.format(political_context=POLITICAL_CONTEXT)
        system_content += "\n\n" + FEW_SHOT_INTERVENTIONS
    else:
        system_content = SYSTEM_PROMPT_TWEETS.format(political_context=POLITICAL_CONTEXT)
        system_content += "\n\n" + FEW_SHOT_TWEETS
    
    user_prompt = USER_PROMPT_TEMPLATE.format(
        source_type=source_type,
        text=text[:2500],  # Truncate very long texts
        author=author,
        group=group,
        date=date,
        period=period,
        context=context if context else "Aucun contexte additionnel"
    )
    
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_content},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.05,  # Very low for consistency
                max_tokens=800,
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            
            return AnnotationResultV3(
                stance=result.get("stance", 0),
                intensity=result.get("intensity", "moderate"),
                confidence=result.get("confidence", 0.5),
                primary_target=result.get("primary_target"),
                secondary_target=result.get("secondary_target"),
                primary_frame=result.get("primary_frame"),
                secondary_frame=result.get("secondary_frame"),
                is_off_topic=result.get("is_off_topic", False),
                is_ambiguous=result.get("is_ambiguous", False),
                has_both_sides=result.get("has_both_sides", False),
                reasoning=result.get("reasoning", ""),
                key_indicators=result.get("key_indicators", []),
                rhetorical_strategy=result.get("rhetorical_strategy", "")
            )
            
        except json.JSONDecodeError as e:
            if attempt < max_retries - 1:
                time.sleep(1)
                continue
            return AnnotationResultV3(
                stance=0, intensity="weak", confidence=0.0,
                primary_target=None, secondary_target=None,
                primary_frame=None, secondary_frame=None,
                is_off_topic=False, is_ambiguous=True, has_both_sides=False,
                reasoning=f"JSON parse error: {e}",
                key_indicators=[], rhetorical_strategy="error"
            )
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(2)
                continue
            return AnnotationResultV3(
                stance=0, intensity="weak", confidence=0.0,
                primary_target=None, secondary_target=None,
                primary_frame=None, secondary_frame=None,
                is_off_topic=False, is_ambiguous=True, has_both_sides=False,
                reasoning=f"API error: {e}",
                key_indicators=[], rhetorical_strategy="error"
            )


def annotate_corpus_v3(
    df: pd.DataFrame,
    source_type: str,
    text_col: str = "TEXTE",
    author_col: str = "AUTEUR",
    group_col: str = "GROUPE",
    date_col: str = "DATE",
    period_col: str = "PERIODE",
    context_col: str = None,
    model: str = "gpt-4o-mini",
    batch_size: int = 50,
    save_interval: int = 100,
    output_path: Path = None,
    progress_callback=None
) -> pd.DataFrame:
    """Annotate a full corpus with checkpointing."""
    
    results = []
    total = len(df)
    
    for idx, row in df.iterrows():
        context = ""
        if context_col and context_col in df.columns:
            context = str(row.get(context_col, ""))
        
        result = annotate_text_v3(
            text=str(row.get(text_col, "")),
            source_type=source_type,
            author=str(row.get(author_col, "Unknown")),
            group=str(row.get(group_col, "Unknown")),
            date=str(row.get(date_col, "Unknown")),
            period=str(row.get(period_col, "Unknown")),
            context=context,
            model=model
        )
        
        result_dict = {
            "stance_v3": result.stance,
            "stance_3class_v3": result.stance_3class,
            "intensity_v3": result.intensity,
            "confidence_v3": result.confidence,
            "primary_target_v3": result.primary_target,
            "secondary_target_v3": result.secondary_target,
            "primary_frame_v3": result.primary_frame,
            "secondary_frame_v3": result.secondary_frame,
            "is_off_topic_v3": result.is_off_topic,
            "is_ambiguous_v3": result.is_ambiguous,
            "has_both_sides_v3": result.has_both_sides,
            "reasoning_v3": result.reasoning,
            "indicators_v3": json.dumps(result.key_indicators, ensure_ascii=False),
            "rhetorical_strategy_v3": result.rhetorical_strategy
        }
        results.append(result_dict)
        
        if progress_callback:
            progress_callback(idx + 1, total)
        
        # Checkpoint save
        if output_path and (idx + 1) % save_interval == 0:
            temp_df = pd.concat([
                df.iloc[:len(results)].reset_index(drop=True),
                pd.DataFrame(results)
            ], axis=1)
            temp_df.to_parquet(output_path.with_suffix('.checkpoint.parquet'), index=False)
        
        # Rate limiting
        time.sleep(0.3)
    
    result_df = pd.DataFrame(results)
    return pd.concat([df.reset_index(drop=True), result_df], axis=1)


# =============================================================================
# CLI
# =============================================================================

if __name__ == "__main__":
    from tqdm import tqdm
    import argparse
    
    parser = argparse.ArgumentParser(description="LLM Annotation V3 - Etat de l'art")
    parser.add_argument("--input", required=True, help="Input file (parquet/xlsx/csv)")
    parser.add_argument("--output", required=True, help="Output file")
    parser.add_argument("--source-type", required=True, choices=["tweet", "intervention"],
                        help="Type de source (tweet ou intervention)")
    parser.add_argument("--sample", type=int, default=None, help="Sample size")
    parser.add_argument("--model", default="gpt-4o-mini", help="OpenAI model")
    parser.add_argument("--text-col", default="TEXTE", help="Text column name")
    parser.add_argument("--author-col", default="AUTEUR", help="Author column name")
    parser.add_argument("--group-col", default="GROUPE", help="Group column name")
    
    args = parser.parse_args()
    
    # Load data
    input_path = Path(args.input)
    if input_path.suffix == ".xlsx":
        df = pd.read_excel(input_path)
    elif input_path.suffix == ".parquet":
        df = pd.read_parquet(input_path)
    else:
        df = pd.read_csv(input_path)
    
    print(f"=" * 60)
    print(f"ANNOTATION LLM V3 - ETAT DE L'ART")
    print(f"=" * 60)
    print(f"\nSource: {args.source_type.upper()}")
    print(f"Fichier: {input_path.name}")
    print(f"Lignes: {len(df)}")
    
    # Sample if requested
    if args.sample and args.sample < len(df):
        df = df.sample(args.sample, random_state=42)
        print(f"Echantillon: {len(df)} lignes")
    
    # Annotate with progress bar
    pbar = tqdm(total=len(df), desc=f"Annotation {args.source_type}")
    
    def update_progress(current, total):
        pbar.update(1)
    
    output_path = Path(args.output)
    result_df = annotate_corpus_v3(
        df,
        source_type=args.source_type,
        text_col=args.text_col,
        author_col=args.author_col,
        group_col=args.group_col,
        model=args.model,
        output_path=output_path,
        progress_callback=update_progress
    )
    
    pbar.close()
    
    # Save
    if output_path.suffix == ".xlsx":
        result_df.to_excel(output_path, index=False)
    elif output_path.suffix == ".parquet":
        result_df.to_parquet(output_path, index=False)
    else:
        result_df.to_csv(output_path, index=False)
    
    print(f"\nSauvegarde: {output_path}")
    
    # Statistics
    print(f"\n{'=' * 60}")
    print("STATISTIQUES")
    print(f"{'=' * 60}")
    
    print(f"\nHors sujet: {result_df['is_off_topic_v3'].sum()}")
    print(f"Ambigus: {result_df['is_ambiguous_v3'].sum()}")
    print(f"Mention deux cotes: {result_df['has_both_sides_v3'].sum()}")
    
    valid = result_df[~result_df['is_off_topic_v3']]
    print(f"\n--- Distribution stance (echelle 5) ---")
    print(valid['stance_v3'].value_counts().sort_index())
    
    print(f"\n--- Distribution stance (3 classes) ---")
    print(valid['stance_3class_v3'].value_counts().sort_index())
    
    print(f"\n--- Intensite ---")
    print(valid['intensity_v3'].value_counts())
    
    print(f"\n--- Cadrage principal ---")
    print(valid['primary_frame_v3'].value_counts())
    
    print(f"\n--- Cible principale ---")
    print(valid['primary_target_v3'].value_counts())
    
    print(f"\n--- Confiance ---")
    print(f"Moyenne: {valid['confidence_v3'].mean():.2f}")
    print(f"Mediane: {valid['confidence_v3'].median():.2f}")
