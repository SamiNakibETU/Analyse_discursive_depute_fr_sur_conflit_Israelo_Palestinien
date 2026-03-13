# Pistes NLP avancées

## Objectif

Prioriser les améliorations méthodologiques utiles pour une publication solide, sans diluer les acquis du pipeline actuel.

## Ce qui est déjà solide

- Triangulation de `stance_v3` (lexical, Wordfish/CA, PCA, LLM)
- Comparaisons lexicales distinctives (log-odds)
- Suivi temporel des registres
- Comparaison d'arènes (Twitter vs AN)

## Limites actuelles

- Approche surtout bag-of-words / bag-of-ngrams
- Peu de modélisation contextuelle du sens
- Peu d'outils pour la structure argumentative
- Validation humaine encore limitée pour un étalon-or strict

## Priorités recommandées

### 1. Validation humaine (priorité immédiate)

Pourquoi:
- Renforce la crédibilité externe des annotations.
- Permet des métriques standard (accord inter-annotateurs, F1, erreurs de classe).

Version faisable maintenant:
- Échantillon stratifié 200-300 textes.
- Double annotation humaine.
- Rapport d'accord + erreurs récurrentes.

### 2. Embeddings contextuels francophones

Pourquoi:
- Mieux capter le sens contextuel qu'un TF-IDF classique.

Version faisable maintenant:
- Encodage phrase-level.
- Distances sémantiques inter-blocs et trajectoires temporelles.

### 3. BERTopic / dynamique des thèmes

Pourquoi:
- Identifier des sous-thèmes non capturés par la taxonomie actuelle.

Version faisable maintenant:
- Modèle topic sur post-7 octobre.
- Suivi des topics dans le temps et par bloc.

### 4. Registres émotionnels fins

Pourquoi:
- Distinguer des textes proches en stance mais différents en tonalité émotionnelle.

Version faisable maintenant:
- Catégorisation émotionnelle fine.
- Comparaison bloc x arène x période.

## Priorités secondaires

- Semantic shift (très intéressant, plus coûteux techniquement)
- Argument mining (fort potentiel, forte complexité)
- Réseaux textuels/intertextualité (utile surtout pour un second papier)

## Garde-fous

- Chaque extension doit garder un protocole de validation simple et lisible.
- Aucune extension ne doit être présentée comme preuve causale en l'absence d'identification causale.
- Les améliorations doivent rester compatibles avec la base actuelle pour comparaison.
