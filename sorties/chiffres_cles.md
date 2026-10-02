# Chiffres clés

Fichier généré par `python -m analyse`. Ne pas modifier à la main.

Nature : `texte` = mesure sur le texte seul ; `extraction` = information factuelle extraite par le modèle ;
`jugement` = appréciation du modèle, exposée au biais partisan du prompt (docs/methodologie.md, §4).

| Clé | Valeur | Libellé | Nature | Source |
|---|---:|---|---|---|
| `auteurs_bruts` | 501 | Auteurs distincts dans les tables d'origine | texte | trajectoires_individuelles.csv |
| `personnes` | 332 | Personnes réelles après fusion des doublons de civilité | texte | trajectoires_individuelles.csv |
| `doublons` | 135 | Personnes présentes sous plusieurs graphies | texte | trajectoires_individuelles.csv |
| `variables_degenerees` | 7 | Variables v4 à 100 % dans tous les blocs (inutilisables) | extraction | variables_batch_specifiques.csv |
| `rtm_rho` | -0,392 | Corrélation écart initial au bloc / changement individuel (régression vers la moyenne) | jugement | movers_caches.csv |
| `rtm_p` | 9.2e-07 | p-valeur associée | jugement | movers_caches.csv |
| `cosinus_correlation_chaines` | 0,789 | Corrélation des deux mesures de distance cosinus (toutes paires, tous mois) | texte | cosine_distance_mensuelle.csv |
| `eta2_bloc` | 0,619 | η² partiel du bloc (position, 5 905 textes v4) | jugement | anova_type2.csv |
| `eta2_fenetre` | 0,028 | η² partiel de la fenêtre | jugement | anova_type2.csv |
| `eta2_arene` | 0,002 | η² partiel de l'arène | jugement | anova_type2.csv |
| `tau_Gauche radicale` | 0,130 | Écart-type réel mois à mois, Gauche radicale | jugement | stance_mensuel.csv |
| `moyenne_Gauche radicale` | 1,609 | Position moyenne pondérée, Gauche radicale | jugement | stance_mensuel.csv |
| `tau_Gauche moderee` | 0,263 | Écart-type réel mois à mois, Gauche modérée | jugement | stance_mensuel.csv |
| `moyenne_Gauche moderee` | 1,033 | Position moyenne pondérée, Gauche modérée | jugement | stance_mensuel.csv |
| `tau_Centre / Majorite` | 0,193 | Écart-type réel mois à mois, Centre / Majorité | jugement | stance_mensuel.csv |
| `moyenne_Centre / Majorite` | -0,804 | Position moyenne pondérée, Centre / Majorité | jugement | stance_mensuel.csv |
| `tau_Droite` | 0,152 | Écart-type réel mois à mois, Droite | jugement | stance_mensuel.csv |
| `moyenne_Droite` | -1,430 | Position moyenne pondérée, Droite | jugement | stance_mensuel.csv |
| `mois_complets` | 18 | Mois où chaque bloc a au moins 15 textes | jugement | stance_mensuel.csv |
| `ecart_moyen` | 2,913 | Écart moyen gauche radicale – droite (points sur 4) | jugement | stance_mensuel.csv |
| `ecart_min` | 2,408 | Écart minimal | jugement | stance_mensuel.csv |
| `ecart_max` | 3,251 | Écart maximal | jugement | stance_mensuel.csv |
| `ecart_tendance_p` | 0,709 | Tendance de l'écart (Kendall), p | jugement | stance_mensuel.csv |
| `lambda_moyen` | 0,200 | Position relative du Centre (0 = droite, 1 = gauche radicale) | jugement | stance_mensuel.csv |
| `lambda_tendance_tau` | 0,268 | Tendance de la position relative du Centre, τ | jugement | stance_mensuel.csv |
| `lambda_tendance_p` | 0,131 | Tendance de la position relative du Centre, p | jugement | stance_mensuel.csv |
| `gaza_mois_gauche` | 26 | Mois où « gaza » est un mot distinctif de la gauche | texte | fighting_words_temporal.csv |
| `hamas_mois_droite` | 27 | Mois où « hamas » est un mot distinctif de la droite | texte | fighting_words_temporal.csv |
| `mots_mois` | 27 | Mois couverts par la table | texte | fighting_words_temporal.csv |
| `signal_bruit` | 11,083 | Écart inter-blocs rapporté à la plus forte variation temporelle intra-bloc | jugement | stance_mensuel.csv |
| `attr_centre_choc` | -0,445 | Indice d'attribution du Centre, fenêtre du 7 octobre | extraction | target_primary_par_batch_bloc.csv |
| `attr_centre_fin` | 0,088 | Indice d'attribution du Centre, avril-juin 2025 | extraction | target_primary_par_batch_bloc.csv |
| `attr_gr_choc` | 0,731 | Indice d'attribution de la gauche radicale, fenêtre du 7 octobre | extraction | target_primary_par_batch_bloc.csv |
| `attr_gm_choc` | 0,474 | Indice d'attribution de la gauche modérée, fenêtre du 7 octobre | extraction | target_primary_par_batch_bloc.csv |
| `cf_z_Gauche radicale` | -16,858 | Tendance de l'appel au cessez-le-feu, Gauche radicale (z) | extraction | ceasefire_call_batch_bloc.csv |
| `cf_z_Gauche moderee` | -6,958 | Tendance de l'appel au cessez-le-feu, Gauche modérée (z) | extraction | ceasefire_call_batch_bloc.csv |
| `cf_z_Centre / Majorite` | 2,768 | Tendance de l'appel au cessez-le-feu, Centre / Majorité (z) | extraction | ceasefire_call_batch_bloc.csv |
| `cf_z_Droite` | -0,334 | Tendance de l'appel au cessez-le-feu, Droite (z) | extraction | ceasefire_call_batch_bloc.csv |
| `cflex_avant_Gauche radicale` | 0,192 | « cessez-le-feu » dans le texte, oct. 2023 – juin 2024, Gauche radicale | texte | ceasefire_lexical.csv |
| `cflex_apres_Gauche radicale` | 0,072 | « cessez-le-feu » dans le texte, juil. 2024 – janv. 2026, Gauche radicale | texte | ceasefire_lexical.csv |
| `cflex_z_Gauche radicale` | -16,746 | Tendance mensuelle, Gauche radicale (z) | texte | ceasefire_lexical.csv |
| `cflex_avant_Gauche moderee` | 0,193 | « cessez-le-feu » dans le texte, oct. 2023 – juin 2024, Gauche modérée | texte | ceasefire_lexical.csv |
| `cflex_apres_Gauche moderee` | 0,063 | « cessez-le-feu » dans le texte, juil. 2024 – janv. 2026, Gauche modérée | texte | ceasefire_lexical.csv |
| `cflex_z_Gauche moderee` | -6,660 | Tendance mensuelle, Gauche modérée (z) | texte | ceasefire_lexical.csv |
| `cflex_avant_Centre / Majorite` | 0,062 | « cessez-le-feu » dans le texte, oct. 2023 – juin 2024, Centre / Majorité | texte | ceasefire_lexical.csv |
| `cflex_apres_Centre / Majorite` | 0,090 | « cessez-le-feu » dans le texte, juil. 2024 – janv. 2026, Centre / Majorité | texte | ceasefire_lexical.csv |
| `cflex_z_Centre / Majorite` | 1,743 | Tendance mensuelle, Centre / Majorité (z) | texte | ceasefire_lexical.csv |
| `cflex_avant_Droite` | 0,019 | « cessez-le-feu » dans le texte, oct. 2023 – juin 2024, Droite | texte | ceasefire_lexical.csv |
| `cflex_apres_Droite` | 0,013 | « cessez-le-feu » dans le texte, juil. 2024 – janv. 2026, Droite | texte | ceasefire_lexical.csv |
| `cflex_z_Droite` | -1,577 | Tendance mensuelle, Droite (z) | texte | ceasefire_lexical.csv |
| `sans_demande_Gauche radicale` | 0,476 | Part des textes sans demande, Gauche radicale | extraction | key_demands_par_batch_bloc.csv |
| `sans_demande_Gauche moderee` | 0,398 | Part des textes sans demande, Gauche modérée | extraction | key_demands_par_batch_bloc.csv |
| `sans_demande_Centre / Majorite` | 0,701 | Part des textes sans demande, Centre / Majorité | extraction | key_demands_par_batch_bloc.csv |
| `sans_demande_Droite` | 0,891 | Part des textes sans demande, Droite | extraction | key_demands_par_batch_bloc.csv |
| `js_cadre_gr_droite` | 0,470 | Divergence gauche radicale / droite sur la définition du problème | jugement | frames_par_bloc.csv |
| `part_gr_debut` | 0,477 | Part de la gauche radicale, octobre 2023 | texte | volume_mensuel.csv |
| `part_gr_fin` | 0,849 | Part de la gauche radicale, janvier 2026 | texte | volume_mensuel.csv |
| `part_gr_p` | 0,030 | Tendance de la part de la gauche radicale, p | texte | volume_mensuel.csv |
| `neb_debut` | 3,079 | Nombre effectif de blocs, octobre 2023 | texte | volume_mensuel.csv |
| `neb_fin` | 1,367 | Nombre effectif de blocs, janvier 2026 | texte | volume_mensuel.csv |
| `neb_p` | 0,034 | Tendance du nombre effectif de blocs, p | texte | volume_mensuel.csv |
| `volume_oct23` | 1353 | Textes en octobre 2023 | texte | volume_mensuel.csv |
| `volume_mediane` | 319 | Médiane mensuelle des textes après octobre 2023 | texte | volume_mensuel.csv |
| `gini` | 0,766 | Indice de Gini de la production par personne | texte | trajectoires_individuelles.csv |
| `mediane_textes` | 6 | Textes par personne (médiane, 28 mois) | texte | trajectoires_individuelles.csv |
| `top10` | 0,332 | Part du corpus produite par les 10 premiers | texte | trajectoires_individuelles.csv |
| `top20` | 0,486 | Part du corpus produite par les 20 premiers | texte | trajectoires_individuelles.csv |
| `au_plus_5` | 163 | Personnes ayant produit 5 textes ou moins | texte | trajectoires_individuelles.csv |
| `part_personnes_gr` | 0,274 | Part des personnes appartenant à la gauche radicale | texte | trajectoires_individuelles.csv |
| `part_textes_gr` | 0,623 | Part des textes produits par la gauche radicale | texte | trajectoires_individuelles.csv |
| `droite_dom_z` | 4,386 | Droite : tendance des cibles intérieures sur les sept fenêtres (z) | extraction | target_primary_par_batch_bloc.csv |
| `droite_dom_tendance_p` | 1.2e-05 | p-valeur | extraction | target_primary_par_batch_bloc.csv |
| `droite_choc` | 0,167 | Droite : part des cibles intérieures, 7 oct. – 15 nov. 2023 | extraction | target_primary_par_batch_bloc.csv |
| `droite_fin` | 0,341 | Droite : part des cibles intérieures, avril-juin 2025 | extraction | target_primary_par_batch_bloc.csv |
| `droite_rafah` | 0,448 | Droite : part des cibles intérieures, 1er mai – 15 juin 2024 | extraction | target_primary_par_batch_bloc.csv |
| `droite_rafah_n` | 67 | Droite : textes de la fenêtre | extraction | target_primary_par_batch_bloc.csv |
| `droite_autres` | 0,243 | Droite : part des cibles intérieures, autres fenêtres | extraction | target_primary_par_batch_bloc.csv |
| `droite_rafah_p` | 4.7e-04 | Test khi², p | extraction | target_primary_par_batch_bloc.csv |
| `interieur_Gauche radicale` | 0,163 | Part des cibles intérieures, Gauche radicale | extraction | target_primary_par_batch_bloc.csv |
| `adversaires_Gauche radicale` | 0,030 | Part des cibles visant un adversaire partisan, Gauche radicale | extraction | target_primary_par_batch_bloc.csv |
| `interieur_Gauche moderee` | 0,142 | Part des cibles intérieures, Gauche modérée | extraction | target_primary_par_batch_bloc.csv |
| `adversaires_Gauche moderee` | 0,016 | Part des cibles visant un adversaire partisan, Gauche modérée | extraction | target_primary_par_batch_bloc.csv |
| `interieur_Centre / Majorite` | 0,130 | Part des cibles intérieures, Centre / Majorité | extraction | target_primary_par_batch_bloc.csv |
| `adversaires_Centre / Majorite` | 0,092 | Part des cibles visant un adversaire partisan, Centre / Majorité | extraction | target_primary_par_batch_bloc.csv |
| `interieur_Droite` | 0,261 | Part des cibles intérieures, Droite | extraction | target_primary_par_batch_bloc.csv |
| `adversaires_Droite` | 0,198 | Part des cibles visant un adversaire partisan, Droite | extraction | target_primary_par_batch_bloc.csv |
| `lfi_mois_negatifs` | 23 | Mois où « lfi » est un mot distinctif de la droite | texte | fighting_words_temporal.csv |
| `lfi_mois_total` | 23 | Mois où « lfi » apparaît dans la table | texte | fighting_words_temporal.csv |
| `lfi_min_mois` | 2024-05 | Mois du score le plus marqué | texte | fighting_words_temporal.csv |
| `an_avant` | 123 | Interventions sur le conflit, juillet 2022 – 6 octobre 2023 | texte | data/an_2022_2024 |
| `an_debat_4mai` | 79 | dont débat du 4 mai 2023 (résolution n° 1082) | texte | data/an_2022_2024 |
| `an_avant_par_mois_hors_debat` | 3,143 | Par mois de séance, hors 4 mai 2023 | texte | data/an_2022_2024 |
| `an_apres` | 757 | Interventions sur le conflit, 7 octobre 2023 – juin 2024 | texte | data/an_2022_2024 |
| `an_apres_par_mois` | 84,111 | Par mois de séance | texte | data/an_2022_2024 |
| `mois_avant` | 14 | Mois de séance avant | texte | data/an_2022_2024 |
| `mois_apres` | 9 | Mois de séance après | texte | data/an_2022_2024 |
| `orateurs_avant` | 42 | Députés intervenant sur le conflit avant le 7 octobre | texte | data/an_2022_2024 |
| `orateurs_apres` | 154 | Députés intervenant sur le conflit après (jusqu'en juin 2024) | texte | data/an_2022_2024 |
| `orateurs_communs` | 23 | Présents dans les deux périodes | texte | data/an_2022_2024 |
| `part_corpus_orateurs_avant` | 0,181 | Part du corpus 2023-2026 produite par des orateurs d'avant le 7 octobre | texte | data/an_2022_2024 + trajectoires_individuelles.csv |
| `top20_deja_presents` | 4 | Parmi les 20 premiers producteurs, déjà orateurs avant | texte | data/an_2022_2024 + trajectoires_individuelles.csv |
| `mots_avant` | 22 508 | Mots des interventions sur le conflit, avant | texte | data/an_2022_2024 |
| `mots_apres` | 106 762 | Mots des interventions sur le conflit, après | texte | data/an_2022_2024 |
| `lex_avant_apartheid` | 31,100 | « apartheid » pour 10 000 mots, avant | texte | data/an_2022_2024 |
| `lex_apres_apartheid` | 1,030 | « apartheid » pour 10 000 mots, après | texte | data/an_2022_2024 |
| `lex_avant_terrorisme, terroriste` | 10,663 | « terrorisme, terroriste » pour 10 000 mots, avant | texte | data/an_2022_2024 |
| `lex_apres_terrorisme, terroriste` | 33,533 | « terrorisme, terroriste » pour 10 000 mots, après | texte | data/an_2022_2024 |
| `lex_avant_otage(s)` | 1,333 | « otage(s) » pour 10 000 mots, avant | texte | data/an_2022_2024 |
| `lex_apres_otage(s)` | 12,551 | « otage(s) » pour 10 000 mots, après | texte | data/an_2022_2024 |
| `lex_avant_humanitaire` | 1,777 | « humanitaire » pour 10 000 mots, avant | texte | data/an_2022_2024 |
| `lex_apres_humanitaire` | 17,422 | « humanitaire » pour 10 000 mots, après | texte | data/an_2022_2024 |
| `lex_avant_cessez-le-feu` | 0 | « cessez-le-feu » pour 10 000 mots, avant | texte | data/an_2022_2024 |
| `lex_apres_cessez-le-feu` | 9,648 | « cessez-le-feu » pour 10 000 mots, après | texte | data/an_2022_2024 |
| `lex_avant_antisémitisme, antisémite` | 19,993 | « antisémitisme, antisémite » pour 10 000 mots, avant | texte | data/an_2022_2024 |
| `lex_apres_antisémitisme, antisémite` | 13,863 | « antisémitisme, antisémite » pour 10 000 mots, après | texte | data/an_2022_2024 |
| `arene_coef` | -0,023 | Effet de l'arène X sur la position (bloc et mois contrôlés) | jugement | twitter_vs_an.csv |
| `arene_p` | 0,336 | p-valeur | jugement | twitter_vs_an.csv |
| `gr_ecart_x_an` | 0,504 | Gauche radicale : écart X – séance (député-mois) | jugement | regression_delta_stance.csv |
| `gr_ecart_x_an_p` | 0,011 | p-valeur | jugement | regression_delta_stance.csv |
