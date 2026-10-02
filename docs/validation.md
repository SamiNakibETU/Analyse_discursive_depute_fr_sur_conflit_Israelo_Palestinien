# Validation humaine

## Ce qui existait

Un échantillon de 149 textes stratifié par bloc, arène et fenêtre (`data/validation/echantillon.csv`). Le fichier censé contenir les annotations humaines donnait un accord parfait avec le modèle (kappa = 1,000, 100 % d'accord exact, aucun écart dans aucun bloc). Sa distribution reproduit exactement celle des étiquettes du modèle (8, 39, 5, 25, 72 textes de −2 à +2). Il s'agissait des étiquettes du modèle, pas d'une annotation humaine. Le fichier a été renommé `etiquettes_llm_v3.csv` et ce résultat n'est plus cité.

## Ce qu'il faut faire

La validation n'a pas encore eu lieu. Elle est indispensable avant toute publication qui s'appuie sur la variable de position.

1. Générer la grille : `python -m analyse.validation grille`. Le fichier `data/validation/grille_annotation.csv` contient les 149 textes dans un ordre aléatoire, avec la date et l'arène, sans l'auteur ni le bloc.
2. Lire `docs/codebook.md`, puis remplir la colonne `position_humaine` (−2 à +2) sans ouvrir `etiquettes_llm_v3.csv`. Compter deux à trois heures.
3. Idéalement, faire annoter la même grille par une seconde personne pour mesurer l'accord entre humains, qui sert de plafond.
4. Calculer les scores : `python -m analyse.validation scores`.

## Ce que la validation mesure

Le modèle connaissait le groupe de l'auteur ; l'annotateur humain ne le connaît pas. L'écart moyen entre modèle et humain, calculé bloc par bloc, mesure donc directement le biais de conformité partisane : s'il est positif pour la gauche radicale et négatif pour la droite, le modèle a poussé les textes vers la position attendue de leur camp.

Seuils usuels pour le kappa pondéré quadratique : au-dessus de 0,6, accord substantiel ; au-dessus de 0,8, accord presque parfait.
