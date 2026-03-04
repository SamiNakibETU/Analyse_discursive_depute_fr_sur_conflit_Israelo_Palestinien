# Résultats numériques — Analyse discours Gaza

Export exhaustif des données chiffrées et séries temporelles produites par `run_analysis.py`.
Équivalent des sorties numériques des notebooks 01 à 13.

---

## Synthèse — Métriques et logs (run_analysis)

```
RAPPORT DES RÉSULTATS — ANALYSE DISCOURS GAZA
============================================================
Corpus : 10,774 textes, 459 députés

============================================================
01 — PORTRAIT DU CORPUS
============================================================

Volume mensuel : 28 mois
  Gauche radicale: total 6838 textes
  Gauche moderee: total 971 textes
  Centre / Majorite: total 1489 textes
  Droite: total 1476 textes

Biais d'activité Twitter (tweets/député) :
  Centre / Majorite: 16.86
  Droite: 19.83
  Gauche moderee: 35.39
  Gauche radicale: 122.10

Paradoxe visibilité (quintiles) : mean_abs_stance par quintile
 quintile  mean_abs_stance  n
        0         1.000101 38
        1         1.103759 37
        2         1.008361 38
        3         1.218378 37
        4         1.567298 38

Attrition : députés actifs min=34, max=211

Volume par groupe : 16 groupes

Stance moyen par bloc (violin) :
  Gauche radicale: mean=1.574, n=6838
  Gauche moderee: mean=0.926, n=971
  Centre / Majorite: mean=-0.769, n=1489
  Droite: mean=-1.378, n=1476

============================================================
02 — VALIDATION ANNOTATION
============================================================

Matrice confusion stance_v3 vs stance_v4 :
stance_v4   -2   -1   0    1     2 
stance_v3                          
-2         511   58   79    6    17
-1         387  253  340   29     5
 0           2   12  299   23     0
 1           4   16  494  550    89
 2           7    9  102  589  2024

Panel B4 vs complet :
             bloc  stance_complet  stance_panel_b4  n_complet  n_panel     delta
  Gauche radicale        1.574144         1.632727       6838     5549  0.058582
   Gauche moderee        0.925850         0.965174        971      402  0.039324
Centre / Majorite       -0.768972        -1.157895       1489      475 -0.388922
           Droite       -1.378049        -1.543326       1476      427 -0.165277

Validation lexical vs annotation :
  Spearman ρ = 0.5941
  Pearson r = 0.6178
  Accord de signe = 73.5 %

============================================================
03 — DYNAMIQUES TEMPORELLES
============================================================

Stance mensuel (extrait) :
  month              bloc  stance_v3   month_ts
2023-10 Centre / Majorite  -0.898039 2023-10-01
2023-10            Droite  -1.446667 2023-10-01
2023-10    Gauche moderee   0.647059 2023-10-01
2023-10   Gauche radicale   1.265116 2023-10-01
2023-11 Centre / Majorite  -0.813084 2023-11-01
2023-11            Droite  -1.186916 2023-11-01
2023-11    Gauche moderee   0.654545 2023-11-01
2023-11   Gauche radicale   1.373494 2023-11-01
2023-12 Centre / Majorite  -0.200000 2023-12-01
2023-12            Droite  -1.125000 2023-12-01
2023-12    Gauche moderee   0.875000 2023-12-01
2023-12   Gauche radicale   1.490446 2023-12-01
2024-01 Centre / Majorite  -0.812500 2024-01-01
2024-01            Droite  -1.375000 2024-01-01
2024-01    Gauche moderee   1.266667 2024-01-01
2024-01   Gauche radicale   1.730088 2024-01-01

Diff-in-diff (impact événements) :
     event              bloc     delta        p
2024-01-26   Gauche radicale -0.047706 0.448326
2024-01-26    Gauche moderee  0.325052 0.083127
2024-01-26 Centre / Majorite -0.103226 0.338858
2024-01-26            Droite  0.185578 0.400074
2024-05-07   Gauche radicale  0.121502 0.001581
2024-05-07    Gauche moderee  0.518041 0.001195
2024-05-07 Centre / Majorite  0.301405 0.030603
2024-05-07            Droite -0.221923 0.072379
2025-01-15   Gauche radicale -0.163309 0.036686
2025-01-15    Gauche moderee -0.333333 0.283737
2025-01-15 Centre / Majorite -0.587774 0.008392
2025-01-15            Droite -1.028571 0.007556

Wasserstein inter-blocs (moyenne par mois) :
month
2023-10    0.403352
2023-11    0.382457
2023-12    0.378092
2024-01    0.475505
2024-02    0.452570
2024-03    0.493231
2024-04    0.428163
2024-05    0.482767
2024-06    0.443645
2024-07    0.490182
2024-08    0.453165
2024-09    0.463587
2024-10    0.433933
2024-11    0.445793
2024-12    0.418608
2025-01    0.355844
2025-02    0.442595
2025-03    0.432398
2025-04    0.459011
2025-05    0.440173
2025-06    0.439036
2025-07    0.485904
2025-08    0.531474
2025-09    0.427634
2025-10    0.389249
2025-11    0.441045
2025-12    0.413405
2026-01    0.488870

Mann-Kendall (tendance temporelle) :
             bloc       tau        p
  Gauche radicale  0.190476 0.162095
   Gauche moderee -0.190982 0.154729
Centre / Majorite  0.089947 0.517918
           Droite -0.113907 0.395494

Intensité délibérative (% conflictuel) :
bloc
Centre / Majorite    0.106193
Droite               0.083339
Gauche moderee       0.138209
Gauche radicale      0.116906

Registre discursif vs stance (Spearman) :
  rho = 0.0456, p = 2.1358e-06
  Interprétation : limitation (rho<0.1)

============================================================
04 — POLARISATION LEXICALE
============================================================

Distance cosinus mensuelle (moyenne) :
month
2023-10    0.145901
2023-11    0.234503
2023-12    0.273685
2024-01    0.282132
2024-02    0.249556
2024-03    0.236350
2024-04    0.239450
2024-05    0.231017
2024-06    0.238387
2024-07    0.299902
2024-08    0.258117
2024-09    0.329276
2024-10    0.229364
2024-11    0.229711
2024-12    0.367378
2025-01    0.227875
2025-02    0.282792
2025-03    0.261980
2025-04    0.295637
2025-05    0.191389
2025-06    0.179386
2025-07    0.247812
2025-08    0.281346
2025-09    0.266327
2025-10    0.271240
2025-11    0.284162
2025-12    0.267597
2026-01    0.464279

Top 10 fighting words (gauche) :
        word         z
        gaza 25.541179
    génocide 20.950808
   palestine 15.302139
gouvernement 15.185767
   massacres 14.509774
      cessez 14.172268
         feu 13.942024
palestiniens 12.902029
  netanyahou 12.826532
       armée 12.715546

Top 10 fighting words (droite) :
         word          z
        hamas -34.858158
  terroristes -18.735412
       otages -18.404155
antisémitisme -18.391171
      octobre -18.347011
        haine -17.247662
        juifs -16.716947
          nos -16.676371
          lfi -15.658885
   terroriste -15.638375

Cessez-le-feu lexical (% par bloc, moyenne) :
bloc
Centre / Majorite     8.7%
Droite                1.4%
Gauche moderee       10.7%
Gauche radicale      11.3%

Polarisation entropique Ec (Bao & Gill) :
  Moyenne Ec globale : 0.7261
  Min/Max : 0.5082 / 0.9030

Effective Dimensionality :
  Moyenne ED : 2.8594
  Min/Max : 2.5595 / 2.9674

Polarisation affective (gap VAD moyen) :
  Moyenne gap : 0.0262

Fondements moraux (moyenne par bloc) :
                       care  fairness   loyalty  authority  sanctity
bloc                                                                
Centre / Majorite  0.179439  0.169538  0.194416   0.170982  0.160869
Droite             0.194723  0.188323  0.204639   0.181924  0.173194
Gauche moderee     0.198662  0.179442  0.210771   0.181155  0.170591
Gauche radicale    0.195465  0.183752  0.208386   0.183705  0.174165

Couverture MFD (% textes avec ≥1 hit par fondement) :
  care: 99.2%
  fairness: 99.3%
  loyalty: 99.4%
  authority: 99.2%
  sanctity: 99.1%

============================================================
05 — ÉVÉNEMENTS PIVOT
============================================================

Variables par batch :
                     n  stance_mean  stance_std
batch                                          
CHOC              1610     0.228571    1.486188
POST_CIJ           350     0.925714    1.400029
RAFAH              977     1.124872    1.309942
POST_SINWAR        237     0.894515    1.482043
MANDATS_CPI        309     1.187702    1.228865
CEASEFIRE_BREACH   751     0.589880    1.493847
NEW_OFFENSIVE     1671     0.865350    1.436626

Appel cessez-le-feu par batch/bloc :
bloc              Centre / Majorite    Droite  Gauche moderee  Gauche radicale
batch                                                                         
CEASEFIRE_BREACH           0.106061  0.000000        0.118644         0.121896
CHOC                       0.034843  0.005682        0.417582         0.366286
MANDATS_CPI                0.125000  0.111111        0.096774         0.057522
NEW_OFFENSIVE              0.113636  0.000000        0.123967         0.076357
POST_CIJ                   0.109091  0.031250        0.521739         0.350230
POST_SINWAR                0.151515  0.023256        0.000000         0.110390
RAFAH                      0.146154  0.042254        0.179245         0.159701

Régression ANOVA (type 2) :
                       sum_sq      df            F        PR(>F)
C(bloc)           7103.762303     3.0  3187.077581  0.000000e+00
C(batch)           123.879325     6.0    27.789008  6.696334e-33
C(arena)             8.860266     1.0    11.925380  5.576506e-04
C(bloc):C(batch)    49.163218    18.0     3.676150  2.211347e-07
Residual          4365.724423  5876.0          NaN           NaN

Coefficients (extrait) :
  Intercept: coef=-0.7859, p=0.0000
  C(bloc)[T.Droite]: coef=-0.6404, p=0.0000
  C(bloc)[T.Gauche moderee]: coef=1.5692, p=0.0000
  C(bloc)[T.Gauche radicale]: coef=2.1474, p=0.0000
  C(batch)[T.CHOC]: coef=-0.1706, p=0.0599
  C(batch)[T.MANDATS_CPI]: coef=-0.1866, p=0.4139
  C(batch)[T.NEW_OFFENSIVE]: coef=0.2264, p=0.0141
  C(batch)[T.POST_CIJ]: coef=-0.1405, p=0.3098

============================================================
06 — CONVERGENCE TRANSPARTISANE
============================================================

% convergence (|stance|≤1) par bloc :
  Gauche radicale: 25.9%
  Gauche moderee: 71.6%
  Centre / Majorite: 78.8%
  Droite: 50.9%

Movers (stance_initial=CHOC, stance_final=NEW_OFFENSIVE) :
bloc
Gauche radicale      58
Gauche moderee       18
Centre / Majorite    32
Droite               39
  Fort (|delta|>1.5): 9, Modere (|delta|>0.8): 18

PCA députés :
  Variance expliquée PC1: 8.72%
  Variance expliquée PC2: 2.75%
  Cumul 2 composantes: 11.47%

============================================================
07 — ÉMOTIONS ET REGISTRES
============================================================

Registre émotionnel par bloc :
emotional_register     anger   defense  defiance      fear     grief  indignation   neutral  solidarity
bloc                                                                                                   
Gauche radicale     0.041272  0.000000  0.008366  0.001673  0.073620     0.636642  0.113776    0.124651
Gauche moderee      0.010870  0.000000  0.001812  0.005435  0.177536     0.371377  0.298913    0.134058
Centre / Majorite   0.001091  0.002181  0.093784  0.032715  0.109051     0.267176  0.439477    0.054526
Droite              0.015294  0.000000  0.411765  0.037647  0.029412     0.364706  0.115294    0.025882

Frames par bloc :
primary_frame_v3        DIP       ECO       EDU       HIS       HUM   HUM+LEG       LEG       MOR       POL       SEC
bloc                                                                                                                 
Gauche radicale    0.017724  0.005273  0.000000  0.004834  0.772228  0.000146  0.095210  0.081295  0.000000  0.023290
Gauche moderee     0.059917  0.011364  0.000000  0.006198  0.640496  0.001033  0.154959  0.088843  0.000000  0.037190
Centre / Majorite  0.118952  0.004032  0.000672  0.029570  0.290995  0.000000  0.040323  0.209005  0.000672  0.305780
Droite             0.027119  0.012881  0.000000  0.044746  0.110508  0.000000  0.015593  0.341017  0.000000  0.448136

============================================================
08 — ANALYSES DE FOND
============================================================

Répartition par bloc :
  Gauche radicale: n=6838, 63.5%
  Gauche moderee: n=971, 9.0%
  Centre / Majorite: n=1489, 13.8%
  Droite: n=1476, 13.7%

Stance : complet vs sous-échantillonné (n_min) :
  Gauche radicale: complet=1.574, sous-échant.=1.593, écart=0.019
  Gauche moderee: complet=0.926, sous-échant.=0.926, écart=0.000
  Centre / Majorite: complet=-0.769, sous-échant.=-0.793, écart=-0.024
  Droite: complet=-1.378, sous-échant.=-1.396, écart=-0.018

============================================================
09 — ENGAGEMENT TWITTER
============================================================

log(1+engagement) moyen par bloc :
                   mean_log     n
bloc                             
Gauche radicale    5.539016  6227
Gauche moderee     4.615323   814
Centre / Majorite  4.308860   944
Droite             4.263186  1150

Corrélation |stance| ↔ log(engagement) : r = 0.245

============================================================
10 — TWITTER VS ASSEMBLÉE NATIONALE
============================================================

Députés actifs sur Twitter et AN : 127
Observations député-mois (les deux arènes) : 231

Régression delta stance (Twitter − AN) :
  Coefficients et p-values :
    Intercept: coef=0.0317, p=0.9058
    C(bloc)[T.Droite]: coef=-0.1516, p=0.5169
    C(bloc)[T.Gauche moderee]: coef=-0.4191, p=0.1320
    C(bloc)[T.Gauche radicale]: coef=0.5036, p=0.0108
    C(batch)[T.CHOC]: coef=0.1196, p=0.6560
    C(batch)[T.NEW_OFFENSIVE]: coef=-0.0456, p=0.8568
    C(batch)[T.OTHER]: coef=-0.3208, p=0.6426
    C(batch)[T.POST_CIJ]: coef=-0.0966, p=0.7590
    C(batch)[T.POST_SINWAR]: coef=-0.1685, p=0.6793
    C(batch)[T.RAFAH]: coef=-0.4574, p=0.1191
    n_tweets: coef=-0.0056, p=0.5007
    engagement_mean: coef=0.0003, p=0.1435

Fighting words Twitter vs AN (top par bloc, |z|>0.5) :
  Gauche radicale: [('vous', np.float64(-21.71), 'AN'), ('mêmes', np.float64(-13.64), 'AN'), ('monsieur', np.float64(-12.43), 'AN'), ('ministre', np.float64(-11.99), 'AN'), ('premier', np.float64(-10.54), 'AN')]
  Gauche moderee: [('vous', np.float64(-8.57), 'AN'), ('gaza', np.float64(7.93), 'Twitter'), ('ministre', np.float64(-6.47), 'AN'), ('palestine', np.float64(6.1), 'Twitter'), ('à', np.float64(5.62), 'Twitter')]
  Centre / Majorite: [('vous', np.float64(-9.05), 'AN'), ('ministre', np.float64(-6.29), 'AN'), ('hamas', np.float64(6.23), 'Twitter'), ('otages', np.float64(5.39), 'Twitter'), ('nous', np.float64(-4.89), 'AN')]
  Droite: [('hamas', np.float64(9.45), 'Twitter'), ('vous', np.float64(-8.49), 'AN'), ('que', np.float64(-7.22), 'AN'), ('du', np.float64(5.36), 'Twitter'), ('nous', np.float64(-5.21), 'AN')]

============================================================
LAG D'ADOPTION (cessez-le-feu lexical)
============================================================
Premier mois où chaque bloc dépasse 10 % de textes avec « cessez-le-feu » :
             bloc month_first_10pct      pct
Centre / Majorite           2023-12 0.300000
           Droite           2024-12 0.133333
   Gauche moderee           2023-10 0.202614
  Gauche radicale           2023-10 0.232558

============================================================
A3 — TENDANCES PRE-EVENEMENT (60j avant)
============================================================

Mann-Kendall tendance pre-evenement :
        event              bloc       tau     p_mk
Cessez-le-feu   Gauche radicale  0.101554 0.339405
  Mandats CPI   Gauche radicale -0.076196 0.429887
Cessez-le-feu    Gauche moderee -0.128355 0.449017
  Mandats CPI    Gauche moderee  0.017647 0.907381
Cessez-le-feu Centre / Majorite  0.055508 0.764990
  Mandats CPI Centre / Majorite  0.045406 0.718185
Cessez-le-feu            Droite  0.128386 0.433008
  Mandats CPI            Droite  0.109856 0.346026

============================================================
A4 — ROBUSTESSE CORPUS EQUILIBRE
============================================================

Tableau robustesse :
  Resultat | Corpus complet  | Corpus equilibre | Conclusion
  R1       | stable         | stable           | robuste
  R2       | Delta=-1.03 p=0.008 | Delta=-1.26 p=0.011 | robuste
  R4       | d_mean=0.306   | d_mean=0.339     | robuste
```

---


## 01 — Portrait du corpus

### volume_mensuel.csv (28 lignes)

| month | Gauche radicale | Gauche moderee | Centre / Majorite | Droite | month_ts |
| --- | --- | --- | --- | --- | --- |
| 2023-10 | 645 | 153 | 255 | 300 | 2023-10-01 |
| 2023-11 | 332 | 55 | 107 | 107 | 2023-11-01 |
| 2023-12 | 157 | 16 | 10 | 16 | 2023-12-01 |
| 2024-01 | 226 | 30 | 64 | 32 | 2024-01-01 |
| 2024-02 | 225 | 55 | 65 | 32 | 2024-02-01 |
| 2024-03 | 243 | 44 | 47 | 73 | 2024-03-01 |
| 2024-04 | 349 | 43 | 51 | 51 | 2024-04-01 |
| 2024-05 | 608 | 92 | 104 | 63 | 2024-05-01 |
| 2024-06 | 126 | 24 | 52 | 25 | 2024-06-01 |
| 2024-07 | 163 | 14 | 27 | 40 | 2024-07-01 |
| 2024-08 | 99 | 16 | 35 | 34 | 2024-08-01 |
| 2024-09 | 225 | 21 | 15 | 19 | 2024-09-01 |
| 2024-10 | 250 | 23 | 70 | 92 | 2024-10-01 |
| 2024-11 | 209 | 38 | 30 | 43 | 2024-11-01 |
| 2024-12 | 103 | 10 | 6 | 15 | 2024-12-01 |
| 2025-01 | 218 | 29 | 41 | 31 | 2025-01-01 |
| 2025-02 | 74 | 12 | 44 | 45 | 2025-02-01 |
| 2025-03 | 151 | 18 | 47 | 41 | 2025-03-01 |
| 2025-04 | 230 | 14 | 26 | 24 | 2025-04-01 |
| 2025-05 | 309 | 50 | 122 | 74 | 2025-05-01 |
| 2025-06 | 548 | 57 | 116 | 101 | 2025-06-01 |
| 2025-07 | 347 | 35 | 31 | 77 | 2025-07-01 |
| 2025-08 | 127 | 20 | 14 | 22 | 2025-08-01 |
| 2025-09 | 343 | 57 | 21 | 47 | 2025-09-01 |
| 2025-10 | 260 | 10 | 57 | 40 | 2025-10-01 |
| 2025-11 | 101 | 19 | 10 | 17 | 2025-11-01 |
| 2025-12 | 97 | 15 | 14 | 11 | 2025-12-01 |
| 2026-01 | 73 | 1 | 8 | 4 | 2026-01-01 |


### activity_bias_by_bloc.csv (4 lignes)

| bloc | n_tweets | n_deputies | tweets_per_deputy |
| --- | --- | --- | --- |
| Centre / Majorite | 944 | 56 | 16.857142857142858 |
| Droite | 1150 | 58 | 19.82758620689655 |
| Gauche moderee | 814 | 23 | 35.391304347826086 |
| Gauche radicale | 6227 | 51 | 122.09803921568628 |


### attrition_mensuelle.csv (28 lignes)

| month | n_deputes_actifs | n_textes | month_ts |
| --- | --- | --- | --- |
| 2023-10 | 211 | 1353 | 2023-10-01 |
| 2023-11 | 148 | 601 | 2023-11-01 |
| 2023-12 | 55 | 199 | 2023-12-01 |
| 2024-01 | 91 | 352 | 2024-01-01 |
| 2024-02 | 95 | 377 | 2024-02-01 |
| 2024-03 | 103 | 407 | 2024-03-01 |
| 2024-04 | 104 | 494 | 2024-04-01 |
| 2024-05 | 130 | 867 | 2024-05-01 |
| 2024-06 | 79 | 227 | 2024-06-01 |
| 2024-07 | 64 | 244 | 2024-07-01 |
| 2024-08 | 59 | 184 | 2024-08-01 |
| 2024-09 | 57 | 280 | 2024-09-01 |
| 2024-10 | 116 | 435 | 2024-10-01 |
| 2024-11 | 87 | 320 | 2024-11-01 |
| 2024-12 | 45 | 134 | 2024-12-01 |
| 2025-01 | 96 | 319 | 2025-01-01 |
| 2025-02 | 70 | 175 | 2025-02-01 |
| 2025-03 | 87 | 257 | 2025-03-01 |
| 2025-04 | 64 | 294 | 2025-04-01 |
| 2025-05 | 124 | 555 | 2025-05-01 |
| 2025-06 | 137 | 822 | 2025-06-01 |
| 2025-07 | 109 | 490 | 2025-07-01 |
| 2025-08 | 49 | 183 | 2025-08-01 |
| 2025-09 | 85 | 468 | 2025-09-01 |
| 2025-10 | 87 | 367 | 2025-10-01 |
| 2025-11 | 60 | 147 | 2025-11-01 |
| 2025-12 | 52 | 137 | 2025-12-01 |
| 2026-01 | 34 | 86 | 2026-01-01 |


### visibility_paradox_quintiles.csv (5 lignes)

| quintile | mean_abs_stance | mean_stance | n |
| --- | --- | --- | --- |
| 0.0 | 1.0001012145748989 | -0.7755398110661268 | 38.0 |
| 1.0 | 1.1037594614444708 | -0.7991926826841438 | 37.0 |
| 2.0 | 1.0083608756985318 | -0.3761821812860997 | 38.0 |
| 3.0 | 1.2183780332183678 | 0.0278775392115644 | 37.0 |
| 4.0 | 1.567297907254435 | 1.2031783620297716 | 38.0 |


### volume_par_groupe.csv (16 lignes)

| group | 0 |
| --- | --- |
| DEM | 53 |
| HOR | 68 |
| SOC | 79 |
| NI | 82 |
| UDR | 87 |
| ECO | 91 |
| MODEM | 182 |
| PS-NFP | 318 |
| LR | 320 |
| GDR | 395 |
| REN | 480 |
| ECO-NFP | 483 |
| EPR | 706 |
| LFI | 832 |
| RN | 987 |
| LFI-NFP | 5611 |


### panel_b4.csv (44 lignes)

| author | bloc |
| --- | --- |
| Alma Dufour | Gauche radicale |
| Antoine Léaument | Gauche radicale |
| Aurore Bergé | Centre / Majorite |
| Aurélien Saintoul | Gauche radicale |
| Aurélien Taché | Gauche radicale |
| Aymeric Caron | Gauche radicale |
| Bastien Lachaud | Gauche radicale |
| Bruno Bilde | Droite |
| Carlos Martens Bilongo | Gauche radicale |
| Caroline Yadan | Centre / Majorite |
| Clémentine Autain | Gauche radicale |
| Constance Le Grip | Centre / Majorite |
| Danièle Obono | Gauche radicale |
| David Guiraud | Gauche radicale |
| Elsa Faucillon | Gauche radicale |
| Emmanuel Fernandes | Gauche radicale |
| Fabien Roussel | Gauche radicale |
| François Cormier-Bouligeon | Centre / Majorite |
| François Piquemal | Gauche radicale |
| Gabriel Amard | Gauche radicale |
| Gabrielle Cathala | Gauche radicale |
| Hadrien Clouet | Gauche radicale |
| Jean-François Coulomme | Gauche radicale |
| Julien Odoul | Droite |
| Jérôme Buisson | Droite |
| Jérôme Guedj | Gauche moderee |
| Jérôme Legavre | Gauche radicale |
| Louis Boyard | Gauche radicale |
| Manuel Bompard | Gauche radicale |
| Mathilde Panot | Gauche radicale |
| Michèle Tabarot | Droite |
| Nadège Abomangoli | Gauche radicale |
| Nathalie Oziol | Gauche radicale |
| Olivier Faure | Gauche moderee |
| Paul Vannier | Gauche radicale |
| Pierre-Yves Cadalen | Gauche radicale |
| Raphaël Arnault | Gauche radicale |
| Sabrina Sebaihi | Gauche moderee |
| Soumya Bourouaha | Gauche radicale |
| Sébastien Delogu | Gauche radicale |
| Ségolène Amiot | Gauche radicale |
| Thomas Portes | Gauche radicale |
| Ugo Bernalicis | Gauche radicale |
| Éric Coquerel | Gauche radicale |


## 02 — Validation annotation

### stance_panel_vs_complet.csv (4 lignes)

| bloc | stance_complet | stance_panel_b4 | n_complet | n_panel | delta |
| --- | --- | --- | --- | --- | --- |
| Gauche radicale | 1.5741444866920151 | 1.632726617408542 | 6838 | 5549 | 0.0585821307165268 |
| Gauche moderee | 0.925849639546859 | 0.965174129353234 | 971 | 402 | 0.0393244898063749 |
| Centre / Majorite | -0.7689724647414372 | -1.1578947368421053 | 1489 | 475 | -0.3889222721006681 |
| Droite | -1.3780487804878048 | -1.5433255269320842 | 1476 | 427 | -0.1652767464442794 |


## 03 — Dynamiques temporelles

### stance_mensuel.csv (112 lignes)

| month | bloc | stance_v3 | month_ts |
| --- | --- | --- | --- |
| 2023-10 | Centre / Majorite | -0.8980392156862745 | 2023-10-01 |
| 2023-10 | Droite | -1.4466666666666668 | 2023-10-01 |
| 2023-10 | Gauche moderee | 0.6470588235294118 | 2023-10-01 |
| 2023-10 | Gauche radicale | 1.2651162790697674 | 2023-10-01 |
| 2023-11 | Centre / Majorite | -0.8130841121495327 | 2023-11-01 |
| 2023-11 | Droite | -1.1869158878504673 | 2023-11-01 |
| 2023-11 | Gauche moderee | 0.6545454545454545 | 2023-11-01 |
| 2023-11 | Gauche radicale | 1.3734939759036144 | 2023-11-01 |
| 2023-12 | Centre / Majorite | -0.2 | 2023-12-01 |
| 2023-12 | Droite | -1.125 | 2023-12-01 |
| 2023-12 | Gauche moderee | 0.875 | 2023-12-01 |
| 2023-12 | Gauche radicale | 1.4904458598726114 | 2023-12-01 |
| 2024-01 | Centre / Majorite | -0.8125 | 2024-01-01 |
| 2024-01 | Droite | -1.375 | 2024-01-01 |
| 2024-01 | Gauche moderee | 1.2666666666666666 | 2024-01-01 |
| 2024-01 | Gauche radicale | 1.7300884955752212 | 2024-01-01 |
| 2024-02 | Centre / Majorite | -0.8615384615384616 | 2024-02-01 |
| 2024-02 | Droite | -1.375 | 2024-02-01 |
| 2024-02 | Gauche moderee | 1.181818181818182 | 2024-02-01 |
| 2024-02 | Gauche radicale | 1.5644444444444443 | 2024-02-01 |
| 2024-03 | Centre / Majorite | -0.7872340425531915 | 2024-03-01 |
| 2024-03 | Droite | -1.6164383561643836 | 2024-03-01 |
| 2024-03 | Gauche moderee | 1.3863636363636365 | 2024-03-01 |
| 2024-03 | Gauche radicale | 1.4938271604938271 | 2024-03-01 |
| 2024-04 | Centre / Majorite | -0.8823529411764706 | 2024-04-01 |
| 2024-04 | Droite | -1.2941176470588236 | 2024-04-01 |
| 2024-04 | Gauche moderee | 0.7441860465116279 | 2024-04-01 |
| 2024-04 | Gauche radicale | 1.5759312320916905 | 2024-04-01 |
| 2024-05 | Centre / Majorite | -0.6153846153846154 | 2024-05-01 |
| 2024-05 | Droite | -1.5238095238095235 | 2024-05-01 |
| 2024-05 | Gauche moderee | 1.2173913043478262 | 2024-05-01 |
| 2024-05 | Gauche radicale | 1.7269736842105263 | 2024-05-01 |
| 2024-06 | Centre / Majorite | -0.7115384615384616 | 2024-06-01 |
| 2024-06 | Droite | -1.56 | 2024-06-01 |
| 2024-06 | Gauche moderee | 0.875 | 2024-06-01 |
| 2024-06 | Gauche radicale | 1.4603174603174602 | 2024-06-01 |
| 2024-07 | Centre / Majorite | -0.7407407407407407 | 2024-07-01 |
| 2024-07 | Droite | -1.65 | 2024-07-01 |
| 2024-07 | Gauche moderee | 1.0 | 2024-07-01 |
| 2024-07 | Gauche radicale | 1.6748466257668713 | 2024-07-01 |
| 2024-08 | Centre / Majorite | -1.3142857142857145 | 2024-08-01 |
| 2024-08 | Droite | -1.411764705882353 | 2024-08-01 |
| 2024-08 | Gauche moderee | 0.4375 | 2024-08-01 |
| 2024-08 | Gauche radicale | 1.616161616161616 | 2024-08-01 |
| 2024-09 | Centre / Majorite | -1.2 | 2024-09-01 |
| 2024-09 | Droite | -1.263157894736842 | 2024-09-01 |
| 2024-09 | Gauche moderee | 1.0952380952380951 | 2024-09-01 |
| 2024-09 | Gauche radicale | 1.5422222222222222 | 2024-09-01 |
| 2024-10 | Centre / Majorite | -0.8714285714285714 | 2024-10-01 |
| 2024-10 | Droite | -1.065217391304348 | 2024-10-01 |
| 2024-10 | Gauche moderee | 1.1304347826086956 | 2024-10-01 |
| 2024-10 | Gauche radicale | 1.708 | 2024-10-01 |
| 2024-11 | Centre / Majorite | -0.9333333333333332 | 2024-11-01 |
| 2024-11 | Droite | -1.2093023255813953 | 2024-11-01 |
| 2024-11 | Gauche moderee | 1.131578947368421 | 2024-11-01 |
| 2024-11 | Gauche radicale | 1.5980861244019138 | 2024-11-01 |
| 2024-12 | Centre / Majorite | -0.8333333333333334 | 2024-12-01 |
| 2024-12 | Droite | -0.6 | 2024-12-01 |
| 2024-12 | Gauche moderee | 1.1 | 2024-12-01 |
| 2024-12 | Gauche radicale | 1.796116504854369 | 2024-12-01 |
| 2025-01 | Centre / Majorite | -0.3902439024390244 | 2025-01-01 |
| 2025-01 | Droite | -0.9032258064516128 | 2025-01-01 |
| 2025-01 | Gauche moderee | 0.8620689655172413 | 2025-01-01 |
| 2025-01 | Gauche radicale | 1.5045871559633028 | 2025-01-01 |
| 2025-02 | Centre / Majorite | -1.0227272727272727 | 2025-02-01 |
| 2025-02 | Droite | -1.6 | 2025-02-01 |
| 2025-02 | Gauche moderee | 0.5833333333333334 | 2025-02-01 |
| 2025-02 | Gauche radicale | 1.4054054054054057 | 2025-02-01 |
| 2025-03 | Centre / Majorite | -0.723404255319149 | 2025-03-01 |
| 2025-03 | Droite | -1.3902439024390243 | 2025-03-01 |
| 2025-03 | Gauche moderee | 1.0555555555555556 | 2025-03-01 |
| 2025-03 | Gauche radicale | 1.403973509933775 | 2025-03-01 |
| 2025-04 | Centre / Majorite | -0.5384615384615384 | 2025-04-01 |
| 2025-04 | Droite | -1.5416666666666667 | 2025-04-01 |
| 2025-04 | Gauche moderee | 0.8571428571428571 | 2025-04-01 |
| 2025-04 | Gauche radicale | 1.6652173913043478 | 2025-04-01 |
| 2025-05 | Centre / Majorite | -0.4754098360655737 | 2025-05-01 |
| 2025-05 | Droite | -1.5 | 2025-05-01 |
| 2025-05 | Gauche moderee | 0.88 | 2025-05-01 |
| 2025-05 | Gauche radicale | 1.56957928802589 | 2025-05-01 |
| 2025-06 | Centre / Majorite | -0.5603448275862069 | 2025-06-01 |
| 2025-06 | Droite | -1.386138613861386 | 2025-06-01 |
| 2025-06 | Gauche moderee | 0.8947368421052632 | 2025-06-01 |
| 2025-06 | Gauche radicale | 1.635036496350365 | 2025-06-01 |
| 2025-07 | Centre / Majorite | -0.6774193548387096 | 2025-07-01 |
| 2025-07 | Droite | -1.4935064935064934 | 2025-07-01 |
| 2025-07 | Gauche moderee | 1.4 | 2025-07-01 |
| 2025-07 | Gauche radicale | 1.6685878962536025 | 2025-07-01 |
| 2025-08 | Centre / Majorite | -1.1428571428571428 | 2025-08-01 |
| 2025-08 | Droite | -1.7272727272727273 | 2025-08-01 |
| 2025-08 | Gauche moderee | 1.1 | 2025-08-01 |
| 2025-08 | Gauche radicale | 1.7716535433070866 | 2025-08-01 |
| 2025-09 | Centre / Majorite | -0.1428571428571428 | 2025-09-01 |
| 2025-09 | Droite | -1.2765957446808511 | 2025-09-01 |
| 2025-09 | Gauche moderee | 1.0701754385964912 | 2025-09-01 |
| 2025-09 | Gauche radicale | 1.7142857142857142 | 2025-09-01 |
| 2025-10 | Centre / Majorite | -1.087719298245614 | 2025-10-01 |
| 2025-10 | Droite | -1.1 | 2025-10-01 |
| 2025-10 | Gauche moderee | -0.1 | 2025-10-01 |
| 2025-10 | Gauche radicale | 1.646153846153846 | 2025-10-01 |
| 2025-11 | Centre / Majorite | -0.4 | 2025-11-01 |
| 2025-11 | Droite | -1.4705882352941178 | 2025-11-01 |
| 2025-11 | Gauche moderee | 0.6842105263157895 | 2025-11-01 |
| 2025-11 | Gauche radicale | 1.683168316831683 | 2025-11-01 |
| 2025-12 | Centre / Majorite | -1.0 | 2025-12-01 |
| 2025-12 | Droite | -1.4545454545454546 | 2025-12-01 |
| 2025-12 | Gauche moderee | -0.2666666666666666 | 2025-12-01 |
| 2025-12 | Gauche radicale | 1.6082474226804124 | 2025-12-01 |
| 2026-01 | Centre / Majorite | -0.75 | 2026-01-01 |
| 2026-01 | Droite | -2.0 | 2026-01-01 |
| 2026-01 | Gauche moderee | -1.0 | 2026-01-01 |
| 2026-01 | Gauche radicale | 1.2054794520547945 | 2026-01-01 |


### event_impact_diff_in_diff.csv (12 lignes)

| event | bloc | delta | p |
| --- | --- | --- | --- |
| 2024-01-26 | Gauche radicale | -0.0477062758840396 | 0.4483255851730465 |
| 2024-01-26 | Gauche moderee | 0.3250517598343686 | 0.083127336352378 |
| 2024-01-26 | Centre / Majorite | -0.1032258064516128 | 0.3388576654440041 |
| 2024-01-26 | Droite | 0.1855779427359489 | 0.4000738395890147 |
| 2024-05-07 | Gauche radicale | 0.1215015920898274 | 0.0015806564854549 |
| 2024-05-07 | Gauche moderee | 0.518041237113402 | 0.0011951130800336 |
| 2024-05-07 | Centre / Majorite | 0.301404853128991 | 0.0306026357234983 |
| 2024-05-07 | Droite | -0.2219227313566936 | 0.0723794149957129 |
| 2025-01-15 | Gauche radicale | -0.1633085896076351 | 0.036685820324134 |
| 2025-01-15 | Gauche moderee | -0.3333333333333333 | 0.2837373670320056 |
| 2025-01-15 | Centre / Majorite | -0.5877742946708464 | 0.0083919708222987 |
| 2025-01-15 | Droite | -1.0285714285714285 | 0.0075558924182788 |


### wasserstein_inter_blocs.csv (163 lignes)

| month | pair | wd_norm |
| --- | --- | --- |
| 2023-10 | Gauche radicale vs Gauche moderee | 0.1545143638850889 |
| 2023-10 | Gauche radicale vs Centre / Majorite | 0.5407888736890105 |
| 2023-10 | Gauche radicale vs Droite | 0.6779457364341085 |
| 2023-10 | Gauche moderee vs Centre / Majorite | 0.3862745098039216 |
| 2023-10 | Gauche moderee vs Droite | 0.5234313725490196 |
| 2023-10 | Centre / Majorite vs Droite | 0.137156862745098 |
| 2023-11 | Gauche radicale vs Gauche moderee | 0.1872672508214676 |
| 2023-11 | Gauche radicale vs Centre / Majorite | 0.5466445220132867 |
| 2023-11 | Gauche radicale vs Droite | 0.6401024659385204 |
| 2023-11 | Gauche moderee vs Centre / Majorite | 0.3669073916737468 |
| 2023-11 | Gauche moderee vs Droite | 0.4603653355989804 |
| 2023-11 | Centre / Majorite vs Droite | 0.0934579439252336 |
| 2023-12 | Gauche radicale vs Gauche moderee | 0.1729697452229299 |
| 2023-12 | Gauche radicale vs Centre / Majorite | 0.4417197452229299 |
| 2023-12 | Gauche radicale vs Droite | 0.6538614649681529 |
| 2023-12 | Gauche moderee vs Centre / Majorite | 0.26875 |
| 2023-12 | Gauche moderee vs Droite | 0.5 |
| 2023-12 | Centre / Majorite vs Droite | 0.23125 |
| 2024-01 | Gauche radicale vs Gauche moderee | 0.1202802359882005 |
| 2024-01 | Gauche radicale vs Centre / Majorite | 0.6356471238938053 |
| 2024-01 | Gauche radicale vs Droite | 0.7762721238938053 |
| 2024-01 | Gauche moderee vs Centre / Majorite | 0.5197916666666667 |
| 2024-01 | Gauche moderee vs Droite | 0.6604166666666667 |
| 2024-01 | Centre / Majorite vs Droite | 0.140625 |
| 2024-02 | Gauche radicale vs Gauche moderee | 0.0956565656565656 |
| 2024-02 | Gauche radicale vs Centre / Majorite | 0.6064957264957265 |
| 2024-02 | Gauche radicale vs Droite | 0.7348611111111112 |
| 2024-02 | Gauche moderee vs Centre / Majorite | 0.5108391608391609 |
| 2024-02 | Gauche moderee vs Droite | 0.6392045454545455 |
| 2024-02 | Centre / Majorite vs Droite | 0.1283653846153846 |
| 2024-03 | Gauche radicale vs Gauche moderee | 0.1101524504302282 |
| 2024-03 | Gauche radicale vs Centre / Majorite | 0.5702653007617546 |
| 2024-03 | Gauche radicale vs Droite | 0.7775663791645526 |
| 2024-03 | Gauche moderee vs Centre / Majorite | 0.5433994197292069 |
| 2024-03 | Gauche moderee vs Droite | 0.7507004981320049 |
| 2024-03 | Centre / Majorite vs Droite | 0.207301078402798 |
| 2024-04 | Gauche radicale vs Gauche moderee | 0.2079362963950156 |
| 2024-04 | Gauche radicale vs Centre / Majorite | 0.6145710433170403 |
| 2024-04 | Gauche radicale vs Droite | 0.7175122197876285 |
| 2024-04 | Gauche moderee vs Centre / Majorite | 0.4066347469220246 |
| 2024-04 | Gauche moderee vs Droite | 0.5095759233926129 |
| 2024-04 | Centre / Majorite vs Droite | 0.1127450980392157 |
| 2024-05 | Gauche radicale vs Gauche moderee | 0.1277173913043478 |
| 2024-05 | Gauche radicale vs Centre / Majorite | 0.5855895748987854 |
| 2024-05 | Gauche radicale vs Droite | 0.8126958020050126 |
| 2024-05 | Gauche moderee vs Centre / Majorite | 0.4581939799331104 |
| 2024-05 | Gauche moderee vs Droite | 0.6853002070393375 |
| 2024-05 | Centre / Majorite vs Droite | 0.227106227106227 |
| 2024-06 | Gauche radicale vs Gauche moderee | 0.1463293650793651 |
| 2024-06 | Gauche radicale vs Centre / Majorite | 0.5429639804639805 |
| 2024-06 | Gauche radicale vs Droite | 0.7550793650793651 |
| 2024-06 | Gauche moderee vs Centre / Majorite | 0.3966346153846154 |
| 2024-06 | Gauche moderee vs Droite | 0.60875 |
| 2024-06 | Centre / Majorite vs Droite | 0.2121153846153846 |
| 2024-07 | Gauche radicale vs Gauche moderee | 0.1809815950920245 |
| 2024-07 | Gauche radicale vs Centre / Majorite | 0.6038968416269029 |
| 2024-07 | Gauche radicale vs Droite | 0.8312116564417178 |
| 2024-07 | Gauche moderee vs Centre / Majorite | 0.4351851851851852 |
| 2024-07 | Gauche moderee vs Droite | 0.6625000000000001 |
| 2024-07 | Centre / Majorite vs Droite | 0.2273148148148148 |
| 2024-08 | Gauche radicale vs Gauche moderee | 0.3047664141414141 |
| 2024-08 | Gauche radicale vs Centre / Majorite | 0.7326118326118327 |
| 2024-08 | Gauche radicale vs Droite | 0.7569815805109923 |
| 2024-08 | Gauche moderee vs Centre / Majorite | 0.4379464285714285 |
| 2024-08 | Gauche moderee vs Droite | 0.4623161764705882 |
| 2024-08 | Centre / Majorite vs Droite | 0.0243697478991596 |
| 2024-09 | Gauche radicale vs Gauche moderee | 0.1434920634920635 |
| 2024-09 | Gauche radicale vs Centre / Majorite | 0.6855555555555556 |
| 2024-09 | Gauche radicale vs Droite | 0.701345029239766 |
| 2024-09 | Gauche moderee vs Centre / Majorite | 0.5738095238095238 |
| 2024-09 | Gauche moderee vs Droite | 0.5895989974937343 |
| 2024-09 | Centre / Majorite vs Droite | 0.087719298245614 |
| 2024-10 | Gauche radicale vs Gauche moderee | 0.1523913043478261 |
| 2024-10 | Gauche radicale vs Centre / Majorite | 0.6448571428571428 |
| 2024-10 | Gauche radicale vs Droite | 0.693304347826087 |
| 2024-10 | Gauche moderee vs Centre / Majorite | 0.5004658385093168 |
| 2024-10 | Gauche moderee vs Droite | 0.5489130434782609 |
| 2024-10 | Centre / Majorite vs Droite | 0.0636645962732919 |
| 2024-11 | Gauche radicale vs Gauche moderee | 0.1680622009569378 |
| 2024-11 | Gauche radicale vs Centre / Majorite | 0.6328548644338119 |
| 2024-11 | Gauche radicale vs Droite | 0.7018471124958273 |
| 2024-11 | Gauche moderee vs Centre / Majorite | 0.5162280701754387 |
| 2024-11 | Gauche moderee vs Droite | 0.5852203182374541 |
| 2024-11 | Centre / Majorite vs Droite | 0.0705426356589147 |
| 2024-12 | Gauche radicale vs Gauche moderee | 0.1885922330097087 |
| 2024-12 | Gauche radicale vs Centre / Majorite | 0.6573624595469256 |
| 2024-12 | Gauche radicale vs Droite | 0.5990291262135923 |
| 2024-12 | Gauche moderee vs Centre / Majorite | 0.4833333333333333 |
| 2024-12 | Gauche moderee vs Droite | 0.425 |
| 2024-12 | Centre / Majorite vs Droite | 0.1583333333333333 |
| 2025-01 | Gauche radicale vs Gauche moderee | 0.1606295476115153 |
| 2025-01 | Gauche radicale vs Centre / Majorite | 0.4737077646005818 |
| 2025-01 | Gauche radicale vs Droite | 0.6019532406037289 |
| 2025-01 | Gauche moderee vs Centre / Majorite | 0.3130782169890664 |
| 2025-01 | Gauche moderee vs Droite | 0.4413236929922136 |
| 2025-01 | Centre / Majorite vs Droite | 0.1443745082612116 |
| 2025-02 | Gauche radicale vs Gauche moderee | 0.205518018018018 |
| 2025-02 | Gauche radicale vs Centre / Majorite | 0.6070331695331695 |
| 2025-02 | Gauche radicale vs Droite | 0.7513513513513512 |
| 2025-02 | Gauche moderee vs Centre / Majorite | 0.4015151515151515 |
| 2025-02 | Gauche moderee vs Droite | 0.5458333333333334 |
| 2025-02 | Centre / Majorite vs Droite | 0.1443181818181818 |
| 2025-03 | Gauche radicale vs Gauche moderee | 0.139532744665195 |
| 2025-03 | Gauche radicale vs Centre / Majorite | 0.5318444413132309 |
| 2025-03 | Gauche radicale vs Droite | 0.6985543530931998 |
| 2025-03 | Gauche moderee vs Centre / Majorite | 0.4447399527186761 |
| 2025-03 | Gauche moderee vs Droite | 0.611449864498645 |
| 2025-03 | Centre / Majorite vs Droite | 0.1682667358588479 |
| 2025-04 | Gauche radicale vs Gauche moderee | 0.2020186335403726 |
| 2025-04 | Gauche radicale vs Centre / Majorite | 0.5509197324414715 |
| 2025-04 | Gauche radicale vs Droite | 0.8017210144927537 |
| 2025-04 | Gauche moderee vs Centre / Majorite | 0.3489010989010989 |
| 2025-04 | Gauche moderee vs Droite | 0.5997023809523809 |
| 2025-04 | Centre / Majorite vs Droite | 0.250801282051282 |
| 2025-05 | Gauche radicale vs Gauche moderee | 0.1723948220064725 |
| 2025-05 | Gauche radicale vs Centre / Majorite | 0.5112472810228659 |
| 2025-05 | Gauche radicale vs Droite | 0.7673948220064725 |
| 2025-05 | Gauche moderee vs Centre / Majorite | 0.3388524590163934 |
| 2025-05 | Gauche moderee vs Droite | 0.595 |
| 2025-05 | Centre / Majorite vs Droite | 0.2561475409836066 |
| 2025-06 | Gauche radicale vs Gauche moderee | 0.1896369573568959 |
| 2025-06 | Gauche radicale vs Centre / Majorite | 0.548845330984143 |
| 2025-06 | Gauche radicale vs Droite | 0.7552937775529378 |
| 2025-06 | Gauche moderee vs Centre / Majorite | 0.3637704174228675 |
| 2025-06 | Gauche moderee vs Droite | 0.5702188639916623 |
| 2025-06 | Centre / Majorite vs Droite | 0.2064484465687948 |
| 2025-07 | Gauche radicale vs Gauche moderee | 0.0916426512968299 |
| 2025-07 | Gauche radicale vs Centre / Majorite | 0.5865018127730779 |
| 2025-07 | Gauche radicale vs Droite | 0.7905235974400239 |
| 2025-07 | Gauche moderee vs Centre / Majorite | 0.5193548387096775 |
| 2025-07 | Gauche moderee vs Droite | 0.7233766233766233 |
| 2025-07 | Centre / Majorite vs Droite | 0.2040217846669459 |
| 2025-08 | Gauche radicale vs Gauche moderee | 0.1718503937007874 |
| 2025-08 | Gauche radicale vs Centre / Majorite | 0.7286276715410573 |
| 2025-08 | Gauche radicale vs Droite | 0.8747315676449535 |
| 2025-08 | Gauche moderee vs Centre / Majorite | 0.5607142857142857 |
| 2025-08 | Gauche moderee vs Droite | 0.7068181818181818 |
| 2025-08 | Centre / Majorite vs Droite | 0.1461038961038961 |
| 2025-09 | Gauche radicale vs Gauche moderee | 0.1697739246074369 |
| 2025-09 | Gauche radicale vs Centre / Majorite | 0.4642857142857143 |
| 2025-09 | Gauche radicale vs Droite | 0.7477203647416413 |
| 2025-09 | Gauche moderee vs Centre / Majorite | 0.3032581453634085 |
| 2025-09 | Gauche moderee vs Droite | 0.5866927958193355 |
| 2025-09 | Centre / Majorite vs Droite | 0.2940729483282674 |
| 2025-10 | Gauche radicale vs Gauche moderee | 0.4365384615384615 |
| 2025-10 | Gauche radicale vs Centre / Majorite | 0.6834682860998651 |
| 2025-10 | Gauche radicale vs Droite | 0.6865384615384615 |
| 2025-10 | Gauche moderee vs Centre / Majorite | 0.2469298245614035 |
| 2025-10 | Gauche moderee vs Droite | 0.25 |
| 2025-10 | Centre / Majorite vs Droite | 0.0320175438596491 |
| 2025-11 | Gauche radicale vs Gauche moderee | 0.2596404377279833 |
| 2025-11 | Gauche radicale vs Centre / Majorite | 0.5207920792079208 |
| 2025-11 | Gauche radicale vs Droite | 0.7884391380314502 |
| 2025-11 | Gauche moderee vs Centre / Majorite | 0.2710526315789474 |
| 2025-11 | Gauche moderee vs Droite | 0.5386996904024768 |
| 2025-11 | Centre / Majorite vs Droite | 0.2676470588235294 |
| 2025-12 | Gauche radicale vs Gauche moderee | 0.4687285223367697 |
| 2025-12 | Gauche radicale vs Centre / Majorite | 0.652061855670103 |
| 2025-12 | Gauche radicale vs Droite | 0.7656982193064668 |
| 2025-12 | Gauche moderee vs Centre / Majorite | 0.1833333333333333 |
| 2025-12 | Gauche moderee vs Droite | 0.2969696969696969 |
| 2025-12 | Centre / Majorite vs Droite | 0.1136363636363636 |
| 2026-01 | Gauche radicale vs Centre / Majorite | 0.4888698630136986 |


### wasserstein_drift.csv (110 lignes)

| month | bloc | wd_norm |
| --- | --- | --- |
| 2023-10 | Gauche radicale | 0.0 |
| 2023-11 | Gauche radicale | 0.0270944242084617 |
| 2023-12 | Gauche radicale | 0.0661383498740927 |
| 2024-01 | Gauche radicale | 0.1162430541263634 |
| 2024-02 | Gauche radicale | 0.0748320413436692 |
| 2024-03 | Gauche radicale | 0.0581634606182409 |
| 2024-04 | Gauche radicale | 0.0784300659692143 |
| 2024-05 | Gauche radicale | 0.1154643512851897 |
| 2024-06 | Gauche radicale | 0.0488002953119232 |
| 2024-07 | Gauche radicale | 0.1054001997431873 |
| 2024-08 | Gauche radicale | 0.0885600187925769 |
| 2024-09 | Gauche radicale | 0.0755297157622739 |
| 2024-10 | Gauche radicale | 0.1107209302325581 |
| 2024-11 | Gauche radicale | 0.0859018582396795 |
| 2024-12 | Gauche radicale | 0.1327500564461503 |
| 2025-01 | Gauche radicale | 0.0620332835502453 |
| 2025-02 | Gauche radicale | 0.0543578462183113 |
| 2025-03 | Gauche radicale | 0.0485907900816263 |
| 2025-04 | Gauche radicale | 0.1000252780586451 |
| 2025-05 | Gauche radicale | 0.0813765334537517 |
| 2025-06 | Gauche radicale | 0.0924800543201493 |
| 2025-07 | Gauche radicale | 0.1008679042959587 |
| 2025-08 | Gauche radicale | 0.1266343160593298 |
| 2025-09 | Gauche radicale | 0.1122923588039867 |
| 2025-10 | Gauche radicale | 0.0952593917710196 |
| 2025-11 | Gauche radicale | 0.1051116739580934 |
| 2025-12 | Gauche radicale | 0.091944377847039 |
| 2026-01 | Gauche radicale | 0.0285865987044706 |
| 2023-10 | Gauche moderee | 0.0 |
| 2023-11 | Gauche moderee | 0.0119132501485442 |
| 2023-12 | Gauche moderee | 0.0592320261437908 |
| 2024-01 | Gauche moderee | 0.1549019607843137 |
| 2024-02 | Gauche moderee | 0.1336898395721925 |
| 2024-03 | Gauche moderee | 0.1848262032085561 |
| 2024-04 | Gauche moderee | 0.0261057911536707 |
| 2024-05 | Gauche moderee | 0.1425831202046036 |
| 2024-06 | Gauche moderee | 0.0806781045751633 |
| 2024-07 | Gauche moderee | 0.088235294117647 |
| 2024-08 | Gauche moderee | 0.0775122549019607 |
| 2024-09 | Gauche moderee | 0.1120448179271708 |
| 2024-10 | Gauche moderee | 0.1208439897698209 |
| 2024-11 | Gauche moderee | 0.1211300309597523 |
| 2024-12 | Gauche moderee | 0.113235294117647 |
| 2025-01 | Gauche moderee | 0.070655848546315 |
| 2025-02 | Gauche moderee | 0.0290032679738561 |
| 2025-03 | Gauche moderee | 0.1021241830065359 |
| 2025-04 | Gauche moderee | 0.0784313725490196 |
| 2025-05 | Gauche moderee | 0.0748366013071895 |
| 2025-06 | Gauche moderee | 0.066219470244238 |
| 2025-07 | Gauche moderee | 0.188235294117647 |
| 2025-08 | Gauche moderee | 0.113235294117647 |
| 2025-09 | Gauche moderee | 0.1057791537667698 |
| 2025-10 | Gauche moderee | 0.1867647058823529 |
| 2025-11 | Gauche moderee | 0.087719298245614 |
| 2025-12 | Gauche moderee | 0.2284313725490196 |
| 2023-10 | Centre / Majorite | 0.0 |
| 2023-11 | Centre / Majorite | 0.0477185266630016 |
| 2023-12 | Centre / Majorite | 0.1764705882352941 |
| 2024-01 | Centre / Majorite | 0.0276960784313725 |
| 2024-02 | Centre / Majorite | 0.0319004524886877 |
| 2024-03 | Centre / Majorite | 0.0483521068001669 |
| 2024-04 | Centre / Majorite | 0.0313725490196078 |
| 2024-05 | Centre / Majorite | 0.0706636500754148 |
| 2024-06 | Centre / Majorite | 0.0822963800904977 |
| 2024-07 | Centre / Majorite | 0.0513071895424837 |
| 2024-08 | Centre / Majorite | 0.1040616246498599 |
| 2024-09 | Centre / Majorite | 0.0754901960784313 |
| 2024-10 | Centre / Majorite | 0.0296218487394958 |
| 2024-11 | Centre / Majorite | 0.0264705882352941 |
| 2024-12 | Centre / Majorite | 0.1014705882352941 |
| 2025-01 | Centre / Majorite | 0.128909612625538 |
| 2025-02 | Centre / Majorite | 0.044451871657754 |
| 2025-03 | Centre / Majorite | 0.0436587400917814 |
| 2025-04 | Centre / Majorite | 0.0918552036199095 |
| 2025-05 | Centre / Majorite | 0.1068627450980392 |
| 2025-06 | Centre / Majorite | 0.0863843813387424 |
| 2025-07 | Centre / Majorite | 0.0551549652118912 |
| 2025-08 | Centre / Majorite | 0.061204481792717 |
| 2025-09 | Centre / Majorite | 0.1907563025210084 |
| 2025-10 | Centre / Majorite | 0.0474200206398348 |
| 2025-11 | Centre / Majorite | 0.1588235294117647 |
| 2025-12 | Centre / Majorite | 0.0439775910364145 |
| 2026-01 | Centre / Majorite | 0.1088235294117647 |
| 2023-10 | Droite | 0.0 |
| 2023-11 | Droite | 0.0649376947040498 |
| 2023-12 | Droite | 0.0920833333333333 |
| 2024-01 | Droite | 0.0239583333333333 |
| 2024-02 | Droite | 0.0295833333333333 |
| 2024-03 | Droite | 0.0429908675799086 |
| 2024-04 | Droite | 0.0381372549019607 |
| 2024-05 | Droite | 0.0289682539682539 |
| 2024-06 | Droite | 0.0283333333333333 |
| 2024-07 | Droite | 0.0508333333333333 |
| 2024-08 | Droite | 0.0256862745098039 |
| 2024-09 | Droite | 0.0475438596491227 |
| 2024-10 | Droite | 0.0953623188405797 |
| 2024-11 | Droite | 0.0610077519379844 |
| 2024-12 | Droite | 0.2133333333333333 |
| 2025-01 | Droite | 0.1358602150537634 |
| 2025-02 | Droite | 0.0383333333333333 |
| 2025-03 | Droite | 0.0152032520325203 |
| 2025-04 | Droite | 0.0237499999999999 |
| 2025-05 | Droite | 0.0136036036036036 |
| 2025-06 | Droite | 0.0218481848184818 |
| 2025-07 | Droite | 0.0271645021645021 |
| 2025-08 | Droite | 0.0701515151515151 |
| 2025-09 | Droite | 0.0425177304964539 |
| 2025-10 | Droite | 0.0983333333333333 |
| 2025-11 | Droite | 0.0448039215686274 |
| 2025-12 | Droite | 0.0296969696969697 |


### mann_kendall_bloc.csv (4 lignes)

| bloc | tau | p |
| --- | --- | --- |
| Gauche radicale | 0.1904761904761904 | 0.1620947367085582 |
| Gauche moderee | -0.190982104223769 | 0.1547289234853785 |
| Centre / Majorite | 0.0899470899470899 | 0.5179179428613762 |
| Droite | -0.113907384682632 | 0.3954940221864672 |


### deliberative_intensity_by_bloc_month.csv (110 lignes)

| month | bloc | pct_conflictual | n | month_ts |
| --- | --- | --- | --- | --- |
| 2023-10 | Centre / Majorite | 0.1019607843137254 | 255 | 2023-10-01 |
| 2023-10 | Droite | 0.1133333333333333 | 300 | 2023-10-01 |
| 2023-10 | Gauche moderee | 0.2091503267973856 | 153 | 2023-10-01 |
| 2023-10 | Gauche radicale | 0.1364341085271317 | 645 | 2023-10-01 |
| 2023-11 | Centre / Majorite | 0.0934579439252336 | 107 | 2023-11-01 |
| 2023-11 | Droite | 0.0934579439252336 | 107 | 2023-11-01 |
| 2023-11 | Gauche moderee | 0.1454545454545454 | 55 | 2023-11-01 |
| 2023-11 | Gauche radicale | 0.1536144578313253 | 332 | 2023-11-01 |
| 2023-12 | Centre / Majorite | 0.0 | 10 | 2023-12-01 |
| 2023-12 | Droite | 0.0 | 16 | 2023-12-01 |
| 2023-12 | Gauche moderee | 0.125 | 16 | 2023-12-01 |
| 2023-12 | Gauche radicale | 0.0955414012738853 | 157 | 2023-12-01 |
| 2024-01 | Centre / Majorite | 0.140625 | 64 | 2024-01-01 |
| 2024-01 | Droite | 0.125 | 32 | 2024-01-01 |
| 2024-01 | Gauche moderee | 0.2333333333333333 | 30 | 2024-01-01 |
| 2024-01 | Gauche radicale | 0.0884955752212389 | 226 | 2024-01-01 |
| 2024-02 | Centre / Majorite | 0.1384615384615384 | 65 | 2024-02-01 |
| 2024-02 | Droite | 0.0625 | 32 | 2024-02-01 |
| 2024-02 | Gauche moderee | 0.0545454545454545 | 55 | 2024-02-01 |
| 2024-02 | Gauche radicale | 0.08 | 225 | 2024-02-01 |
| 2024-03 | Centre / Majorite | 0.0425531914893617 | 47 | 2024-03-01 |
| 2024-03 | Droite | 0.0684931506849315 | 73 | 2024-03-01 |
| 2024-03 | Gauche moderee | 0.1363636363636363 | 44 | 2024-03-01 |
| 2024-03 | Gauche radicale | 0.139917695473251 | 243 | 2024-03-01 |
| 2024-04 | Centre / Majorite | 0.1372549019607843 | 51 | 2024-04-01 |
| 2024-04 | Droite | 0.0588235294117647 | 51 | 2024-04-01 |
| 2024-04 | Gauche moderee | 0.2325581395348837 | 43 | 2024-04-01 |
| 2024-04 | Gauche radicale | 0.1146131805157593 | 349 | 2024-04-01 |
| 2024-05 | Centre / Majorite | 0.1442307692307692 | 104 | 2024-05-01 |
| 2024-05 | Droite | 0.1111111111111111 | 63 | 2024-05-01 |
| 2024-05 | Gauche moderee | 0.0978260869565217 | 92 | 2024-05-01 |
| 2024-05 | Gauche radicale | 0.1447368421052631 | 608 | 2024-05-01 |
| 2024-06 | Centre / Majorite | 0.0576923076923076 | 52 | 2024-06-01 |
| 2024-06 | Droite | 0.12 | 25 | 2024-06-01 |
| 2024-06 | Gauche moderee | 0.2083333333333333 | 24 | 2024-06-01 |
| 2024-06 | Gauche radicale | 0.0873015873015873 | 126 | 2024-06-01 |
| 2024-07 | Centre / Majorite | 0.2592592592592592 | 27 | 2024-07-01 |
| 2024-07 | Droite | 0.05 | 40 | 2024-07-01 |
| 2024-07 | Gauche moderee | 0.0 | 14 | 2024-07-01 |
| 2024-07 | Gauche radicale | 0.1165644171779141 | 163 | 2024-07-01 |
| 2024-08 | Centre / Majorite | 0.1428571428571428 | 35 | 2024-08-01 |
| 2024-08 | Droite | 0.088235294117647 | 34 | 2024-08-01 |
| 2024-08 | Gauche moderee | 0.1875 | 16 | 2024-08-01 |
| 2024-08 | Gauche radicale | 0.0909090909090909 | 99 | 2024-08-01 |
| 2024-09 | Centre / Majorite | 0.0 | 15 | 2024-09-01 |
| 2024-09 | Droite | 0.0526315789473684 | 19 | 2024-09-01 |
| 2024-09 | Gauche moderee | 0.0952380952380952 | 21 | 2024-09-01 |
| 2024-09 | Gauche radicale | 0.1644444444444444 | 225 | 2024-09-01 |
| 2024-10 | Centre / Majorite | 0.1428571428571428 | 70 | 2024-10-01 |
| 2024-10 | Droite | 0.0652173913043478 | 92 | 2024-10-01 |
| 2024-10 | Gauche moderee | 0.1739130434782608 | 23 | 2024-10-01 |
| 2024-10 | Gauche radicale | 0.12 | 250 | 2024-10-01 |
| 2024-11 | Centre / Majorite | 0.1333333333333333 | 30 | 2024-11-01 |
| 2024-11 | Droite | 0.1860465116279069 | 43 | 2024-11-01 |
| 2024-11 | Gauche moderee | 0.0526315789473684 | 38 | 2024-11-01 |
| 2024-11 | Gauche radicale | 0.138755980861244 | 209 | 2024-11-01 |
| 2024-12 | Centre / Majorite | 0.1666666666666666 | 6 | 2024-12-01 |
| 2024-12 | Droite | 0.0666666666666666 | 15 | 2024-12-01 |
| 2024-12 | Gauche moderee | 0.1 | 10 | 2024-12-01 |
| 2024-12 | Gauche radicale | 0.116504854368932 | 103 | 2024-12-01 |
| 2025-01 | Centre / Majorite | 0.048780487804878 | 41 | 2025-01-01 |
| 2025-01 | Droite | 0.0967741935483871 | 31 | 2025-01-01 |
| 2025-01 | Gauche moderee | 0.1034482758620689 | 29 | 2025-01-01 |
| 2025-01 | Gauche radicale | 0.1605504587155963 | 218 | 2025-01-01 |
| 2025-02 | Centre / Majorite | 0.1818181818181818 | 44 | 2025-02-01 |
| 2025-02 | Droite | 0.0888888888888888 | 45 | 2025-02-01 |
| 2025-02 | Gauche moderee | 0.0833333333333333 | 12 | 2025-02-01 |
| 2025-02 | Gauche radicale | 0.081081081081081 | 74 | 2025-02-01 |
| 2025-03 | Centre / Majorite | 0.1489361702127659 | 47 | 2025-03-01 |
| 2025-03 | Droite | 0.0 | 41 | 2025-03-01 |
| 2025-03 | Gauche moderee | 0.3333333333333333 | 18 | 2025-03-01 |
| 2025-03 | Gauche radicale | 0.1390728476821192 | 151 | 2025-03-01 |
| 2025-04 | Centre / Majorite | 0.0769230769230769 | 26 | 2025-04-01 |
| 2025-04 | Droite | 0.0833333333333333 | 24 | 2025-04-01 |
| 2025-04 | Gauche moderee | 0.2142857142857142 | 14 | 2025-04-01 |
| 2025-04 | Gauche radicale | 0.1304347826086956 | 230 | 2025-04-01 |
| 2025-05 | Centre / Majorite | 0.0983606557377049 | 122 | 2025-05-01 |
| 2025-05 | Droite | 0.1081081081081081 | 74 | 2025-05-01 |
| 2025-05 | Gauche moderee | 0.14 | 50 | 2025-05-01 |
| 2025-05 | Gauche radicale | 0.1262135922330097 | 309 | 2025-05-01 |
| 2025-06 | Centre / Majorite | 0.1120689655172413 | 116 | 2025-06-01 |
| 2025-06 | Droite | 0.0693069306930693 | 101 | 2025-06-01 |
| 2025-06 | Gauche moderee | 0.1929824561403508 | 57 | 2025-06-01 |
| 2025-06 | Gauche radicale | 0.1660583941605839 | 548 | 2025-06-01 |
| 2025-07 | Centre / Majorite | 0.0967741935483871 | 31 | 2025-07-01 |
| 2025-07 | Droite | 0.1428571428571428 | 77 | 2025-07-01 |
| 2025-07 | Gauche moderee | 0.0571428571428571 | 35 | 2025-07-01 |
| 2025-07 | Gauche radicale | 0.1123919308357348 | 347 | 2025-07-01 |
| 2025-08 | Centre / Majorite | 0.0714285714285714 | 14 | 2025-08-01 |
| 2025-08 | Droite | 0.0909090909090909 | 22 | 2025-08-01 |
| 2025-08 | Gauche moderee | 0.25 | 20 | 2025-08-01 |
| 2025-08 | Gauche radicale | 0.0787401574803149 | 127 | 2025-08-01 |
| 2025-09 | Centre / Majorite | 0.0 | 21 | 2025-09-01 |
| 2025-09 | Droite | 0.0425531914893617 | 47 | 2025-09-01 |
| 2025-09 | Gauche moderee | 0.1052631578947368 | 57 | 2025-09-01 |
| 2025-09 | Gauche radicale | 0.0845481049562682 | 343 | 2025-09-01 |
| 2025-10 | Centre / Majorite | 0.1228070175438596 | 57 | 2025-10-01 |
| 2025-10 | Droite | 0.175 | 40 | 2025-10-01 |
| 2025-10 | Gauche moderee | 0.2 | 10 | 2025-10-01 |
| 2025-10 | Gauche radicale | 0.1038461538461538 | 260 | 2025-10-01 |
| 2025-11 | Centre / Majorite | 0.1 | 10 | 2025-11-01 |
| 2025-11 | Droite | 0.0 | 17 | 2025-11-01 |
| 2025-11 | Gauche moderee | 0.0 | 19 | 2025-11-01 |
| 2025-11 | Gauche radicale | 0.0693069306930693 | 101 | 2025-11-01 |
| 2025-12 | Centre / Majorite | 0.2142857142857142 | 14 | 2025-12-01 |
| 2025-12 | Droite | 0.0909090909090909 | 11 | 2025-12-01 |
| 2025-12 | Gauche moderee | 0.0 | 15 | 2025-12-01 |
| 2025-12 | Gauche radicale | 0.1237113402061855 | 97 | 2025-12-01 |
| 2026-01 | Centre / Majorite | 0.0 | 8 | 2026-01-01 |
| 2026-01 | Gauche radicale | 0.1095890410958904 | 73 | 2026-01-01 |


## 04 — Polarisation lexicale

### cosine_distance_mensuelle.csv (163 lignes)

| month | pair | dist |
| --- | --- | --- |
| 2023-10 | Gauche radicale vs Gauche moderee | 0.0855967628749312 |
| 2023-10 | Gauche radicale vs Centre / Majorite | 0.1519619371777365 |
| 2023-10 | Gauche radicale vs Droite | 0.194688392636634 |
| 2023-10 | Gauche moderee vs Centre / Majorite | 0.1563847737426215 |
| 2023-10 | Gauche moderee vs Droite | 0.1996379190180035 |
| 2023-10 | Centre / Majorite vs Droite | 0.08713547254258 |
| 2023-11 | Gauche radicale vs Gauche moderee | 0.1404833933091575 |
| 2023-11 | Gauche radicale vs Centre / Majorite | 0.328244169434838 |
| 2023-11 | Gauche radicale vs Droite | 0.2303479087675229 |
| 2023-11 | Gauche moderee vs Centre / Majorite | 0.294404033136046 |
| 2023-11 | Gauche moderee vs Droite | 0.2352096012207504 |
| 2023-11 | Centre / Majorite vs Droite | 0.1783313956316621 |
| 2023-12 | Gauche radicale vs Gauche moderee | 0.1965229339951911 |
| 2023-12 | Gauche radicale vs Centre / Majorite | 0.2225486254689541 |
| 2023-12 | Gauche radicale vs Droite | 0.2754015160295993 |
| 2023-12 | Gauche moderee vs Centre / Majorite | 0.3145516149186904 |
| 2023-12 | Gauche moderee vs Droite | 0.3527421610700245 |
| 2023-12 | Centre / Majorite vs Droite | 0.2803434414316461 |
| 2024-01 | Gauche radicale vs Gauche moderee | 0.1703409360709435 |
| 2024-01 | Gauche radicale vs Centre / Majorite | 0.2346634483263465 |
| 2024-01 | Gauche radicale vs Droite | 0.3616627706161677 |
| 2024-01 | Gauche moderee vs Centre / Majorite | 0.2915671227663525 |
| 2024-01 | Gauche moderee vs Droite | 0.44068082425804 |
| 2024-01 | Centre / Majorite vs Droite | 0.1938792087947183 |
| 2024-02 | Gauche radicale vs Gauche moderee | 0.1469597806102449 |
| 2024-02 | Gauche radicale vs Centre / Majorite | 0.2223936034666896 |
| 2024-02 | Gauche radicale vs Droite | 0.300760193001529 |
| 2024-02 | Gauche moderee vs Centre / Majorite | 0.299685542445425 |
| 2024-02 | Gauche moderee vs Droite | 0.3749453860014837 |
| 2024-02 | Centre / Majorite vs Droite | 0.152588600365386 |
| 2024-03 | Gauche radicale vs Gauche moderee | 0.1446592054993943 |
| 2024-03 | Gauche radicale vs Centre / Majorite | 0.2095819570615824 |
| 2024-03 | Gauche radicale vs Droite | 0.2433418238115744 |
| 2024-03 | Gauche moderee vs Centre / Majorite | 0.2969536312297357 |
| 2024-03 | Gauche moderee vs Droite | 0.3363834033042638 |
| 2024-03 | Centre / Majorite vs Droite | 0.18718025935982 |
| 2024-04 | Gauche radicale vs Gauche moderee | 0.1724404437004443 |
| 2024-04 | Gauche radicale vs Centre / Majorite | 0.196612999572754 |
| 2024-04 | Gauche radicale vs Droite | 0.2733187413049606 |
| 2024-04 | Gauche moderee vs Centre / Majorite | 0.2685949305025477 |
| 2024-04 | Gauche moderee vs Droite | 0.3177107831061754 |
| 2024-04 | Centre / Majorite vs Droite | 0.2080246253677181 |
| 2024-05 | Gauche radicale vs Gauche moderee | 0.1167289736321299 |
| 2024-05 | Gauche radicale vs Centre / Majorite | 0.1956371079284665 |
| 2024-05 | Gauche radicale vs Droite | 0.2824260175303831 |
| 2024-05 | Gauche moderee vs Centre / Majorite | 0.2289800002012201 |
| 2024-05 | Gauche moderee vs Droite | 0.3327500208347648 |
| 2024-05 | Centre / Majorite vs Droite | 0.2295795080194801 |
| 2024-06 | Gauche radicale vs Gauche moderee | 0.163215066738412 |
| 2024-06 | Gauche radicale vs Centre / Majorite | 0.2016978937307074 |
| 2024-06 | Gauche radicale vs Droite | 0.2889309143429094 |
| 2024-06 | Gauche moderee vs Centre / Majorite | 0.2096607671873076 |
| 2024-06 | Gauche moderee vs Droite | 0.3389863912418605 |
| 2024-06 | Centre / Majorite vs Droite | 0.2278324959352384 |
| 2024-07 | Gauche radicale vs Gauche moderee | 0.2675276755785779 |
| 2024-07 | Gauche radicale vs Centre / Majorite | 0.2694674792903111 |
| 2024-07 | Gauche radicale vs Droite | 0.2838990975489134 |
| 2024-07 | Gauche moderee vs Centre / Majorite | 0.3852974015546192 |
| 2024-07 | Gauche moderee vs Droite | 0.3711246306561818 |
| 2024-07 | Centre / Majorite vs Droite | 0.22209384700106 |
| 2024-08 | Gauche radicale vs Gauche moderee | 0.2409619643227251 |
| 2024-08 | Gauche radicale vs Centre / Majorite | 0.2250150017001277 |
| 2024-08 | Gauche radicale vs Droite | 0.2639831548578069 |
| 2024-08 | Gauche moderee vs Centre / Majorite | 0.3004833641465324 |
| 2024-08 | Gauche moderee vs Droite | 0.3205846399517225 |
| 2024-08 | Centre / Majorite vs Droite | 0.1976751938811353 |
| 2024-09 | Gauche radicale vs Gauche moderee | 0.2350531004976256 |
| 2024-09 | Gauche radicale vs Centre / Majorite | 0.308083865764392 |
| 2024-09 | Gauche radicale vs Droite | 0.2992135386401579 |
| 2024-09 | Gauche moderee vs Centre / Majorite | 0.4464987482959354 |
| 2024-09 | Gauche moderee vs Droite | 0.408446850730911 |
| 2024-09 | Centre / Majorite vs Droite | 0.2783613351668289 |
| 2024-10 | Gauche radicale vs Gauche moderee | 0.2242883881152393 |
| 2024-10 | Gauche radicale vs Centre / Majorite | 0.1911588411142462 |
| 2024-10 | Gauche radicale vs Droite | 0.2000313587319796 |
| 2024-10 | Gauche moderee vs Centre / Majorite | 0.3008478938536335 |
| 2024-10 | Gauche moderee vs Droite | 0.3148694646271827 |
| 2024-10 | Centre / Majorite vs Droite | 0.1449871860464423 |
| 2024-11 | Gauche radicale vs Gauche moderee | 0.1580585294856376 |
| 2024-11 | Gauche radicale vs Centre / Majorite | 0.2060046018558523 |
| 2024-11 | Gauche radicale vs Droite | 0.210887420595671 |
| 2024-11 | Gauche moderee vs Centre / Majorite | 0.2894297755278755 |
| 2024-11 | Gauche moderee vs Droite | 0.3011172512879199 |
| 2024-11 | Centre / Majorite vs Droite | 0.2127662782473057 |
| 2024-12 | Gauche radicale vs Gauche moderee | 0.2733256800745948 |
| 2024-12 | Gauche radicale vs Centre / Majorite | 0.4050082103505374 |
| 2024-12 | Gauche radicale vs Droite | 0.2217760240401389 |
| 2024-12 | Gauche moderee vs Centre / Majorite | 0.5572344060469755 |
| 2024-12 | Gauche moderee vs Droite | 0.3659622435030394 |
| 2024-12 | Centre / Majorite vs Droite | 0.3809626311146726 |
| 2025-01 | Gauche radicale vs Gauche moderee | 0.1894090371870362 |
| 2025-01 | Gauche radicale vs Centre / Majorite | 0.1569242534058176 |
| 2025-01 | Gauche radicale vs Droite | 0.2612510635406645 |
| 2025-01 | Gauche moderee vs Centre / Majorite | 0.2107272474964342 |
| 2025-01 | Gauche moderee vs Droite | 0.330682063897284 |
| 2025-01 | Centre / Majorite vs Droite | 0.2182588121295425 |
| 2025-02 | Gauche radicale vs Gauche moderee | 0.2411699144622566 |
| 2025-02 | Gauche radicale vs Centre / Majorite | 0.2436597217216416 |
| 2025-02 | Gauche radicale vs Droite | 0.2891437476161747 |
| 2025-02 | Gauche moderee vs Centre / Majorite | 0.3683450568710626 |
| 2025-02 | Gauche moderee vs Droite | 0.3794893151331767 |
| 2025-02 | Centre / Majorite vs Droite | 0.1749433354137375 |
| 2025-03 | Gauche radicale vs Gauche moderee | 0.2087649353002129 |
| 2025-03 | Gauche radicale vs Centre / Majorite | 0.1827244491742886 |
| 2025-03 | Gauche radicale vs Droite | 0.2820455794902023 |
| 2025-03 | Gauche moderee vs Centre / Majorite | 0.2763606745878786 |
| 2025-03 | Gauche moderee vs Droite | 0.3931436879791751 |
| 2025-03 | Centre / Majorite vs Droite | 0.2288422687797899 |
| 2025-04 | Gauche radicale vs Gauche moderee | 0.2097146319882732 |
| 2025-04 | Gauche radicale vs Centre / Majorite | 0.2206800241258999 |
| 2025-04 | Gauche radicale vs Droite | 0.3148960542737652 |
| 2025-04 | Gauche moderee vs Centre / Majorite | 0.2675292073160675 |
| 2025-04 | Gauche moderee vs Droite | 0.3973552735846135 |
| 2025-04 | Centre / Majorite vs Droite | 0.363649483340733 |
| 2025-05 | Gauche radicale vs Gauche moderee | 0.154316259795651 |
| 2025-05 | Gauche radicale vs Centre / Majorite | 0.1603564865364891 |
| 2025-05 | Gauche radicale vs Droite | 0.2288514015597158 |
| 2025-05 | Gauche moderee vs Centre / Majorite | 0.1863885169888267 |
| 2025-05 | Gauche moderee vs Droite | 0.2756788490993908 |
| 2025-05 | Centre / Majorite vs Droite | 0.1427452940311123 |
| 2025-06 | Gauche radicale vs Gauche moderee | 0.1385743496516824 |
| 2025-06 | Gauche radicale vs Centre / Majorite | 0.1589831956655224 |
| 2025-06 | Gauche radicale vs Droite | 0.2158095827028452 |
| 2025-06 | Gauche moderee vs Centre / Majorite | 0.1634614041782305 |
| 2025-06 | Gauche moderee vs Droite | 0.2344413631096998 |
| 2025-06 | Centre / Majorite vs Droite | 0.1650464379158175 |
| 2025-07 | Gauche radicale vs Gauche moderee | 0.1602739816200105 |
| 2025-07 | Gauche radicale vs Centre / Majorite | 0.260319517797306 |
| 2025-07 | Gauche radicale vs Droite | 0.2366827006958385 |
| 2025-07 | Gauche moderee vs Centre / Majorite | 0.3204844707937551 |
| 2025-07 | Gauche moderee vs Droite | 0.3035102171115845 |
| 2025-07 | Centre / Majorite vs Droite | 0.2056004877463561 |
| 2025-08 | Gauche radicale vs Gauche moderee | 0.2136010708104535 |
| 2025-08 | Gauche radicale vs Centre / Majorite | 0.2671808063696768 |
| 2025-08 | Gauche radicale vs Droite | 0.274772545330703 |
| 2025-08 | Gauche moderee vs Centre / Majorite | 0.3236520764933054 |
| 2025-08 | Gauche moderee vs Droite | 0.3591025624924636 |
| 2025-08 | Centre / Majorite vs Droite | 0.2497689779799068 |
| 2025-09 | Gauche radicale vs Gauche moderee | 0.1480206746080254 |
| 2025-09 | Gauche radicale vs Centre / Majorite | 0.2955697650046867 |
| 2025-09 | Gauche radicale vs Droite | 0.2791616519825173 |
| 2025-09 | Gauche moderee vs Centre / Majorite | 0.274334025408502 |
| 2025-09 | Gauche moderee vs Droite | 0.2755007930168553 |
| 2025-09 | Centre / Majorite vs Droite | 0.3253768743274741 |
| 2025-10 | Gauche radicale vs Gauche moderee | 0.4033544397459742 |
| 2025-10 | Gauche radicale vs Centre / Majorite | 0.2097656367278856 |
| 2025-10 | Gauche radicale vs Droite | 0.2275065839785773 |
| 2025-10 | Gauche moderee vs Centre / Majorite | 0.2786535642759892 |
| 2025-10 | Gauche moderee vs Droite | 0.3366234363410756 |
| 2025-10 | Centre / Majorite vs Droite | 0.1715389957264996 |
| 2025-11 | Gauche radicale vs Gauche moderee | 0.2463624910903535 |
| 2025-11 | Gauche radicale vs Centre / Majorite | 0.2486996906591989 |
| 2025-11 | Gauche radicale vs Droite | 0.2483141056505804 |
| 2025-11 | Gauche moderee vs Centre / Majorite | 0.2902515030766261 |
| 2025-11 | Gauche moderee vs Droite | 0.3162901331321651 |
| 2025-11 | Centre / Majorite vs Droite | 0.3550515545821985 |
| 2025-12 | Gauche radicale vs Gauche moderee | 0.2525835283554573 |
| 2025-12 | Gauche radicale vs Centre / Majorite | 0.2427500607561188 |
| 2025-12 | Gauche radicale vs Droite | 0.2912778373966361 |
| 2025-12 | Gauche moderee vs Centre / Majorite | 0.2148448708335678 |
| 2025-12 | Gauche moderee vs Droite | 0.3187931664777793 |
| 2025-12 | Centre / Majorite vs Droite | 0.2853324831719507 |
| 2026-01 | Gauche radicale vs Centre / Majorite | 0.464278986068097 |


### fighting_words.csv (25700 lignes)

| word | z |
| --- | --- |
| hamas | -34.85815844185399 |
| gaza | 25.541178897028452 |
| génocide | 20.95080818947475 |
| terroristes | -18.735412188027265 |
| otages | -18.40415462969712 |
| antisémitisme | -18.39117129574193 |
| octobre | -18.34701115216254 |
| haine | -17.24766202291567 |
| juifs | -16.716947320215755 |
| nos | -16.676371230564573 |
| lfi | -15.658885316524517 |
| terroriste | -15.63837459494038 |
| palestine | 15.30213878147843 |
| gouvernement | 15.185767439602634 |
| massacres | 14.509773823096833 |
| cessez | 14.172267993484924 |
| feu | 13.942023935002643 |
| compatriotes | -13.159846929382033 |
| palestiniens | 12.90202872313242 |
| netanyahou | 12.826532101788468 |
| armée | 12.715545788941528 |
| terrorisme | -12.682872310623411 |
| israélienne | 12.583339126712628 |
| guerre | 12.318736952880249 |
| islamiste | -11.78399254792432 |
| ... | ... |
| violemment | -0.0153578373284635 |
| ouvre | -0.0153578373284635 |
| cessé | -0.0153578373284635 |
| mairies | -0.0153578373284635 |
| témoigne | -0.0153578373284635 |
| longue | -0.0153578373284635 |
| gendarmes | -0.0153578373284635 |
| mais | -0.0146111506752316 |
| accès | 0.0098664010949457 |
| votre | -0.0094810620147397 |
| seule | -0.0087589165626596 |
| sortir | -0.0075444862904349 |
| attention | 0.0063894309307057 |
| colonna | 0.0036879116536494 |
| tes | 0.0036879116536494 |
| échelle | 0.0036879116536494 |
| préfet | 0.0036879116536494 |
| attal | 0.0036879116536494 |
| confiance | 0.0036879116536494 |
| changer | 0.0036879116536494 |
| décès | 0.0036879116536494 |
| comprend | 0.0036879116536494 |
| venue | 0.0036879116536494 |
| sort | -0.0032074305210645 |

*(tronqué à 50 lignes — voir CSV pour données complètes)*


### ceasefire_lexical.csv (112 lignes)

| month | bloc | pct | n | month_ts |
| --- | --- | --- | --- | --- |
| 2023-10 | Centre / Majorite | 0.0313725490196078 | 255 | 2023-10-01 |
| 2023-10 | Droite | 0.0233333333333333 | 300 | 2023-10-01 |
| 2023-10 | Gauche moderee | 0.2026143790849673 | 153 | 2023-10-01 |
| 2023-10 | Gauche radicale | 0.2325581395348837 | 645 | 2023-10-01 |
| 2023-11 | Centre / Majorite | 0.0654205607476635 | 107 | 2023-11-01 |
| 2023-11 | Droite | 0.0186915887850467 | 107 | 2023-11-01 |
| 2023-11 | Gauche moderee | 0.3090909090909091 | 55 | 2023-11-01 |
| 2023-11 | Gauche radicale | 0.3192771084337349 | 332 | 2023-11-01 |
| 2023-12 | Centre / Majorite | 0.3 | 10 | 2023-12-01 |
| 2023-12 | Droite | 0.0 | 16 | 2023-12-01 |
| 2023-12 | Gauche moderee | 0.1875 | 16 | 2023-12-01 |
| 2023-12 | Gauche radicale | 0.1273885350318471 | 157 | 2023-12-01 |
| 2024-01 | Centre / Majorite | 0.03125 | 64 | 2024-01-01 |
| 2024-01 | Droite | 0.0 | 32 | 2024-01-01 |
| 2024-01 | Gauche moderee | 0.3 | 30 | 2024-01-01 |
| 2024-01 | Gauche radicale | 0.1814159292035398 | 226 | 2024-01-01 |
| 2024-02 | Centre / Majorite | 0.0615384615384615 | 65 | 2024-02-01 |
| 2024-02 | Droite | 0.03125 | 32 | 2024-02-01 |
| 2024-02 | Gauche moderee | 0.1818181818181818 | 55 | 2024-02-01 |
| 2024-02 | Gauche radicale | 0.2311111111111111 | 225 | 2024-02-01 |
| 2024-03 | Centre / Majorite | 0.0425531914893617 | 47 | 2024-03-01 |
| 2024-03 | Droite | 0.0 | 73 | 2024-03-01 |
| 2024-03 | Gauche moderee | 0.2727272727272727 | 44 | 2024-03-01 |
| 2024-03 | Gauche radicale | 0.2304526748971193 | 243 | 2024-03-01 |
| 2024-04 | Centre / Majorite | 0.0784313725490196 | 51 | 2024-04-01 |
| 2024-04 | Droite | 0.0196078431372549 | 51 | 2024-04-01 |
| 2024-04 | Gauche moderee | 0.1627906976744186 | 43 | 2024-04-01 |
| 2024-04 | Gauche radicale | 0.1747851002865329 | 349 | 2024-04-01 |
| 2024-05 | Centre / Majorite | 0.1442307692307692 | 104 | 2024-05-01 |
| 2024-05 | Droite | 0.0317460317460317 | 63 | 2024-05-01 |
| 2024-05 | Gauche moderee | 0.0869565217391304 | 92 | 2024-05-01 |
| 2024-05 | Gauche radicale | 0.0921052631578947 | 608 | 2024-05-01 |
| 2024-06 | Centre / Majorite | 0.0384615384615384 | 52 | 2024-06-01 |
| 2024-06 | Droite | 0.0 | 25 | 2024-06-01 |
| 2024-06 | Gauche moderee | 0.0833333333333333 | 24 | 2024-06-01 |
| 2024-06 | Gauche radicale | 0.1349206349206349 | 126 | 2024-06-01 |
| 2024-07 | Centre / Majorite | 0.074074074074074 | 27 | 2024-07-01 |
| 2024-07 | Droite | 0.0 | 40 | 2024-07-01 |
| 2024-07 | Gauche moderee | 0.1428571428571428 | 14 | 2024-07-01 |
| 2024-07 | Gauche radicale | 0.1226993865030674 | 163 | 2024-07-01 |
| 2024-08 | Centre / Majorite | 0.0285714285714285 | 35 | 2024-08-01 |
| 2024-08 | Droite | 0.0 | 34 | 2024-08-01 |
| 2024-08 | Gauche moderee | 0.125 | 16 | 2024-08-01 |
| 2024-08 | Gauche radicale | 0.0202020202020202 | 99 | 2024-08-01 |
| 2024-09 | Centre / Majorite | 0.1333333333333333 | 15 | 2024-09-01 |
| 2024-09 | Droite | 0.0 | 19 | 2024-09-01 |
| 2024-09 | Gauche moderee | 0.0952380952380952 | 21 | 2024-09-01 |
| 2024-09 | Gauche radicale | 0.0977777777777777 | 225 | 2024-09-01 |
| 2024-10 | Centre / Majorite | 0.1571428571428571 | 70 | 2024-10-01 |
| 2024-10 | Droite | 0.0326086956521739 | 92 | 2024-10-01 |
| 2024-10 | Gauche moderee | 0.0 | 23 | 2024-10-01 |
| 2024-10 | Gauche radicale | 0.152 | 250 | 2024-10-01 |
| 2024-11 | Centre / Majorite | 0.0333333333333333 | 30 | 2024-11-01 |
| 2024-11 | Droite | 0.0697674418604651 | 43 | 2024-11-01 |
| 2024-11 | Gauche moderee | 0.0263157894736842 | 38 | 2024-11-01 |
| 2024-11 | Gauche radicale | 0.0669856459330143 | 209 | 2024-11-01 |
| 2024-12 | Centre / Majorite | 0.1666666666666666 | 6 | 2024-12-01 |
| 2024-12 | Droite | 0.1333333333333333 | 15 | 2024-12-01 |
| 2024-12 | Gauche moderee | 0.1 | 10 | 2024-12-01 |
| 2024-12 | Gauche radicale | 0.0194174757281553 | 103 | 2024-12-01 |
| 2025-01 | Centre / Majorite | 0.2926829268292683 | 41 | 2025-01-01 |
| 2025-01 | Droite | 0.0 | 31 | 2025-01-01 |
| 2025-01 | Gauche moderee | 0.2413793103448276 | 29 | 2025-01-01 |
| 2025-01 | Gauche radicale | 0.2385321100917431 | 218 | 2025-01-01 |
| 2025-02 | Centre / Majorite | 0.0227272727272727 | 44 | 2025-02-01 |
| 2025-02 | Droite | 0.0 | 45 | 2025-02-01 |
| 2025-02 | Gauche moderee | 0.0 | 12 | 2025-02-01 |
| 2025-02 | Gauche radicale | 0.0135135135135135 | 74 | 2025-02-01 |
| 2025-03 | Centre / Majorite | 0.1063829787234042 | 47 | 2025-03-01 |
| 2025-03 | Droite | 0.0 | 41 | 2025-03-01 |
| 2025-03 | Gauche moderee | 0.1666666666666666 | 18 | 2025-03-01 |
| 2025-03 | Gauche radicale | 0.1788079470198675 | 151 | 2025-03-01 |
| 2025-04 | Centre / Majorite | 0.1153846153846153 | 26 | 2025-04-01 |
| 2025-04 | Droite | 0.0 | 24 | 2025-04-01 |
| 2025-04 | Gauche moderee | 0.0714285714285714 | 14 | 2025-04-01 |
| 2025-04 | Gauche radicale | 0.0521739130434782 | 230 | 2025-04-01 |
| 2025-05 | Centre / Majorite | 0.0655737704918032 | 122 | 2025-05-01 |
| 2025-05 | Droite | 0.0 | 74 | 2025-05-01 |
| 2025-05 | Gauche moderee | 0.04 | 50 | 2025-05-01 |
| 2025-05 | Gauche radicale | 0.0226537216828478 | 309 | 2025-05-01 |
| 2025-06 | Centre / Majorite | 0.0862068965517241 | 116 | 2025-06-01 |
| 2025-06 | Droite | 0.0099009900990099 | 101 | 2025-06-01 |
| 2025-06 | Gauche moderee | 0.0526315789473684 | 57 | 2025-06-01 |
| 2025-06 | Gauche radicale | 0.0218978102189781 | 548 | 2025-06-01 |
| 2025-07 | Centre / Majorite | 0.032258064516129 | 31 | 2025-07-01 |
| 2025-07 | Droite | 0.0 | 77 | 2025-07-01 |
| 2025-07 | Gauche moderee | 0.0285714285714285 | 35 | 2025-07-01 |
| 2025-07 | Gauche radicale | 0.0259365994236311 | 347 | 2025-07-01 |
| 2025-08 | Centre / Majorite | 0.0 | 14 | 2025-08-01 |
| 2025-08 | Droite | 0.0 | 22 | 2025-08-01 |
| 2025-08 | Gauche moderee | 0.0 | 20 | 2025-08-01 |
| 2025-08 | Gauche radicale | 0.0157480314960629 | 127 | 2025-08-01 |
| 2025-09 | Centre / Majorite | 0.0476190476190476 | 21 | 2025-09-01 |
| 2025-09 | Droite | 0.0 | 47 | 2025-09-01 |
| 2025-09 | Gauche moderee | 0.0526315789473684 | 57 | 2025-09-01 |
| 2025-09 | Gauche radicale | 0.0116618075801749 | 343 | 2025-09-01 |
| 2025-10 | Centre / Majorite | 0.087719298245614 | 57 | 2025-10-01 |
| 2025-10 | Droite | 0.025 | 40 | 2025-10-01 |
| 2025-10 | Gauche moderee | 0.0 | 10 | 2025-10-01 |
| 2025-10 | Gauche radicale | 0.1423076923076923 | 260 | 2025-10-01 |
| 2025-11 | Centre / Majorite | 0.2 | 10 | 2025-11-01 |
| 2025-11 | Droite | 0.0 | 17 | 2025-11-01 |
| 2025-11 | Gauche moderee | 0.0526315789473684 | 19 | 2025-11-01 |
| 2025-11 | Gauche radicale | 0.1287128712871287 | 101 | 2025-11-01 |
| 2025-12 | Centre / Majorite | 0.0 | 14 | 2025-12-01 |
| 2025-12 | Droite | 0.0 | 11 | 2025-12-01 |
| 2025-12 | Gauche moderee | 0.0 | 15 | 2025-12-01 |
| 2025-12 | Gauche radicale | 0.0309278350515463 | 97 | 2025-12-01 |
| 2026-01 | Centre / Majorite | 0.0 | 8 | 2026-01-01 |
| 2026-01 | Droite | 0.0 | 4 | 2026-01-01 |
| 2026-01 | Gauche moderee | 0.0 | 1 | 2026-01-01 |
| 2026-01 | Gauche radicale | 0.0684931506849315 | 73 | 2026-01-01 |


### polarisation_index.csv (28 lignes)

| month | dist | month_ts | wd_mean |
| --- | --- | --- | --- |
| 2023-10 | 0.1459008763320844 | 2023-10-01 | 0.4033519531843745 |
| 2023-11 | 0.2345034169166628 | 2023-11-01 | 0.382457484995206 |
| 2023-12 | 0.2736850488190176 | 2023-12-01 | 0.3780918259023354 |
| 2024-01 | 0.2821323851387614 | 2024-01-01 | 0.4755054695181908 |
| 2024-02 | 0.2495555176484597 | 2024-02-01 | 0.4525704156954157 |
| 2024-03 | 0.2363500467110618 | 2024-03-01 | 0.4932308544367575 |
| 2024-04 | 0.2394504205924333 | 2024-04-01 | 0.4281625546422563 |
| 2024-05 | 0.2310169380244074 | 2024-05-01 | 0.4827671970478034 |
| 2024-06 | 0.2383872548627392 | 2024-06-01 | 0.4436454517704518 |
| 2024-07 | 0.2999016886049439 | 2024-07-01 | 0.4901816821934409 |
| 2024-08 | 0.2581172198100083 | 2024-08-01 | 0.4531653633675692 |
| 2024-09 | 0.3292762398493085 | 2024-09-01 | 0.4635867446393762 |
| 2024-10 | 0.2293638554147873 | 2024-10-01 | 0.4339327122153209 |
| 2024-11 | 0.229710642833377 | 2024-11-01 | 0.4457925336597307 |
| 2024-12 | 0.3673781991883265 | 2024-12-01 | 0.4186084142394822 |
| 2025-01 | 0.2278754129427965 | 2025-01-01 | 0.3558444951763863 |
| 2025-02 | 0.2827918485363416 | 2025-02-01 | 0.4425948675948676 |
| 2025-03 | 0.2619802658852579 | 2025-03-01 | 0.4323980153579658 |
| 2025-04 | 0.2956374457715587 | 2025-04-01 | 0.4590106903965599 |
| 2025-05 | 0.1913894680018643 | 2025-05-01 | 0.4401728208393018 |
| 2025-06 | 0.1793860555372997 | 2025-06-01 | 0.4390356323128836 |
| 2025-07 | 0.2478118959608084 | 2025-07-01 | 0.4859035513771964 |
| 2025-08 | 0.2813463399127515 | 2025-08-01 | 0.5314743327538604 |
| 2025-09 | 0.2663272973913435 | 2025-09-01 | 0.4276339821909673 |
| 2025-10 | 0.2712404427993336 | 2025-10-01 | 0.3892487629329734 |
| 2025-11 | 0.2841615796985204 | 2025-11-01 | 0.4410451726287179 |
| 2025-12 | 0.2675969911652516 | 2025-12-01 | 0.4134046652087889 |
| 2026-01 | 0.464278986068097 | 2026-01-01 | 0.4888698630136986 |


### entropic_polarization_temporal.csv (28 lignes)

| month | Ec | n | month_ts |
| --- | --- | --- | --- |
| 2023-10 | 0.8382978873848583 | 1353 | 2023-10-01 |
| 2023-11 | 0.7741668149744538 | 601 | 2023-11-01 |
| 2023-12 | 0.6055089246326147 | 199 | 2023-12-01 |
| 2024-01 | 0.7154304554054514 | 352 | 2024-01-01 |
| 2024-02 | 0.7206322806530361 | 377 | 2024-02-01 |
| 2024-03 | 0.818690920825804 | 407 | 2024-03-01 |
| 2024-04 | 0.7020726744884833 | 494 | 2024-04-01 |
| 2024-05 | 0.627946305783156 | 867 | 2024-05-01 |
| 2024-06 | 0.7862196981649714 | 227 | 2024-06-01 |
| 2024-07 | 0.7951590107436803 | 244 | 2024-07-01 |
| 2024-08 | 0.8832900974557781 | 184 | 2024-08-01 |
| 2024-09 | 0.6218823102777602 | 280 | 2024-09-01 |
| 2024-10 | 0.8124164530357971 | 435 | 2024-10-01 |
| 2024-11 | 0.7050524956575235 | 320 | 2024-11-01 |
| 2024-12 | 0.5081824233177212 | 134 | 2024-12-01 |
| 2025-01 | 0.6554850036192769 | 319 | 2025-01-01 |
| 2025-02 | 0.9030068174503602 | 175 | 2025-02-01 |
| 2025-03 | 0.8317803819845829 | 257 | 2025-03-01 |
| 2025-04 | 0.6238586581604644 | 294 | 2025-04-01 |
| 2025-05 | 0.822316738222008 | 555 | 2025-05-01 |
| 2025-06 | 0.7239525327471801 | 822 | 2025-06-01 |
| 2025-07 | 0.707356026151066 | 490 | 2025-07-01 |
| 2025-08 | 0.6968718894393049 | 183 | 2025-08-01 |
| 2025-09 | 0.569500335870049 | 468 | 2025-09-01 |
| 2025-10 | 0.7363509509347868 | 367 | 2025-10-01 |
| 2025-11 | 0.6642164314792016 | 147 | 2025-11-01 |
| 2025-12 | 0.7495209863092727 | 137 | 2025-12-01 |
| 2026-01 | 0.732111787207598 | 86 | 2026-01-01 |


### effective_dimensionality_temporal.csv (28 lignes)

| month | ED | n | n_feat | month_ts |
| --- | --- | --- | --- | --- |
| 2023-10 | 2.559490257152955 | 211 | 3 | 2023-10-01 |
| 2023-11 | 2.7319462683775653 | 148 | 3 | 2023-11-01 |
| 2023-12 | 2.837152753360752 | 55 | 3 | 2023-12-01 |
| 2024-01 | 2.719614079287098 | 91 | 3 | 2024-01-01 |
| 2024-02 | 2.6952147843613323 | 95 | 3 | 2024-02-01 |
| 2024-03 | 2.806815365465207 | 103 | 3 | 2024-03-01 |
| 2024-04 | 2.7112995460670586 | 104 | 3 | 2024-04-01 |
| 2024-05 | 2.8946130776745718 | 130 | 3 | 2024-05-01 |
| 2024-06 | 2.8840033443032937 | 79 | 3 | 2024-06-01 |
| 2024-07 | 2.895820782672112 | 64 | 3 | 2024-07-01 |
| 2024-08 | 2.8653657119431526 | 59 | 3 | 2024-08-01 |
| 2024-09 | 2.92617133605728 | 57 | 3 | 2024-09-01 |
| 2024-10 | 2.894629043142809 | 116 | 3 | 2024-10-01 |
| 2024-11 | 2.8798753932855745 | 87 | 3 | 2024-11-01 |
| 2024-12 | 2.9046362988438204 | 45 | 3 | 2024-12-01 |
| 2025-01 | 2.929232275466596 | 96 | 3 | 2025-01-01 |
| 2025-02 | 2.96265290259829 | 70 | 3 | 2025-02-01 |
| 2025-03 | 2.8526600184645554 | 87 | 3 | 2025-03-01 |
| 2025-04 | 2.912690442677865 | 64 | 3 | 2025-04-01 |
| 2025-05 | 2.889354487818196 | 124 | 3 | 2025-05-01 |
| 2025-06 | 2.8854507960413853 | 137 | 3 | 2025-06-01 |
| 2025-07 | 2.914672650524401 | 109 | 3 | 2025-07-01 |
| 2025-08 | 2.9101581982186246 | 49 | 3 | 2025-08-01 |
| 2025-09 | 2.967394832385147 | 85 | 3 | 2025-09-01 |
| 2025-10 | 2.864925950967949 | 87 | 3 | 2025-10-01 |
| 2025-11 | 2.9326384959468816 | 60 | 3 | 2025-11-01 |
| 2025-12 | 2.930822505229361 | 52 | 3 | 2025-12-01 |
| 2026-01 | 2.904124483723502 | 34 | 3 | 2026-01-01 |


### affective_vad_by_bloc_month.csv (110 lignes)

| month | bloc | valence | arousal | dominance | n | month_ts |
| --- | --- | --- | --- | --- | --- | --- |
| 2023-10 | Centre / Majorite | 0.5061757649711679 | 0.5006819194730868 | 0.5043001613101281 | 251 | 2023-10-01 |
| 2023-10 | Droite | 0.4936229135304992 | 0.5036957972866022 | 0.4896479758825564 | 300 | 2023-10-01 |
| 2023-10 | Gauche moderee | 0.4938820848820306 | 0.5007803571451084 | 0.4970148940610674 | 153 | 2023-10-01 |
| 2023-10 | Gauche radicale | 0.5010706422006416 | 0.4996817639689738 | 0.4994507572332283 | 644 | 2023-10-01 |
| 2023-11 | Centre / Majorite | 0.5280295831950552 | 0.4903753145353323 | 0.5009002627423516 | 106 | 2023-11-01 |
| 2023-11 | Droite | 0.5114550137740949 | 0.4911142804025358 | 0.4824342178654648 | 107 | 2023-11-01 |
| 2023-11 | Gauche moderee | 0.5291797579735865 | 0.4767586031948654 | 0.5008047282019786 | 55 | 2023-11-01 |
| 2023-11 | Gauche radicale | 0.5199754402481995 | 0.4959019563536896 | 0.5026828582574175 | 331 | 2023-11-01 |
| 2023-12 | Centre / Majorite | 0.5094119810315431 | 0.4865149023159988 | 0.4878941476142499 | 10 | 2023-12-01 |
| 2023-12 | Droite | 0.5392249674825916 | 0.4551450686279621 | 0.4883942429707488 | 16 | 2023-12-01 |
| 2023-12 | Gauche moderee | 0.5103756232200033 | 0.4893939002349973 | 0.4834291391026217 | 16 | 2023-12-01 |
| 2023-12 | Gauche radicale | 0.5074855299057552 | 0.4938939603011866 | 0.4939448306770648 | 157 | 2023-12-01 |
| 2024-01 | Centre / Majorite | 0.5219502536698063 | 0.4931304410914532 | 0.5102222394992221 | 64 | 2024-01-01 |
| 2024-01 | Droite | 0.5222324090187603 | 0.4791724253344506 | 0.4741776146016628 | 32 | 2024-01-01 |
| 2024-01 | Gauche moderee | 0.5172481424484197 | 0.4940233686163955 | 0.5103396142988154 | 30 | 2024-01-01 |
| 2024-01 | Gauche radicale | 0.5039078520438093 | 0.5010722464609931 | 0.5077139767760731 | 226 | 2024-01-01 |
| 2024-02 | Centre / Majorite | 0.5156480413949838 | 0.4886770654133469 | 0.4928280592261448 | 65 | 2024-02-01 |
| 2024-02 | Droite | 0.5157749766675704 | 0.4876339778576993 | 0.4981943280448661 | 32 | 2024-02-01 |
| 2024-02 | Gauche moderee | 0.5261228286141814 | 0.4801912057873108 | 0.5020207319760317 | 55 | 2024-02-01 |
| 2024-02 | Gauche radicale | 0.5102405650695748 | 0.4998256556793394 | 0.5022578852433176 | 224 | 2024-02-01 |
| 2024-03 | Centre / Majorite | 0.5257309350115184 | 0.4834575932787551 | 0.5066399210234452 | 47 | 2024-03-01 |
| 2024-03 | Droite | 0.5282015685125094 | 0.4793229681260407 | 0.5023967228754888 | 73 | 2024-03-01 |
| 2024-03 | Gauche moderee | 0.5170699359682488 | 0.4922737028997959 | 0.5096565112319112 | 44 | 2024-03-01 |
| 2024-03 | Gauche radicale | 0.5093913378726295 | 0.4996284913487198 | 0.508554970911784 | 243 | 2024-03-01 |
| 2024-04 | Centre / Majorite | 0.5304240452527896 | 0.4891143615710174 | 0.5084370102999737 | 51 | 2024-04-01 |
| 2024-04 | Droite | 0.5111493259565215 | 0.5108482834592455 | 0.499515397627615 | 51 | 2024-04-01 |
| 2024-04 | Gauche moderee | 0.5183424598642714 | 0.4999832294598786 | 0.5136586272200759 | 43 | 2024-04-01 |
| 2024-04 | Gauche radicale | 0.5068245328420565 | 0.4948243755166919 | 0.4971847179606002 | 349 | 2024-04-01 |
| 2024-05 | Centre / Majorite | 0.5222684008490716 | 0.4827342917623985 | 0.5011314253844379 | 104 | 2024-05-01 |
| 2024-05 | Droite | 0.5026184856788899 | 0.490988273014847 | 0.4788344599228868 | 63 | 2024-05-01 |
| 2024-05 | Gauche moderee | 0.5039144637903535 | 0.5047976932594241 | 0.5066446315520975 | 92 | 2024-05-01 |
| 2024-05 | Gauche radicale | 0.4958851679189024 | 0.5029225531581091 | 0.5010350847052746 | 608 | 2024-05-01 |
| 2024-06 | Centre / Majorite | 0.5220111742161397 | 0.4790792005720722 | 0.4911524429663848 | 52 | 2024-06-01 |
| 2024-06 | Droite | 0.5295680336885337 | 0.50930474935522 | 0.5013388568294451 | 25 | 2024-06-01 |
| 2024-06 | Gauche moderee | 0.4817288710504197 | 0.4904660344384024 | 0.4901845734137471 | 24 | 2024-06-01 |
| 2024-06 | Gauche radicale | 0.5056448680999587 | 0.5014224151103218 | 0.5053524843360966 | 126 | 2024-06-01 |
| 2024-07 | Centre / Majorite | 0.532672647644233 | 0.4846958614361905 | 0.4908105487968964 | 27 | 2024-07-01 |
| 2024-07 | Droite | 0.5159492990236992 | 0.5140892236228537 | 0.5027182021010862 | 39 | 2024-07-01 |
| 2024-07 | Gauche moderee | 0.5140087825248677 | 0.4671520415873859 | 0.4987810485854421 | 14 | 2024-07-01 |
| 2024-07 | Gauche radicale | 0.501989305939211 | 0.5078416746396917 | 0.5054097347824176 | 162 | 2024-07-01 |
| 2024-08 | Centre / Majorite | 0.4961373516226856 | 0.495539532603363 | 0.497369201520622 | 35 | 2024-08-01 |
| 2024-08 | Droite | 0.5122348119004883 | 0.4981827896505437 | 0.4914881702593821 | 33 | 2024-08-01 |
| 2024-08 | Gauche moderee | 0.4939816366113092 | 0.4894907811039566 | 0.5057143290884588 | 16 | 2024-08-01 |
| 2024-08 | Gauche radicale | 0.4907208710739241 | 0.5055863205328639 | 0.5023151611378175 | 99 | 2024-08-01 |
| 2024-09 | Centre / Majorite | 0.4975033072143961 | 0.4981214037728421 | 0.4897156445711981 | 15 | 2024-09-01 |
| 2024-09 | Droite | 0.4906056483854349 | 0.5016447954074604 | 0.4750215234704644 | 19 | 2024-09-01 |
| 2024-09 | Gauche moderee | 0.4988433451544941 | 0.5122684601441618 | 0.4966365519159502 | 21 | 2024-09-01 |
| 2024-09 | Gauche radicale | 0.4863724106270455 | 0.5046132712029958 | 0.4975195776528092 | 224 | 2024-09-01 |
| 2024-10 | Centre / Majorite | 0.5059900414960747 | 0.5010872303591944 | 0.5018579158072057 | 70 | 2024-10-01 |
| 2024-10 | Droite | 0.5157699182089907 | 0.4936583666819231 | 0.4976483806833411 | 92 | 2024-10-01 |
| 2024-10 | Gauche moderee | 0.5026220290029197 | 0.5027009563708946 | 0.4977851801184856 | 23 | 2024-10-01 |
| 2024-10 | Gauche radicale | 0.5047047644384349 | 0.504426135021989 | 0.503834329931115 | 249 | 2024-10-01 |
| 2024-11 | Centre / Majorite | 0.5267413492597711 | 0.4901103885389916 | 0.5048255971090906 | 30 | 2024-11-01 |
| 2024-11 | Droite | 0.4998556238569995 | 0.4948868827133117 | 0.4920979612931397 | 43 | 2024-11-01 |
| 2024-11 | Gauche moderee | 0.522396920144998 | 0.491093725286384 | 0.5075290645362058 | 38 | 2024-11-01 |
| 2024-11 | Gauche radicale | 0.5113491295372171 | 0.4987849085176579 | 0.5053784446708952 | 207 | 2024-11-01 |
| 2024-12 | Centre / Majorite | 0.5269439717553688 | 0.4669036181139123 | 0.4858872315592904 | 6 | 2024-12-01 |
| 2024-12 | Droite | 0.5319490652106179 | 0.4988186861306334 | 0.5036360773349458 | 15 | 2024-12-01 |
| 2024-12 | Gauche moderee | 0.4916637322093111 | 0.4775471441672362 | 0.4810027219184324 | 10 | 2024-12-01 |
| 2024-12 | Gauche radicale | 0.494202972226072 | 0.4997068010333833 | 0.4995812541288364 | 103 | 2024-12-01 |
| 2025-01 | Centre / Majorite | 0.532214903558564 | 0.4752105840950015 | 0.4949538644635973 | 41 | 2025-01-01 |
| 2025-01 | Droite | 0.5026364174685397 | 0.4865582982880409 | 0.4909763138102904 | 31 | 2025-01-01 |
| 2025-01 | Gauche moderee | 0.5575011313892895 | 0.4710727300028507 | 0.5186316014500045 | 29 | 2025-01-01 |
| 2025-01 | Gauche radicale | 0.5041790531662059 | 0.4953382303877167 | 0.4969126809240187 | 218 | 2025-01-01 |
| 2025-02 | Centre / Majorite | 0.5131266798163435 | 0.4778411729368929 | 0.4807173755113456 | 44 | 2025-02-01 |
| 2025-02 | Droite | 0.4983762999702256 | 0.5023806227847883 | 0.4994154870763505 | 45 | 2025-02-01 |
| 2025-02 | Gauche moderee | 0.5205159443235858 | 0.4706784441020624 | 0.5009593422639774 | 12 | 2025-02-01 |
| 2025-02 | Gauche radicale | 0.5033766342331514 | 0.4969112693533218 | 0.4966176779689097 | 74 | 2025-02-01 |
| 2025-03 | Centre / Majorite | 0.5053324016456028 | 0.4938745915737728 | 0.4939350366297332 | 47 | 2025-03-01 |
| 2025-03 | Droite | 0.5125700707819327 | 0.4978194207237027 | 0.5034625260076098 | 41 | 2025-03-01 |
| 2025-03 | Gauche moderee | 0.5261281675027591 | 0.4787999233777113 | 0.4949336691481906 | 18 | 2025-03-01 |
| 2025-03 | Gauche radicale | 0.5060512931704131 | 0.4918276823295603 | 0.494259413089055 | 151 | 2025-03-01 |
| 2025-04 | Centre / Majorite | 0.505440854182431 | 0.5019952400737894 | 0.505329470238302 | 26 | 2025-04-01 |
| 2025-04 | Droite | 0.4996479591059841 | 0.5069234380174974 | 0.4876094336296127 | 24 | 2025-04-01 |
| 2025-04 | Gauche moderee | 0.517114375345758 | 0.4789440990366327 | 0.5001890898106884 | 14 | 2025-04-01 |
| 2025-04 | Gauche radicale | 0.5103326296063488 | 0.4974501627278787 | 0.493301274607764 | 229 | 2025-04-01 |
| 2025-05 | Centre / Majorite | 0.5326179166970789 | 0.4842532426072128 | 0.5066063071442839 | 122 | 2025-05-01 |
| 2025-05 | Droite | 0.5075132415436616 | 0.5040814357928362 | 0.5060345820495293 | 74 | 2025-05-01 |
| 2025-05 | Gauche moderee | 0.5166177350811838 | 0.4761845187526502 | 0.4959483417632945 | 50 | 2025-05-01 |
| 2025-05 | Gauche radicale | 0.4969586998348266 | 0.5045462098280508 | 0.5010111430796754 | 309 | 2025-05-01 |
| 2025-06 | Centre / Majorite | 0.5171238007163127 | 0.4867948157509823 | 0.5090423271015948 | 116 | 2025-06-01 |
| 2025-06 | Droite | 0.5091576945025853 | 0.4990729786632484 | 0.5136091907231026 | 101 | 2025-06-01 |
| 2025-06 | Gauche moderee | 0.5060069508214498 | 0.5026342397901612 | 0.5072216421452392 | 57 | 2025-06-01 |
| 2025-06 | Gauche radicale | 0.5106230345569541 | 0.4967500530267449 | 0.5120454145784765 | 545 | 2025-06-01 |
| 2025-07 | Centre / Majorite | 0.534709584709464 | 0.4824701933899055 | 0.5116036625716326 | 31 | 2025-07-01 |
| 2025-07 | Droite | 0.5234475865587271 | 0.4967823362864499 | 0.5078880249208915 | 77 | 2025-07-01 |
| 2025-07 | Gauche moderee | 0.5025879394590747 | 0.482464398514353 | 0.5030995382676794 | 35 | 2025-07-01 |
| 2025-07 | Gauche radicale | 0.515156392934261 | 0.4964309788755436 | 0.5063981883116586 | 346 | 2025-07-01 |
| 2025-08 | Centre / Majorite | 0.4782531581625821 | 0.4988825851971189 | 0.4912860814187926 | 14 | 2025-08-01 |
| 2025-08 | Droite | 0.5138074183971835 | 0.4977693544164691 | 0.49711476101384 | 22 | 2025-08-01 |
| 2025-08 | Gauche moderee | 0.5307960302709267 | 0.4865722300044147 | 0.5265202758352945 | 20 | 2025-08-01 |
| 2025-08 | Gauche radicale | 0.5089691599263794 | 0.5043041325186945 | 0.5087767666313895 | 124 | 2025-08-01 |
| 2025-09 | Centre / Majorite | 0.5331401412989443 | 0.4917975074200472 | 0.5308623819831916 | 21 | 2025-09-01 |
| 2025-09 | Droite | 0.5152102318380117 | 0.4929209484840481 | 0.5014776317920442 | 47 | 2025-09-01 |
| 2025-09 | Gauche moderee | 0.5305839099206884 | 0.4897906422166918 | 0.509949382153177 | 56 | 2025-09-01 |
| 2025-09 | Gauche radicale | 0.5090305872485542 | 0.4989617982071437 | 0.5119425969243812 | 342 | 2025-09-01 |
| 2025-10 | Centre / Majorite | 0.5130785298517675 | 0.4943640686943329 | 0.4972016355006673 | 57 | 2025-10-01 |
| 2025-10 | Droite | 0.4973452652426092 | 0.4948646076443814 | 0.4936995487933832 | 40 | 2025-10-01 |
| 2025-10 | Gauche moderee | 0.5048422985872904 | 0.528694637097557 | 0.5128269519979505 | 10 | 2025-10-01 |
| 2025-10 | Gauche radicale | 0.5126955363145571 | 0.4944538000499792 | 0.4998857052108795 | 260 | 2025-10-01 |
| 2025-11 | Centre / Majorite | 0.5167996379582481 | 0.4879822541836988 | 0.5324887208437303 | 10 | 2025-11-01 |
| 2025-11 | Droite | 0.5357517464465562 | 0.4871957100953641 | 0.5148787576610241 | 17 | 2025-11-01 |
| 2025-11 | Gauche moderee | 0.5475167087633653 | 0.4698918541147858 | 0.509232367334057 | 19 | 2025-11-01 |
| 2025-11 | Gauche radicale | 0.5132241114810344 | 0.4899177710257418 | 0.4939489630455627 | 101 | 2025-11-01 |
| 2025-12 | Centre / Majorite | 0.4842137021721326 | 0.518830717905289 | 0.4803166408841228 | 14 | 2025-12-01 |
| 2025-12 | Droite | 0.4866236248657342 | 0.4897845029094476 | 0.4903293294247026 | 11 | 2025-12-01 |
| 2025-12 | Gauche moderee | 0.4927542312102757 | 0.4893547624571468 | 0.4738847263268314 | 15 | 2025-12-01 |
| 2025-12 | Gauche radicale | 0.5166652271242772 | 0.498346215797936 | 0.5176577751775948 | 95 | 2025-12-01 |
| 2026-01 | Centre / Majorite | 0.5307360446570973 | 0.5310749601275917 | 0.4621726475279106 | 7 | 2026-01-01 |
| 2026-01 | Gauche radicale | 0.517712868510432 | 0.4950598119735705 | 0.517065075051711 | 73 | 2026-01-01 |


### affective_polarization_temporal.csv (28 lignes)

| month | gap_vad | month_ts |
| --- | --- | --- |
| 2023-10 | 0.0115792755724561 | 2023-10-01 |
| 2023-11 | 0.0202523839095582 | 2023-11-01 |
| 2023-12 | 0.0276102699555678 | 2023-12-01 |
| 2024-01 | 0.0270139449949821 | 2024-01-01 |
| 2024-02 | 0.0149852279051575 | 2024-02-01 |
| 2024-03 | 0.0166351370094153 | 2024-03-01 |
| 2024-04 | 0.0218270796097107 | 2024-04-01 |
| 2024-05 | 0.0267381488948342 | 2024-05-01 |
| 2024-06 | 0.0357096190973193 | 2024-06-01 |
| 2024-07 | 0.0349011037668995 | 2024-07-01 |
| 2024-08 | 0.0178330247023192 | 2024-08-01 |
| 2024-09 | 0.0184466557610615 | 2024-09-01 |
| 2024-10 | 0.0103021398392555 | 2024-10-01 |
| 2024-11 | 0.0187027949234392 | 2024-11-01 |
| 2024-12 | 0.0400386066681765 | 2024-12-01 |
| 2025-01 | 0.039656277481977 | 2025-01-01 |
| 2025-02 | 0.0269722429814135 | 2025-02-01 |
| 2025-03 | 0.0170125805463098 | 2025-03-01 |
| 2025-04 | 0.0218228459520011 | 2025-04-01 |
| 2025-05 | 0.0286434442732116 | 2025-05-01 |
| 2025-06 | 0.0111758105189233 | 2025-06-01 |
| 2025-07 | 0.0216093461610208 | 2025-07-01 |
| 2025-08 | 0.0365804276933529 | 2025-08-01 |
| 2025-09 | 0.0236647799469514 | 2025-09-01 |
| 2025-10 | 0.0251698310324235 | 2025-10-01 |
| 2025-11 | 0.0337156844180372 | 2025-11-01 |
| 2025-12 | 0.0375767141136374 | 2025-12-01 |
| 2026-01 | 0.0669318505119859 | 2026-01-01 |


### moral_foundations_by_bloc_month.csv (110 lignes)

| month | bloc | care | fairness | loyalty | authority | sanctity | n | month_ts |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2023-10 | Centre / Majorite | 0.1948100887400382 | 0.1812265160031561 | 0.2046622333295971 | 0.1782158285515274 | 0.1685584127132223 | 255 | 2023-10-01 |
| 2023-10 | Droite | 0.1904945646871903 | 0.1767549498040384 | 0.2045810658804014 | 0.1767886112993918 | 0.1643637258304547 | 300 | 2023-10-01 |
| 2023-10 | Gauche moderee | 0.2081970222525802 | 0.1813630834498475 | 0.212769501074595 | 0.184673085985928 | 0.1714447769197226 | 153 | 2023-10-01 |
| 2023-10 | Gauche radicale | 0.2119684088950435 | 0.193821701183598 | 0.2137348405410234 | 0.1882045451546929 | 0.1809371158826195 | 645 | 2023-10-01 |
| 2023-11 | Centre / Majorite | 0.1826950461647659 | 0.1691514297583943 | 0.2035623527196457 | 0.1686327029013024 | 0.1625912982960296 | 107 | 2023-11-01 |
| 2023-11 | Droite | 0.2045317447743314 | 0.1938698495505208 | 0.2187205707313275 | 0.1818195628631889 | 0.1727442032171285 | 107 | 2023-11-01 |
| 2023-11 | Gauche moderee | 0.1960547692916304 | 0.1681959154703466 | 0.203893496143261 | 0.1611905854973681 | 0.1479789378563482 | 55 | 2023-11-01 |
| 2023-11 | Gauche radicale | 0.1939710474412923 | 0.1779590466875338 | 0.2053079842086095 | 0.1760145899576088 | 0.1714139027769408 | 332 | 2023-11-01 |
| 2023-12 | Centre / Majorite | 0.1838256885975608 | 0.1622222638334595 | 0.2005356263525334 | 0.1806807177833014 | 0.1548596617838627 | 10 | 2023-12-01 |
| 2023-12 | Droite | 0.197417663995858 | 0.1859026544576245 | 0.1826451173010914 | 0.1791813280436249 | 0.164595327624407 | 16 | 2023-12-01 |
| 2023-12 | Gauche moderee | 0.1765197160994598 | 0.1695498265229646 | 0.2070259180006256 | 0.1812318639912127 | 0.1671356474403148 | 16 | 2023-12-01 |
| 2023-12 | Gauche radicale | 0.2077895309050682 | 0.1787086389500517 | 0.201651896883482 | 0.1819237303275588 | 0.1763541669473831 | 157 | 2023-12-01 |
| 2024-01 | Centre / Majorite | 0.17331512384453 | 0.1629014177035918 | 0.1839375351110932 | 0.1540709013385893 | 0.1521277875323286 | 64 | 2024-01-01 |
| 2024-01 | Droite | 0.1995980198658238 | 0.1917522375942767 | 0.1849523513763825 | 0.1734748446775831 | 0.1605045520359256 | 32 | 2024-01-01 |
| 2024-01 | Gauche moderee | 0.1973450607437086 | 0.1740651024633398 | 0.2294441292866499 | 0.1917613102445985 | 0.1701118709256718 | 30 | 2024-01-01 |
| 2024-01 | Gauche radicale | 0.1985153997548727 | 0.1910974050866741 | 0.2108060249574697 | 0.1789777920000261 | 0.1703287748266764 | 226 | 2024-01-01 |
| 2024-02 | Centre / Majorite | 0.1758886939902724 | 0.1514269575931856 | 0.1718502016651327 | 0.1565592922657234 | 0.1446942026626959 | 65 | 2024-02-01 |
| 2024-02 | Droite | 0.1952111757053725 | 0.1713030033761476 | 0.1890284257519858 | 0.1642291248753823 | 0.1653305874405055 | 32 | 2024-02-01 |
| 2024-02 | Gauche moderee | 0.2128673217117365 | 0.1675411728269657 | 0.1974722506090986 | 0.1706226139885715 | 0.1648119450355278 | 55 | 2024-02-01 |
| 2024-02 | Gauche radicale | 0.2071247330908049 | 0.18475341289712 | 0.2106895245728499 | 0.1835109837735052 | 0.1823154497514124 | 225 | 2024-02-01 |
| 2024-03 | Centre / Majorite | 0.183558444120087 | 0.1553790042429503 | 0.1849378216978585 | 0.1721849017781407 | 0.1597917951389593 | 47 | 2024-03-01 |
| 2024-03 | Droite | 0.2014689987570229 | 0.2109638786176559 | 0.2159406857835308 | 0.2007015041636947 | 0.1855844074395312 | 73 | 2024-03-01 |
| 2024-03 | Gauche moderee | 0.1967550913940465 | 0.1842618983652443 | 0.2223869884228816 | 0.1852907866174833 | 0.1859042074746758 | 44 | 2024-03-01 |
| 2024-03 | Gauche radicale | 0.1988455553025905 | 0.1885941352808995 | 0.2070367064590133 | 0.1832103645533329 | 0.1782611537320049 | 243 | 2024-03-01 |
| 2024-04 | Centre / Majorite | 0.1906741276156787 | 0.1770837718248553 | 0.2104212568473621 | 0.1766986854255155 | 0.1680072167456434 | 51 | 2024-04-01 |
| 2024-04 | Droite | 0.1849306427297567 | 0.1833947233032487 | 0.2025008487479933 | 0.1721547200180752 | 0.1623176497489515 | 51 | 2024-04-01 |
| 2024-04 | Gauche moderee | 0.1964060747091416 | 0.1870018583439939 | 0.2220823279749839 | 0.1888984243660441 | 0.1851099840096865 | 43 | 2024-04-01 |
| 2024-04 | Gauche radicale | 0.2009320864363953 | 0.185355034728606 | 0.2095006781437709 | 0.189876157797124 | 0.1797606140338194 | 349 | 2024-04-01 |
| 2024-05 | Centre / Majorite | 0.1928188215994423 | 0.1803823573175697 | 0.2070594605286609 | 0.1738816676636121 | 0.1653085580069827 | 104 | 2024-05-01 |
| 2024-05 | Droite | 0.2150808358659743 | 0.2019190893288726 | 0.2191304521005343 | 0.1920447130015965 | 0.1800525302779222 | 63 | 2024-05-01 |
| 2024-05 | Gauche moderee | 0.200926487120489 | 0.1871491815601819 | 0.2266944628017195 | 0.1913996089767273 | 0.1827780441636138 | 92 | 2024-05-01 |
| 2024-05 | Gauche radicale | 0.2011920443626546 | 0.1891875281047008 | 0.2191593361663915 | 0.1886800244945588 | 0.1811451304145145 | 608 | 2024-05-01 |
| 2024-06 | Centre / Majorite | 0.1764803947803034 | 0.1781602423095441 | 0.2026054508848742 | 0.1752807867485269 | 0.1690218104796519 | 52 | 2024-06-01 |
| 2024-06 | Droite | 0.1982996826197142 | 0.1904139805154686 | 0.2305710321803948 | 0.1947999528333787 | 0.1792297370853724 | 25 | 2024-06-01 |
| 2024-06 | Gauche moderee | 0.2004470224959736 | 0.1943628228012931 | 0.2397689728872454 | 0.1938095197167249 | 0.1800655524868193 | 24 | 2024-06-01 |
| 2024-06 | Gauche radicale | 0.1905662477271104 | 0.1764936123604434 | 0.2077817284684907 | 0.1853129018326596 | 0.1787808850371287 | 126 | 2024-06-01 |
| 2024-07 | Centre / Majorite | 0.1903683840056647 | 0.1628851875814503 | 0.1864444977738878 | 0.1820985181462209 | 0.1660276528771194 | 27 | 2024-07-01 |
| 2024-07 | Droite | 0.1906835587565619 | 0.1892630855420209 | 0.208427863881118 | 0.1941359831710404 | 0.1743028998771671 | 40 | 2024-07-01 |
| 2024-07 | Gauche moderee | 0.2133463854225094 | 0.2032224141056129 | 0.2201152609515812 | 0.1905442737971956 | 0.1695966723567845 | 14 | 2024-07-01 |
| 2024-07 | Gauche radicale | 0.1927631009449861 | 0.1959855799739636 | 0.2158712714107559 | 0.1912839738405608 | 0.1803860329840981 | 163 | 2024-07-01 |
| 2024-08 | Centre / Majorite | 0.1839653251104857 | 0.1829830615162349 | 0.205680308085341 | 0.1794117778788315 | 0.1743310373517723 | 35 | 2024-08-01 |
| 2024-08 | Droite | 0.1792096592489657 | 0.1828495047719955 | 0.2035573982209664 | 0.1721638454670538 | 0.1630323995166089 | 34 | 2024-08-01 |
| 2024-08 | Gauche moderee | 0.2048015277562278 | 0.1885878306136706 | 0.2142253504838976 | 0.1981554850722421 | 0.1780913858802183 | 16 | 2024-08-01 |
| 2024-08 | Gauche radicale | 0.1976049637575195 | 0.1852583197181313 | 0.2077583961541215 | 0.188163197318208 | 0.1718757462639436 | 99 | 2024-08-01 |
| 2024-09 | Centre / Majorite | 0.1438943306848621 | 0.1521705326269126 | 0.1632642485943266 | 0.1398151298008023 | 0.1374983679664554 | 15 | 2024-09-01 |
| 2024-09 | Droite | 0.2201579011566765 | 0.2113046316677236 | 0.234140413227898 | 0.2089521862292464 | 0.2024922416114071 | 19 | 2024-09-01 |
| 2024-09 | Gauche moderee | 0.2348960555193048 | 0.1891883518330149 | 0.2551373022836608 | 0.2231365260214957 | 0.2106298479096282 | 21 | 2024-09-01 |
| 2024-09 | Gauche radicale | 0.197012783571784 | 0.1824478411678398 | 0.2095978517126765 | 0.1915877663384811 | 0.1814645108105239 | 225 | 2024-09-01 |
| 2024-10 | Centre / Majorite | 0.1804740776755901 | 0.1570726163106996 | 0.1783944053015877 | 0.1591906160357415 | 0.1516423063957299 | 70 | 2024-10-01 |
| 2024-10 | Droite | 0.2107607373653366 | 0.1863963709582672 | 0.2167326873642263 | 0.1931251595575635 | 0.1804046976993759 | 92 | 2024-10-01 |
| 2024-10 | Gauche moderee | 0.1953731502022745 | 0.1763551294814132 | 0.1876202430930731 | 0.1664933331948668 | 0.1609385426138856 | 23 | 2024-10-01 |
| 2024-10 | Gauche radicale | 0.1918595892335625 | 0.1753537499496372 | 0.2036646786762986 | 0.179522167043921 | 0.1692092802641105 | 250 | 2024-10-01 |
| 2024-11 | Centre / Majorite | 0.1651202538247265 | 0.1659206662322171 | 0.1744302632936194 | 0.1505245543020342 | 0.1443569658644082 | 30 | 2024-11-01 |
| 2024-11 | Droite | 0.1878037904357357 | 0.1835633112370453 | 0.1980763633345277 | 0.1855820381849129 | 0.1684770259612207 | 43 | 2024-11-01 |
| 2024-11 | Gauche moderee | 0.2062697453051876 | 0.1773127960386553 | 0.2346087381223966 | 0.1860934120817385 | 0.1715470609533632 | 38 | 2024-11-01 |
| 2024-11 | Gauche radicale | 0.2049069186786687 | 0.1933169707179655 | 0.2221688675706591 | 0.1848553062483501 | 0.1795920186953784 | 209 | 2024-11-01 |
| 2024-12 | Centre / Majorite | 0.1726692606710042 | 0.1819127996259184 | 0.2036220390344404 | 0.1635493457270979 | 0.1417136888711342 | 6 | 2024-12-01 |
| 2024-12 | Droite | 0.1901177300203669 | 0.1855273925537617 | 0.1880702655023141 | 0.1482567959302239 | 0.1548910827288109 | 15 | 2024-12-01 |
| 2024-12 | Gauche moderee | 0.1917599631391594 | 0.1904790438084584 | 0.1952204763623971 | 0.1460198346125667 | 0.1597250261392475 | 10 | 2024-12-01 |
| 2024-12 | Gauche radicale | 0.1964279223233985 | 0.1951378861401002 | 0.2148391580327733 | 0.1927674930317575 | 0.1797356563066193 | 103 | 2024-12-01 |
| 2025-01 | Centre / Majorite | 0.1593273346779869 | 0.1452348258775943 | 0.1898831822555607 | 0.161101072614815 | 0.149041203491707 | 41 | 2025-01-01 |
| 2025-01 | Droite | 0.1886594462783426 | 0.1896778569468574 | 0.2040621183807055 | 0.1786254126439333 | 0.1699014337207187 | 31 | 2025-01-01 |
| 2025-01 | Gauche moderee | 0.1908422874810958 | 0.176217995409137 | 0.2027571937961494 | 0.1854773183777048 | 0.1666415444626428 | 29 | 2025-01-01 |
| 2025-01 | Gauche radicale | 0.1868996647939067 | 0.1727095189621346 | 0.1953992819407132 | 0.1723100057108699 | 0.1638468870795458 | 218 | 2025-01-01 |
| 2025-02 | Centre / Majorite | 0.1760354448756173 | 0.1601602578867217 | 0.1801308219415549 | 0.155406043821098 | 0.1505674051894261 | 44 | 2025-02-01 |
| 2025-02 | Droite | 0.2002107950118028 | 0.1790726908498495 | 0.2013532995228444 | 0.1616637214643254 | 0.1692341467546259 | 45 | 2025-02-01 |
| 2025-02 | Gauche moderee | 0.1858445816204411 | 0.1726613546087172 | 0.1948083494983994 | 0.1737223478932688 | 0.1716461920592525 | 12 | 2025-02-01 |
| 2025-02 | Gauche radicale | 0.1897456024282817 | 0.1849157834166031 | 0.20793916192672 | 0.1843684012410059 | 0.1722252724987514 | 74 | 2025-02-01 |
| 2025-03 | Centre / Majorite | 0.177107698011696 | 0.1657235257259817 | 0.1926529814512571 | 0.1663750432162714 | 0.1584455308580462 | 47 | 2025-03-01 |
| 2025-03 | Droite | 0.2024205845454774 | 0.1950421859609062 | 0.2114647552612832 | 0.1961739985909787 | 0.1896977740947311 | 41 | 2025-03-01 |
| 2025-03 | Gauche moderee | 0.1821002960958028 | 0.1740805822390496 | 0.2015105035192202 | 0.1500631483021881 | 0.1454926448977752 | 18 | 2025-03-01 |
| 2025-03 | Gauche radicale | 0.1881091607262857 | 0.1813403807964175 | 0.2049027124327536 | 0.1798151839662897 | 0.1712085667006149 | 151 | 2025-03-01 |
| 2025-04 | Centre / Majorite | 0.1709249149134364 | 0.171858144718287 | 0.2034518894338135 | 0.1654686547755414 | 0.1557761531279638 | 26 | 2025-04-01 |
| 2025-04 | Droite | 0.1928890894030321 | 0.1922682284427976 | 0.1995378326510498 | 0.1840608046424571 | 0.1772608520617481 | 24 | 2025-04-01 |
| 2025-04 | Gauche moderee | 0.194273988363195 | 0.1796355163285686 | 0.2058649939959986 | 0.1768876820873031 | 0.1731358084063489 | 14 | 2025-04-01 |
| 2025-04 | Gauche radicale | 0.2019610902903441 | 0.1899067770596198 | 0.2084321694501482 | 0.1842486485889999 | 0.1767532571461652 | 230 | 2025-04-01 |
| 2025-05 | Centre / Majorite | 0.1828634631287471 | 0.1724698350033258 | 0.189243075439197 | 0.1805287533475548 | 0.1700801740079028 | 122 | 2025-05-01 |
| 2025-05 | Droite | 0.1769175364910145 | 0.1773867361034318 | 0.1989255777742027 | 0.1745565232814115 | 0.163868610298126 | 74 | 2025-05-01 |
| 2025-05 | Gauche moderee | 0.2064448064974965 | 0.183505442962209 | 0.2127885937780407 | 0.1845513135351169 | 0.1751378895417989 | 50 | 2025-05-01 |
| 2025-05 | Gauche radicale | 0.1971709445243231 | 0.181125117170053 | 0.2050071687102122 | 0.1853830690250286 | 0.1731746353363589 | 309 | 2025-05-01 |
| 2025-06 | Centre / Majorite | 0.1643387987909773 | 0.1632943438354444 | 0.1832655441533296 | 0.1632671909502843 | 0.151223770905336 | 116 | 2025-06-01 |
| 2025-06 | Droite | 0.1903144596539114 | 0.1806853751118806 | 0.2057486062940772 | 0.1844035976421549 | 0.1763331580944675 | 101 | 2025-06-01 |
| 2025-06 | Gauche moderee | 0.1876154696293487 | 0.1728861739609465 | 0.1961975354684201 | 0.1792715313279698 | 0.1651030416832145 | 57 | 2025-06-01 |
| 2025-06 | Gauche radicale | 0.1934264263398279 | 0.1824504418736053 | 0.208030021205244 | 0.1785677148238945 | 0.1672292685288272 | 548 | 2025-06-01 |
| 2025-07 | Centre / Majorite | 0.1689912920961258 | 0.1766958279514912 | 0.1931456871998678 | 0.1711641163216792 | 0.1630447965420799 | 31 | 2025-07-01 |
| 2025-07 | Droite | 0.194026675429246 | 0.1834882079289838 | 0.2051035794953965 | 0.197338792193793 | 0.180066712351493 | 77 | 2025-07-01 |
| 2025-07 | Gauche moderee | 0.2223134074824346 | 0.1824171255792014 | 0.2216027484032543 | 0.2043628513990486 | 0.1811805973809012 | 35 | 2025-07-01 |
| 2025-07 | Gauche radicale | 0.1965447853083246 | 0.1831466106205366 | 0.2072960496905148 | 0.1855179675858043 | 0.1743873859550433 | 347 | 2025-07-01 |
| 2025-08 | Centre / Majorite | 0.1774998230936661 | 0.1690773433477703 | 0.2032133995112687 | 0.1734123713945259 | 0.1712052952216095 | 14 | 2025-08-01 |
| 2025-08 | Droite | 0.1837316047067587 | 0.1914691368826587 | 0.198329999077007 | 0.177671550590174 | 0.175811081278836 | 22 | 2025-08-01 |
| 2025-08 | Gauche moderee | 0.1980328540874704 | 0.1725867044606397 | 0.22250581929132 | 0.1747563660806257 | 0.1714288212145212 | 20 | 2025-08-01 |
| 2025-08 | Gauche radicale | 0.1844097272737291 | 0.1727465967196736 | 0.2033322350432898 | 0.1764792348784769 | 0.1709793717130429 | 127 | 2025-08-01 |
| 2025-09 | Centre / Majorite | 0.2116212062332751 | 0.1908533679831584 | 0.2315305641944872 | 0.2159730221622738 | 0.1847465451486623 | 21 | 2025-09-01 |
| 2025-09 | Droite | 0.2113962629863487 | 0.1893449342853626 | 0.2259561274890034 | 0.2092956519608382 | 0.1812701930714734 | 47 | 2025-09-01 |
| 2025-09 | Gauche moderee | 0.1951923851445177 | 0.1810300742361365 | 0.2129238729851519 | 0.1881369507258027 | 0.1673947020035042 | 57 | 2025-09-01 |
| 2025-09 | Gauche radicale | 0.1946402565895707 | 0.1770489530340635 | 0.2166840438231669 | 0.189822472879021 | 0.1760787772583285 | 343 | 2025-09-01 |
| 2025-10 | Centre / Majorite | 0.1752180099815951 | 0.1617190032144159 | 0.1846972494502051 | 0.1539755492770195 | 0.1449898837055634 | 57 | 2025-10-01 |
| 2025-10 | Droite | 0.1932877307138482 | 0.1761779521584012 | 0.1977108783371193 | 0.1783661060021565 | 0.1683188837680889 | 40 | 2025-10-01 |
| 2025-10 | Gauche moderee | 0.170860094987884 | 0.1701542393428803 | 0.1715891201033189 | 0.1600531346829521 | 0.1372823009689135 | 10 | 2025-10-01 |
| 2025-10 | Gauche radicale | 0.1899555589626559 | 0.1790557998693731 | 0.2014399217314653 | 0.182005343175385 | 0.1724967395791219 | 260 | 2025-10-01 |
| 2025-11 | Centre / Majorite | 0.1638244324007324 | 0.1478889177184147 | 0.183673538753462 | 0.1644770904212507 | 0.1376239568684155 | 10 | 2025-11-01 |
| 2025-11 | Droite | 0.1814133926943373 | 0.1990332421331884 | 0.2254998992499634 | 0.1893975352545875 | 0.189802405727799 | 17 | 2025-11-01 |
| 2025-11 | Gauche moderee | 0.2053048272497836 | 0.1575608578798825 | 0.1667441800049053 | 0.1715508838501276 | 0.1528037981266952 | 19 | 2025-11-01 |
| 2025-11 | Gauche radicale | 0.1889424131515661 | 0.1782728054987338 | 0.2012650382060625 | 0.1797506875843616 | 0.1705325190183928 | 101 | 2025-11-01 |
| 2025-12 | Centre / Majorite | 0.2020155805224354 | 0.2009271959294472 | 0.2102482073561589 | 0.1878431628475238 | 0.1845434941056978 | 14 | 2025-12-01 |
| 2025-12 | Droite | 0.1764825189305199 | 0.1858969172765097 | 0.1544782349184847 | 0.1429885449591598 | 0.156347749820341 | 11 | 2025-12-01 |
| 2025-12 | Gauche moderee | 0.1930747222310898 | 0.1835518452376035 | 0.2130601708923304 | 0.1830400587545923 | 0.1928317364479674 | 15 | 2025-12-01 |
| 2025-12 | Gauche radicale | 0.1920159154427331 | 0.1813565353341719 | 0.2050572208026721 | 0.172678730822883 | 0.1577746075565589 | 97 | 2025-12-01 |
| 2026-01 | Centre / Majorite | 0.2039681085043988 | 0.2002902003910068 | 0.217091275659824 | 0.2177068059628543 | 0.2225042766373411 | 8 | 2026-01-01 |
| 2026-01 | Gauche radicale | 0.1777107945383769 | 0.1875234394088168 | 0.2104502528164887 | 0.1889044009581887 | 0.1683832881942302 | 73 | 2026-01-01 |


## 04b — Fighting words temporel

### fighting_words_temporal.csv (22797 lignes)

| month | word | z |
| --- | --- | --- |
| 2023-10 | réunit | -0.5428603468765728 |
| 2023-10 | franceenisrael | -0.6128370153562004 |
| 2023-10 | décerné | -0.5428603468765728 |
| 2023-10 | macronie | 0.5370957502832789 |
| 2023-10 | hamasmassacre | -0.5428603468765728 |
| 2023-10 | passive | -0.5428603468765728 |
| 2023-10 | bombardé | 0.6402365993404355 |
| 2023-10 | infréquentable | -0.5428603468765728 |
| 2023-10 | nourrir | -0.5428603468765728 |
| 2023-10 | combien | 0.6873722651061688 |
| 2023-10 | ancien | -1.680355386494233 |
| 2023-10 | cannet | -0.5428603468765728 |
| 2023-10 | idéologie | -0.6825746853776851 |
| 2023-10 | cafouilleuse | -0.5428603468765728 |
| 2023-10 | frontalières | -0.5428603468765728 |
| 2023-10 | dont | 0.5461747916582285 |
| 2023-10 | vidéo | -1.253180719340285 |
| 2023-10 | vote | -0.7257003312237641 |
| 2023-10 | koweït | -0.5428603468765728 |
| 2023-10 | ingéniez | -0.5428603468765728 |
| 2023-10 | alexandrerozen | -0.5428603468765728 |
| 2023-10 | décidé | -0.8423891415443356 |
| 2023-10 | succèdent | -0.5428603468765728 |
| 2023-10 | personnelles | -0.5428603468765728 |
| 2023-10 | cultes | -0.5428603468765728 |
| 2023-10 | juridique | -0.5428603468765728 |
| 2023-10 | joie | -0.6536552241246498 |
| 2023-10 | écrit | 0.5147256364869164 |
| 2023-10 | sur | 1.821772848305686 |
| 2023-10 | déni | -0.8423891415443356 |
| 2023-10 | attacked | -0.5428603468765728 |
| 2023-10 | leader | -0.6128370153562004 |
| 2023-10 | stratégique | -0.5971389749862454 |
| 2023-10 | si | -1.0974068068198373 |
| 2023-10 | entendeur | -0.5428603468765728 |
| 2023-10 | franco | 0.697873929835981 |
| 2023-10 | solidarité | -1.1505921975085778 |
| 2023-10 | incontournable | -0.5428603468765728 |
| 2023-10 | crié | -0.5428603468765728 |
| 2023-10 | soutenir | -2.1036318734899977 |
| 2023-10 | commissaire | -0.5428603468765728 |
| 2023-10 | millions | 2.6047865079311863 |
| 2023-10 | redoutons | -0.5428603468765728 |
| 2023-10 | accorder | -0.5428603468765728 |
| 2023-10 | différencie | -0.6128370153562004 |
| 2023-10 | sentir | -0.5428603468765728 |
| 2023-10 | bfmtv | -1.365788488089278 |
| 2023-10 | près | 1.460190314801818 |
| 2023-10 | pension | -0.5428603468765728 |
| 2023-10 | palestinienne | 1.0963138415869342 |
| 2023-10 | flotter | -0.5428603468765728 |
| 2023-10 | cohésion | -0.8423891415443356 |
| 2023-10 | connaît | -0.5971389749862454 |
| 2023-10 | psg | -0.5428603468765728 |
| 2023-10 | infiltrées | -0.5428603468765728 |
| 2023-10 | jeannebarsegh | -0.5428603468765728 |
| 2023-10 | savent | -0.5971389749862454 |
| 2023-10 | traque | -0.6128370153562004 |
| 2023-10 | intrinsèquement | -0.5428603468765728 |
| 2023-10 | soir | 2.0218046940258527 |
| 2023-10 | inquiets | -0.5428603468765728 |
| 2023-10 | valez | -0.5428603468765728 |
| 2023-10 | délitement | -0.5428603468765728 |
| 2023-10 | fort | 0.5370957502832789 |
| 2023-10 | pourra | -1.9307168622832047 |
| 2023-10 | ukrainiens | -0.5428603468765728 |
| 2023-10 | agences | 0.5370957502832789 |
| 2023-10 | relativisent | -0.5971389749862454 |
| 2023-10 | hopital | 0.5708146873246048 |
| 2023-10 | anges | -0.5428603468765728 |
| 2023-10 | image | -0.5971389749862454 |
| 2023-10 | abraham | -0.5428603468765728 |
| 2023-10 | pleins | -0.5428603468765728 |
| 2023-10 | perpétrés | 1.1652991613593595 |
| 2023-10 | communisme | -0.5428603468765728 |
| 2023-10 | semblable | -0.5428603468765728 |
| 2023-10 | ramener | -0.5971389749862454 |
| 2023-10 | grave | 1.1652991613593595 |
| 2023-10 | information | -1.365788488089278 |
| 2023-10 | travailler | -1.253180719340285 |
| 2023-10 | lancés | -0.5428603468765728 |
| 2023-10 | présente | -0.6128370153562004 |
| 2023-10 | bénéficient | -0.5428603468765728 |
| 2023-10 | défendre | -1.5233918049797068 |
| 2023-10 | chemin | 1.2847224199226654 |
| 2023-10 | fichés | -0.5428603468765728 |
| 2023-10 | violence | 1.193250919079627 |
| 2023-10 | prendra | -0.5428603468765728 |
| 2023-10 | nié | -0.5428603468765728 |
| 2023-10 | bat | -0.5971389749862454 |
| 2023-10 | glace | -0.5428603468765728 |
| 2023-10 | quand | -0.6766458799819907 |
| 2023-10 | aéroport | -0.5971389749862454 |
| 2023-10 | clairs | -0.8423891415443356 |
| 2023-10 | guide | -0.5428603468765728 |
| 2023-10 | à | 1.4342567322158335 |
| 2023-10 | république | 2.11886562558204 |
| 2023-10 | régionales | -0.5428603468765728 |
| 2023-10 | nuit | 0.5708146873246048 |
| 2023-10 | biden | -1.0308559434450515 |
| ... | ... | ... |
| 2025-12 | israélienne | 0.5064022446449105 |
| 2025-12 | ni | -1.161566600295333 |
| 2025-12 | antisémite | -1.6364485610580468 |
| 2025-12 | ravive | -0.6687018205922796 |
| 2025-12 | comptes | -0.6687018205922796 |
| 2025-12 | santé | -0.8808673984017251 |
| 2025-12 | passer | -1.4958268528693208 |
| 2025-12 | a | -1.3242688081094438 |
| 2025-12 | génocide | 0.5677538189442948 |
| 2025-12 | égalité | -1.4958268528693208 |
| 2025-12 | autres | -0.9156650083829788 |
| 2025-12 | dirigeants | -0.6687018205922796 |
| 2025-12 | israël | 1.225813833422568 |
| 2025-12 | déclarer | -0.6687018205922796 |
| 2025-12 | sont | 1.088158939313415 |
| 2025-12 | pierre | -0.6687018205922796 |
| 2025-12 | enquise | -0.6687018205922796 |
| 2025-12 | ridicule | -0.6687018205922796 |
| 2025-12 | reprises | -0.6687018205922796 |
| 2025-12 | être | 0.5138187914116665 |
| 2025-12 | hors | -1.4958268528693208 |
| 2025-12 | assumé | -0.6687018205922796 |
| 2025-12 | cauchemar | -0.6687018205922796 |
| 2025-12 | dispositifs | -0.7389865168341303 |
| 2025-12 | free | -1.4958268528693208 |
| 2025-12 | monsieur | -1.4958268528693208 |
| 2025-12 | immigrationniste | -0.6687018205922796 |
| 2025-12 | militant | -0.8808673984017251 |
| 2025-12 | derrière | -0.6687018205922796 |
| 2025-12 | devrait | -1.4958268528693208 |
| 2025-12 | rêver | -0.6687018205922796 |
| 2025-12 | condamnent | -0.6687018205922796 |
| 2025-12 | chaine | -0.6687018205922796 |
| 2025-12 | culpabiliser | -0.6687018205922796 |
| 2025-12 | collègue | -1.4958268528693208 |
| 2025-12 | balayez | -0.6687018205922796 |
| 2025-12 | qu | -1.494814223942555 |
| 2025-12 | usa | -0.6687018205922796 |
| 2025-12 | ici | -1.161566600295333 |
| 2025-12 | avoué | -0.6687018205922796 |
| 2025-12 | français | -0.6521763789087335 |
| 2025-12 | international | 0.5543929300855335 |
| 2025-12 | continuation | -0.6687018205922796 |
| 2025-12 | place | -1.4958268528693208 |
| 2025-12 | entre | -1.161566600295333 |
| 2025-12 | couvert | -0.6687018205922796 |
| 2025-12 | recycle | -0.6687018205922796 |
| 2025-12 | avec | -2.215316055890485 |
| 2025-12 | messages | -0.6687018205922796 |
| 2025-12 | faso | -1.4958268528693208 |
| 2025-12 | hassan | -0.6687018205922796 |
| 2025-12 | nécessite | -0.6687018205922796 |
| 2025-12 | pas | -1.2585683534151342 |
| 2025-12 | rajoute | -0.6687018205922796 |
| 2025-12 | paris | -1.4958268528693208 |
| 2025-12 | anathèmes | -0.6687018205922796 |
| 2025-12 | droit | 0.5207232330683212 |
| 2025-12 | palestine | 1.0043453309336976 |
| 2025-12 | toutes | -1.0695080113102051 |
| 2025-12 | olympiques | -2.290036704003279 |
| 2025-12 | bondi | -0.7389865168341303 |
| 2025-12 | honneurs | -0.6687018205922796 |
| 2025-12 | macron | -1.161566600295333 |
| 2025-12 | accueilli | -1.4958268528693208 |
| 2025-12 | cordon | -0.6687018205922796 |
| 2025-12 | refusé | -1.161566600295333 |
| 2025-12 | echorouk | -0.6687018205922796 |
| 2025-12 | matin | -1.4958268528693208 |
| 2025-12 | cour | -0.6687018205922796 |
| 2025-12 | je | -0.9156650083829788 |
| 2025-12 | déchaînée | -0.6687018205922796 |
| 2025-12 | cherche | -0.6687018205922796 |
| 2025-12 | lumière | -1.161566600295333 |
| 2025-12 | commencer | -0.6687018205922796 |
| 2025-12 | il | -1.6267053375166158 |
| 2025-12 | antisémites | -2.290036704003279 |
| 2025-12 | angleterre | -0.6687018205922796 |
| 2025-12 | actes | -1.161566600295333 |
| 2025-12 | terrible | -0.6687018205922796 |
| 2025-12 | politicienne | -0.6687018205922796 |
| 2025-12 | municipales | -0.6687018205922796 |
| 2025-12 | massacres | -1.161566600295333 |
| 2025-12 | fête | -1.4958268528693208 |
| 2025-12 | tranquillement | -1.161566600295333 |
| 2025-12 | douloureuse | -0.6687018205922796 |
| 2025-12 | sa | -2.110175941063937 |
| 2025-12 | gaza | 0.7638696224399157 |
| 2025-12 | avez | -0.8808673984017251 |
| 2025-12 | encore | -1.6364485610580468 |
| 2025-12 | question | -1.4958268528693208 |
| 2025-12 | milliards | -1.161566600295333 |
| 2025-12 | cabinet | -0.6687018205922796 |
| 2025-12 | maghreb | -0.6687018205922796 |
| 2025-12 | pure | -0.6687018205922796 |
| 2025-12 | crs | -0.6687018205922796 |
| 2025-12 | vos | -2.754118181988991 |
| 2025-12 | colonisation | -0.6462082961313542 |
| 2025-12 | algerie | -0.6687018205922796 |
| 2025-12 | par | 0.911765039706386 |

*(tronqué à 200 lignes — voir CSV pour données complètes)*


## 05 — Événements pivot

### variables_batch_specifiques.csv (7 lignes)

| batch | n | stance_mean | stance_std |
| --- | --- | --- | --- |
| CHOC | 1610 | 0.2285714285714285 | 1.486187850956839 |
| POST_CIJ | 350 | 0.9257142857142856 | 1.4000292377509511 |
| RAFAH | 977 | 1.1248720573183213 | 1.3099421246316152 |
| POST_SINWAR | 237 | 0.8945147679324894 | 1.4820434661595008 |
| MANDATS_CPI | 309 | 1.1877022653721685 | 1.2288645226233783 |
| CEASEFIRE_BREACH | 751 | 0.5898801597869507 | 1.4938465290269412 |
| NEW_OFFENSIVE | 1671 | 0.8653500897666068 | 1.4366260728429463 |


### ceasefire_call_batch_bloc.csv (28 lignes)

| batch | bloc | pct | n |
| --- | --- | --- | --- |
| CEASEFIRE_BREACH | Centre / Majorite | 0.106060606060606 | 132 |
| CEASEFIRE_BREACH | Droite | 0.0 | 117 |
| CEASEFIRE_BREACH | Gauche moderee | 0.1186440677966101 | 59 |
| CEASEFIRE_BREACH | Gauche radicale | 0.1218961625282167 | 443 |
| CHOC | Centre / Majorite | 0.0348432055749128 | 287 |
| CHOC | Droite | 0.0056818181818181 | 352 |
| CHOC | Gauche moderee | 0.4175824175824176 | 182 |
| CHOC | Gauche radicale | 0.3662864385297845 | 789 |
| MANDATS_CPI | Centre / Majorite | 0.125 | 16 |
| MANDATS_CPI | Droite | 0.1111111111111111 | 36 |
| MANDATS_CPI | Gauche moderee | 0.0967741935483871 | 31 |
| MANDATS_CPI | Gauche radicale | 0.0575221238938053 | 226 |
| NEW_OFFENSIVE | Centre / Majorite | 0.1136363636363636 | 264 |
| NEW_OFFENSIVE | Droite | 0.0 | 199 |
| NEW_OFFENSIVE | Gauche moderee | 0.1239669421487603 | 121 |
| NEW_OFFENSIVE | Gauche radicale | 0.0763569457221711 | 1087 |
| POST_CIJ | Centre / Majorite | 0.109090909090909 | 55 |
| POST_CIJ | Droite | 0.03125 | 32 |
| POST_CIJ | Gauche moderee | 0.5217391304347826 | 46 |
| POST_CIJ | Gauche radicale | 0.3502304147465437 | 217 |
| POST_SINWAR | Centre / Majorite | 0.1515151515151515 | 33 |
| POST_SINWAR | Droite | 0.0232558139534883 | 43 |
| POST_SINWAR | Gauche moderee | 0.0 | 7 |
| POST_SINWAR | Gauche radicale | 0.1103896103896103 | 154 |
| RAFAH | Centre / Majorite | 0.1461538461538461 | 130 |
| RAFAH | Droite | 0.0422535211267605 | 71 |
| RAFAH | Gauche moderee | 0.1792452830188679 | 106 |
| RAFAH | Gauche radicale | 0.1597014925373134 | 670 |


### anova_interaction.csv (5 lignes)

| Unnamed: 0 | sum_sq | df | F | PR(>F) |
| --- | --- | --- | --- | --- |
| C(bloc) | 7103.76230338046 | 3.0 | 3187.0775808582025 | 0.0 |
| C(batch) | 123.87932503211394 | 6.0 | 27.789008322661456 | 6.696334031590087e-33 |
| C(arena) | 8.86026578683701 | 1.0 | 11.925379782021468 | 0.0005576506490594 |
| C(bloc):C(batch) | 49.163218323092806 | 18.0 | 3.676150379398341 | 2.211347139863675e-07 |
| Residual | 4365.724422625399 | 5876.0 |  |  |


### anova_type2.csv (5 lignes)

| index | sum_sq | df | F | PR(>F) |
| --- | --- | --- | --- | --- |
| C(bloc) | 7103.76230338046 | 3.0 | 3187.0775808582025 | 0.0 |
| C(batch) | 123.87932503211394 | 6.0 | 27.789008322661456 | 6.696334031590087e-33 |
| C(arena) | 8.86026578683701 | 1.0 | 11.925379782021468 | 0.0005576506490594 |
| C(bloc):C(batch) | 49.163218323092806 | 18.0 | 3.676150379398341 | 2.211347139863675e-07 |
| Residual | 4365.724422625399 | 5876.0 |  |  |


## 06 — Convergence transpartisane

### convergence_batch_bloc.csv (28 lignes)

| batch | bloc | pct |
| --- | --- | --- |
| CEASEFIRE_BREACH | Centre / Majorite | 0.7954545454545454 |
| CEASEFIRE_BREACH | Droite | 0.4871794871794871 |
| CEASEFIRE_BREACH | Gauche moderee | 0.8305084745762712 |
| CEASEFIRE_BREACH | Gauche radicale | 0.3724604966139955 |
| CHOC | Centre / Majorite | 0.7770034843205574 |
| CHOC | Droite | 0.4914772727272727 |
| CHOC | Gauche moderee | 0.9065934065934066 |
| CHOC | Gauche radicale | 0.6666666666666666 |
| MANDATS_CPI | Centre / Majorite | 1.0 |
| MANDATS_CPI | Droite | 0.6111111111111112 |
| MANDATS_CPI | Gauche moderee | 0.8387096774193549 |
| MANDATS_CPI | Gauche radicale | 0.2389380530973451 |
| NEW_OFFENSIVE | Centre / Majorite | 0.8106060606060606 |
| NEW_OFFENSIVE | Droite | 0.5025125628140703 |
| NEW_OFFENSIVE | Gauche moderee | 0.7024793388429752 |
| NEW_OFFENSIVE | Gauche radicale | 0.2787488500459981 |
| POST_CIJ | Centre / Majorite | 0.7272727272727273 |
| POST_CIJ | Droite | 0.59375 |
| POST_CIJ | Gauche moderee | 0.8260869565217391 |
| POST_CIJ | Gauche radicale | 0.5253456221198156 |
| POST_SINWAR | Centre / Majorite | 0.7272727272727273 |
| POST_SINWAR | Droite | 0.5813953488372093 |
| POST_SINWAR | Gauche moderee | 0.5714285714285714 |
| POST_SINWAR | Gauche radicale | 0.2402597402597402 |
| RAFAH | Centre / Majorite | 0.8615384615384616 |
| RAFAH | Droite | 0.380281690140845 |
| RAFAH | Gauche moderee | 0.6698113207547169 |
| RAFAH | Gauche radicale | 0.3029850746268657 |


### movers_caches.csv (147 lignes)

| author | stance_initial | stance_final | delta_individuel | bloc | mover_type | rupture_date |
| --- | --- | --- | --- | --- | --- | --- |
| Adrien Quatennens | 1.1666666666666667 | 2.0 | 0.8333333333333333 | Gauche radicale | modere |  |
| Agnès Firmin Le Bodo | -2.0 | -1.0 | 1.0 | Centre / Majorite | modere |  |
| Alma Dufour | 1.4615384615384617 | 1.696 | 0.2344615384615385 | Gauche radicale | non_mover |  |
| Amélia Lakrafi | 0.0 | 0.8571428571428571 | 0.8571428571428571 | Centre / Majorite | modere |  |
| Anne-Cécile Violland | -1.5 | -1.0 | 0.5 | Centre / Majorite | non_mover |  |
| Antoine Léaument | 1.2 | 1.4090909090909092 | 0.2090909090909092 | Gauche radicale | non_mover |  |
| Antoine Villedieu | -2.0 | -2.0 | 0.0 | Droite | non_mover |  |
| Arthur Delaporte | 0.5 | 0.5 | 0.0 | Gauche moderee | non_mover |  |
| Aurore Bergé | -1.125 | -0.9333333333333332 | 0.1916666666666666 | Centre / Majorite | non_mover |  |
| Aurélien Saintoul | 1.6 | 1.3548387096774193 | -0.2451612903225808 | Gauche radicale | non_mover |  |
| Aurélien Taché | 1.7333333333333334 | 1.5277777777777777 | -0.2055555555555557 | Gauche radicale | non_mover |  |
| Aymeric Caron | 1.1666666666666667 | 1.6895306859205776 | 0.5228640192539109 | Gauche radicale | non_mover |  |
| Bastien Lachaud | 1.6470588235294117 | 1.6744186046511629 | 0.0273597811217511 | Gauche radicale | non_mover |  |
| Belkhir Belhaddad | 1.0 | 1.0 | 0.0 | Centre / Majorite | non_mover |  |
| Benjamin Haddad | -1.0625 | -1.0 | 0.0625 | Centre / Majorite | non_mover |  |
| Boris Vallaud | 0.6 | 1.0 | 0.4 | Gauche moderee | non_mover |  |
| Brigitte Klinkert | -0.6666666666666666 | -1.0 | -0.3333333333333333 | Centre / Majorite | non_mover |  |
| Bruno Bilde | -1.4 | -1.75 | -0.3500000000000001 | Droite | non_mover |  |
| Bryan Masson | -1.0 | -1.0 | 0.0 | Droite | non_mover |  |
| Carlos Martens Bilongo | 1.6428571428571428 | 1.7272727272727273 | 0.0844155844155845 | Gauche radicale | non_mover |  |
| Caroline Parmentier | -1.0 | -2.0 | -1.0 | Droite | modere |  |
| Caroline Yadan | -0.8 | -1.1111111111111112 | -0.3111111111111111 | Centre / Majorite | non_mover |  |
| Catherine Couturier | 1.2 | 1.75 | 0.55 | Gauche radicale | non_mover |  |
| Claire Lejeune | 1.0 | 1.911764705882353 | 0.911764705882353 | Gauche radicale | modere |  |
| Clémence Guetté | 1.8333333333333333 | 1.875 | 0.0416666666666667 | Gauche radicale | non_mover |  |
| Clémentine Autain | 1.375 | 1.807692307692308 | 0.4326923076923077 | Gauche radicale | non_mover |  |
| Constance Le Grip | -1.1153846153846154 | -1.0 | 0.1153846153846154 | Centre / Majorite | non_mover |  |
| Céline Calvez | -0.3333333333333333 | 0.3333333333333333 | 0.6666666666666666 | Centre / Majorite | non_mover |  |
| Damien Maudet | 1.4285714285714286 | 1.0 | -0.4285714285714286 | Gauche radicale | non_mover |  |
| Danielle Simonnet | 1.5 | 1.0 | -0.5 | Gauche moderee | non_mover |  |
| Danièle Obono | 1.7 | 1.7926829268292683 | 0.0926829268292683 | Gauche radicale | non_mover |  |
| David Guiraud | 1.7215189873417722 | 1.9393939393939397 | 0.2178749520521672 | Gauche radicale | non_mover |  |
| Dominique Potier | 0.3333333333333333 | 0.3333333333333333 | 0.0 | Gauche moderee | non_mover |  |
| Edwige Diaz | -2.0 | -1.0714285714285714 | 0.9285714285714286 | Droite | modere |  |
| Elsa Faucillon | 1.4 | 1.7826086956521738 | 0.3826086956521739 | Gauche radicale | non_mover |  |
| Emmanuel Fernandes | 1.5666666666666669 | 1.4545454545454546 | -0.112121212121212 | Gauche radicale | non_mover |  |
| Ersilia Soudais | 1.4285714285714286 | 1.8888888888888888 | 0.4603174603174602 | Gauche radicale | non_mover |  |
| Erwan Balanant | -1.5 | 1.0 | 2.5 | Centre / Majorite | fort |  |
| Fabien Roussel | 1.4 | 1.6578947368421053 | 0.2578947368421054 | Gauche radicale | non_mover |  |
| Florian Chauche | 1.5 | 0.6666666666666666 | -0.8333333333333334 | Gauche radicale | modere |  |
| Franck Riester | -1.0 | -1.0 | 0.0 | Centre / Majorite | non_mover |  |
| François Cormier-Bouligeon | -1.2 | -1.3333333333333333 | -0.1333333333333333 | Centre / Majorite | non_mover |  |
| François Piquemal | 1.0 | 1.6363636363636365 | 0.6363636363636365 | Gauche radicale | non_mover |  |
| François Ruffin | 1.2222222222222223 | 1.8 | 0.5777777777777777 | Gauche moderee | non_mover |  |
| Frédéric Valletoux | -1.0 | -2.0 | -1.0 | Centre / Majorite | modere |  |
| Gabriel Amard | 1.3333333333333333 | 1.5588235294117647 | 0.2254901960784314 | Gauche radicale | non_mover |  |
| Guillaume Bigot | -1.5714285714285714 | -1.0 | 0.5714285714285714 | Droite | non_mover |  |
| Gérald Darmanin | -1.0 | -1.0 | 0.0 | Centre / Majorite | non_mover |  |
| Hadrien Clouet | 1.3703703703703705 | 1.3114754098360657 | -0.0588949605343049 | Gauche radicale | non_mover |  |
| Hervé de Lépinau | -1.625 | -2.0 | -0.375 | Droite | non_mover |  |
| ... | ... | ... | ... | ... | ... | ... |
| Matthieu Marchio | -1.3333333333333333 | -1.0 | 0.3333333333333332 | Droite | non_mover |  |
| Maxime Michelet | -1.0 | -1.0 | 0.0 | Droite | non_mover |  |
| Michel Barnier | -1.0 | -0.8 | 0.1999999999999999 | Droite | non_mover |  |
| Michel Guiniot | -1.0 | -1.0 | 0.0 | Droite | non_mover |  |
| Michèle Tabarot | -1.3 | -1.181818181818182 | 0.1181818181818181 | Droite | non_mover |  |
| Mme Alma Dufour | 1.6666666666666667 | 1.8 | 0.1333333333333333 | Gauche radicale | non_mover |  |
| Mme Caroline Yadan | -1.2857142857142858 | -1.588235294117647 | -0.3025210084033611 | Centre / Majorite | non_mover |  |
| Mme Constance Le Grip | -1.5 | 0.0 | 1.5 | Centre / Majorite | modere |  |
| Mme Cyrielle Chatelain | 1.125 | 0.8 | -0.3249999999999999 | Gauche moderee | non_mover |  |
| Mme Elsa Faucillon | 1.6666666666666667 | 2.0 | 0.3333333333333332 | Gauche radicale | non_mover |  |
| Mme Marine Le Pen | -0.8333333333333334 | -1.0 | -0.1666666666666666 | Droite | non_mover |  |
| Mme Mathilde Panot | 1.4848484848484849 | 1.5 | 0.0151515151515151 | Gauche radicale | non_mover |  |
| Mme Michèle Tabarot | -1.4 | -1.0 | 0.3999999999999999 | Droite | non_mover |  |
| Mme Sabrina Sebaihi | 1.6666666666666667 | 1.8 | 0.1333333333333333 | Gauche moderee | non_mover |  |
| Mme Sandrine Rousseau | 1.25 | -2.0 | -3.25 | Gauche moderee | fort |  |
| Mme Sophie Taillé-Polian | 1.5 | -0.5 | -2.0 | Gauche moderee | fort |  |
| Nadège Abomangoli | 1.5161290322580645 | 1.641025641025641 | 0.1248966087675764 | Gauche radicale | non_mover |  |
| Natalia Pouzyreff | -1.0909090909090908 | -1.0 | 0.0909090909090908 | Centre / Majorite | non_mover |  |
| Nathalie Oziol | 1.5625 | 1.7027027027027026 | 0.1402027027027026 | Gauche radicale | non_mover |  |
| Olivier Faure | 0.5681818181818182 | 1.0277777777777777 | 0.4595959595959594 | Gauche moderee | non_mover |  |
| Patrick Hetzel | -1.0 | -1.0 | 0.0 | Droite | non_mover |  |
| Paul Vannier | 1.6428571428571428 | 1.7142857142857142 | 0.0714285714285714 | Gauche radicale | non_mover |  |
| Philippe Ballard | -1.2 | -1.25 | -0.05 | Droite | non_mover |  |
| Philippe Brun | -0.5 | 0.5454545454545454 | 1.0454545454545454 | Gauche moderee | modere |  |
| Philippe Gosselin | -1.4 | -1.0 | 0.3999999999999999 | Droite | non_mover |  |
| Philippe Juvin | -1.0 | -1.1666666666666667 | -0.1666666666666667 | Droite | non_mover |  |
| Philippe Schreck | -2.0 | -1.5 | 0.5 | Droite | non_mover |  |
| Pierre Cazeneuve | -1.0 | 1.0 | 2.0 | Centre / Majorite | fort |  |
| Pierre-Henri Dumont | -1.0 | -1.3333333333333333 | -0.3333333333333332 | Droite | non_mover |  |
| Pierre-Yves Cadalen | 1.3333333333333333 | 1.4745762711864407 | 0.1412429378531075 | Gauche radicale | non_mover |  |
| Raphaël Arnault | 1.542857142857143 | 1.736842105263158 | 0.193984962406015 | Gauche radicale | non_mover |  |
| René Pilato | 0.8571428571428571 | 1.608695652173913 | 0.751552795031056 | Gauche radicale | non_mover |  |
| Roger Chudeau | -2.0 | -2.0 | 0.0 | Droite | non_mover |  |
| Sabrina Sebaihi | 0.6666666666666666 | 1.3636363636363635 | 0.6969696969696969 | Gauche moderee | non_mover |  |
| Sarah Legrain | 1.5 | 1.8928571428571428 | 0.3928571428571428 | Gauche radicale | non_mover |  |
| Soumya Bourouaha | 1.5 | 1.5714285714285714 | 0.0714285714285714 | Gauche radicale | non_mover |  |
| Stéphane Peu | 0.8333333333333334 | 1.3 | 0.4666666666666667 | Gauche radicale | non_mover |  |
| Sylvain Maillard | -1.2 | -1.375 | -0.175 | Centre / Majorite | non_mover |  |
| Sébastien Chenu | -1.5416666666666667 | -1.44 | 0.1016666666666668 | Droite | non_mover |  |
| Sébastien Delogu | 1.8571428571428568 | 1.7857142857142858 | -0.0714285714285714 | Gauche radicale | non_mover |  |
| Ségolène Amiot | 1.6666666666666667 | 1.85 | 0.1833333333333333 | Gauche radicale | non_mover |  |
| Thomas Portes | 1.75 | 1.865612648221344 | 0.1156126482213439 | Gauche radicale | non_mover |  |
| Théo Bernhardt | -1.4545454545454546 | -1.25 | 0.2045454545454545 | Droite | non_mover |  |
| Ugo Bernalicis | 1.4 | 1.6538461538461535 | 0.2538461538461538 | Gauche radicale | non_mover |  |
| Violette Spillebout | 0.0 | 0.0 | 0.0 | Centre / Majorite | non_mover |  |
| Éric Bothorel | -0.6538461538461539 | -0.72 | -0.0661538461538461 | Centre / Majorite | non_mover |  |
| Éric Ciotti | -1.5 | -1.7272727272727273 | -0.2272727272727273 | Droite | non_mover |  |
| Éric Coquerel | 1.4 | 1.5925925925925926 | 0.1925925925925926 | Gauche radicale | non_mover |  |
| Éric Pauget | -1.6666666666666667 | -1.5 | 0.1666666666666667 | Droite | non_mover |  |

*(tronqué à 100 lignes — voir CSV pour données complètes)*


### pca_coordonnees.csv (459 lignes)

| author | bloc | PC1 | PC2 |
| --- | --- | --- | --- |
| Adrien Quatennens | Gauche radicale | 0.2280038886344695 | 0.1082608992567366 |
| Agnès Firmin Le Bodo | Centre / Majorite | -0.1630223775872886 | -0.1794721840270105 |
| Alexandre Portier | Droite | -0.1338247464518359 | -0.062235366505292 |
| Alexandre Sabatou | Droite | -0.2200924925544546 | -0.1561666213339691 |
| Alexis Jolly | Droite | 0.00414665090839 | -0.1034236408878363 |
| Alma Dufour | Gauche radicale | 0.324307854153454 | 0.0310757107951443 |
| Amélia Lakrafi | Centre / Majorite | 0.2814002498759472 | -0.0313014334166625 |
| Anne Sicard | Droite | -0.0192175778737282 | -0.1829526237560094 |
| Anne-Cécile Violland | Centre / Majorite | -0.1998054234397516 | -0.3149783800172032 |
| Antoine Léaument | Gauche radicale | 0.2193554793462816 | 0.1114064990678185 |
| Antoine Villedieu | Droite | 0.0550666278097919 | -0.074163912945141 |
| Arthur Delaporte | Gauche moderee | 0.202801019983108 | -0.1063707916001934 |
| Aurore Bergé | Centre / Majorite | 0.1135410105364831 | 0.0533948584228561 |
| Aurélien Lopez-Liguori | Droite | -0.4024981908288328 | -0.0622197056849246 |
| Aurélien Saintoul | Gauche radicale | 0.2977528454040069 | 0.0284594176176206 |
| Aurélien Taché | Gauche radicale | 0.2959613435219992 | 0.0370167144787857 |
| Ayda Hadizadeh | Gauche moderee | 0.1191091684768684 | 0.0031213664663087 |
| Aymeric Caron | Gauche radicale | 0.2708575629335717 | 0.1474778874553717 |
| Bastien Lachaud | Gauche radicale | 0.331912753029104 | -0.0026311839250999 |
| Belkhir Belhaddad | Centre / Majorite | -0.0414022330128151 | -0.1909930840330562 |
| Benjamin Haddad | Centre / Majorite | 0.1969654488791439 | -0.1613170584600482 |
| Boris Vallaud | Gauche moderee | 0.237913005247491 | -0.1078811207773048 |
| Brigitte Klinkert | Centre / Majorite | 0.1050150115716154 | -0.2735169877327395 |
| Brigitte Liso | Centre / Majorite | -0.3888030179512021 | -0.1856199333084032 |
| Bruno Bilde | Droite | 0.1859247865355702 | -0.0541353662001468 |
| Bruno Fuchs | Centre / Majorite | 0.1434047348171277 | -0.2099635253993677 |
| Bruno Millienne | Centre / Majorite | 0.0479083934972728 | 0.0475378576296324 |
| Bryan Masson | Droite | -0.0819775829414162 | -0.1219169756137094 |
| Carlos Martens Bilongo | Gauche radicale | 0.2994159508876112 | 0.0171745293090721 |
| Caroline Abadie | Centre / Majorite | -0.164478274634122 | -0.0165459961797958 |
| Caroline Colombier | Droite | -0.120379220766212 | -0.0489844536423598 |
| Caroline Parmentier | Droite | -0.0716487664336005 | -0.1327326686581651 |
| Caroline Yadan | Centre / Majorite | 0.2987104741715476 | -0.0307670797560701 |
| Catherine Couturier | Gauche radicale | 0.0967092054742151 | -0.0661738450439918 |
| Charles Sitzenstuhl | Centre / Majorite | -0.0370647110336046 | -0.0452640714502244 |
| Christophe Marion | Centre / Majorite | -0.1773732140575087 | -0.3182919644219229 |
| Claire Lejeune | Gauche radicale | 0.3005417754936139 | -0.0365809201291291 |
| Clémence Guetté | Gauche radicale | 0.2585952604134794 | -0.014573650310971 |
| Clémentine Autain | Gauche radicale | 0.3342846630872911 | -0.0703888925501731 |
| Constance Le Grip | Centre / Majorite | 0.2164066354717746 | -0.1626033062911437 |
| Cyrielle Chatelain | Gauche moderee | 0.2155926367008314 | -0.126179827639153 |
| Cécile Rilhac | Centre / Majorite | -0.0253877009062194 | -0.2594876046529712 |
| Céline Calvez | Centre / Majorite | 0.1236078591403256 | -0.2231306065859258 |
| Céline Hervieu | Gauche moderee | -0.36375882463513 | -0.0660702114268166 |
| Damien Maudet | Gauche radicale | 0.1859983170865642 | -0.0577193290949558 |
| Daniel Labaronne | Centre / Majorite | -0.035389305113709 | -0.2926003816685834 |
| Danielle Simonnet | Gauche moderee | 0.2390639896374469 | -0.1049940381328905 |
| Danièle Obono | Gauche radicale | 0.2778786243210513 | 0.0243061293878227 |
| David Guiraud | Gauche radicale | 0.3057642952409563 | 0.0540071978151743 |
| Didier Martin | Centre / Majorite | -0.1262312474764229 | -0.3765694323206884 |
| ... | ... | ... | ... |
| Philippe Ballard | Droite | 0.1349601363853731 | -0.1211120666697867 |
| Philippe Bonnecarrère | Droite | -0.320317445435974 | -0.0395724713353573 |
| Philippe Brun | Gauche moderee | 0.149590908124916 | -0.0211705683399108 |
| Philippe Gosselin | Droite | -0.1135837933106646 | -0.1630381916086746 |
| Philippe Juvin | Droite | 0.0029828774986114 | -0.0844367527779503 |
| Philippe Latombe | Centre / Majorite | -0.3379600630611558 | -0.304714607393839 |
| Philippe Schreck | Droite | 0.0399545943579991 | -0.079844910752837 |
| Pierre Cazeneuve | Centre / Majorite | 0.1400519384326743 | -0.2249045964483115 |
| Pierre Meurin | Droite | -0.3280259906192792 | -0.1833320070193508 |
| Pierre-Henri Dumont | Droite | 0.1692718273241094 | -0.1286437958900233 |
| Pierre-Yves Cadalen | Gauche radicale | 0.251372311755781 | -0.0368210575556886 |
| Pouria Amirshahi | Gauche moderee | 0.1242373458939283 | -0.0156796897224703 |
| Prisca Thevenot | Centre / Majorite | 0.0046197317828149 | 0.0104283512871335 |
| Raphaël Arnault | Gauche radicale | 0.245135581130226 | 0.0106931083021117 |
| René Pilato | Gauche radicale | 0.1205371092006717 | 0.0998139926691546 |
| Roger Chudeau | Droite | -0.0774445348156618 | -0.0490831404868816 |
| Sabrina Agresti-Roubache | Centre / Majorite | 0.0861011186060504 | -0.1665123588389378 |
| Sabrina Sebaihi | Gauche moderee | 0.3370549959110959 | -0.0269007533516029 |
| Sandra Regol | Gauche moderee | 0.0298724519588016 | -0.0532653928813773 |
| Sandrine Rousseau | Gauche moderee | 0.2206881792022956 | 0.0069618010713288 |
| Sarah Legrain | Gauche radicale | 0.2709926631149206 | 0.0590507969156721 |
| Sophie Blanc | Droite | -0.1308199826108996 | -0.0408460980706431 |
| Soumya Bourouaha | Gauche radicale | 0.285827058172479 | -0.0404238083999933 |
| Stéphane Mazars | Centre / Majorite | -0.364639821873822 | -0.314069735376845 |
| Stéphane Peu | Gauche radicale | 0.2117558771914921 | -0.1210349404421639 |
| Stéphanie Rist | Centre / Majorite | -0.4222574810426345 | -0.1196574195643116 |
| Sylvain Maillard | Centre / Majorite | 0.1544770814490748 | -0.1480158955705337 |
| Sylvie Bonnet | Droite | -0.3819490751327206 | -0.1238315193755813 |
| Sébastien Chenu | Droite | 0.1892152855619381 | -0.0231746853844359 |
| Sébastien Delogu | Gauche radicale | 0.2565641022069547 | -0.0493364324755706 |
| Sébastien Jumel | Gauche radicale | 0.1628256578341036 | -0.092576801658926 |
| Ségolène Amiot | Gauche radicale | 0.2655780942179335 | -0.0418386644745086 |
| Thomas Ménagé | Droite | 0.0217030369197481 | -0.1498998298465061 |
| Thomas Portes | Gauche radicale | 0.3085672885238836 | 0.0163207581823446 |
| Théo Bernhardt | Droite | 0.027576821768745 | -0.0516882539430109 |
| Ugo Bernalicis | Gauche radicale | 0.2965703333463162 | -0.0437337375811024 |
| Vincent Bru | Centre / Majorite | -0.1493905144564626 | -0.1471850139740988 |
| Vincent Jeanbrun | Droite | -0.2997950777486913 | -0.1262738488576997 |
| Violette Spillebout | Centre / Majorite | 0.1619697781788595 | -0.0051097867003694 |
| Virginie Duby-Muller | Droite | -0.2697083103063406 | -0.4110321042687704 |
| William Martinet | Gauche radicale | 0.1507538375027151 | 0.0189336301822515 |
| Yoann Gillet | Droite | 0.0304423524294269 | -0.1516620642594068 |
| Élisabeth de Maistre | Droite | -0.4294203557985315 | -0.0179731539860706 |
| Élise Leboucher | Gauche radicale | 0.2263790958972921 | -0.0688661726100289 |
| Éric Bothorel | Centre / Majorite | 0.1866110444183407 | -0.1101712917553528 |
| Éric Ciotti | Droite | 0.2114330826909836 | -0.1915598608813643 |
| Éric Coquerel | Gauche radicale | 0.3357452227789061 | 0.0081112682679363 |
| Éric Pauget | Droite | 0.1925728726967285 | -0.0984502582827099 |
| Éric Poulliat | Centre / Majorite | -0.1644147320231238 | -0.1435515944457956 |

*(tronqué à 100 lignes — voir CSV pour données complètes)*


## 07 — Emotions et registres

### emotional_register.csv (4 lignes)

| bloc | anger | defense | defiance | fear | grief | indignation | neutral | solidarity |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Gauche radicale | 0.041271611823759 | 0.0 | 0.0083658672615727 | 0.0016731734523145 | 0.0736196319018405 | 0.6366424986056888 | 0.1137757947573898 | 0.1246514221974344 |
| Gauche moderee | 0.0108695652173913 | 0.0 | 0.0018115942028985 | 0.0054347826086956 | 0.1775362318840579 | 0.3713768115942029 | 0.2989130434782608 | 0.1340579710144927 |
| Centre / Majorite | 0.0010905125408942 | 0.0021810250817884 | 0.0937840785169029 | 0.0327153762268266 | 0.109051254089422 | 0.2671755725190839 | 0.4394765539803708 | 0.054525627044711 |
| Droite | 0.0152941176470588 | 0.0 | 0.4117647058823529 | 0.0376470588235294 | 0.0294117647058823 | 0.3647058823529411 | 0.1152941176470588 | 0.0258823529411764 |


### frames_par_bloc.csv (4 lignes)

| bloc | DIP | ECO | EDU | HIS | HUM | HUM+LEG | LEG | MOR | POL | SEC |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Gauche radicale | 0.0177237439578145 | 0.0052731800205068 | 0.0 | 0.0048337483521312 | 0.7722279185586641 | 0.0001464772227918 | 0.0952101948147063 | 0.08129485864948 | 0.0 | 0.023289878423905 |
| Gauche moderee | 0.0599173553719008 | 0.0113636363636363 | 0.0 | 0.006198347107438 | 0.640495867768595 | 0.0010330578512396 | 0.1549586776859504 | 0.0888429752066115 | 0.0 | 0.0371900826446281 |
| Centre / Majorite | 0.1189516129032258 | 0.0040322580645161 | 0.0006720430107526 | 0.0295698924731182 | 0.290994623655914 | 0.0 | 0.0403225806451612 | 0.209005376344086 | 0.0006720430107526 | 0.3057795698924731 |
| Droite | 0.0271186440677966 | 0.0128813559322033 | 0.0 | 0.0447457627118644 | 0.1105084745762711 | 0.0 | 0.015593220338983 | 0.3410169491525424 | 0.0 | 0.4481355932203389 |


### registre_conflictuel_bloc_batch.csv (28 lignes)

| bloc | batch | registre_conflictuel_moyen | n |
| --- | --- | --- | --- |
| Centre / Majorite | CEASEFIRE_BREACH | 0.553030303030303 | 132 |
| Centre / Majorite | CHOC | 0.543010752688172 | 372 |
| Centre / Majorite | MANDATS_CPI | 0.5833333333333334 | 6 |
| Centre / Majorite | NEW_OFFENSIVE | 0.5238663484486874 | 419 |
| Centre / Majorite | POST_CIJ | 0.5398773006134969 | 163 |
| Centre / Majorite | POST_SINWAR | 0.5166666666666667 | 30 |
| Centre / Majorite | RAFAH | 0.5544554455445545 | 303 |
| Droite | CEASEFIRE_BREACH | 0.5256410256410257 | 117 |
| Droite | CHOC | 0.541371158392435 | 423 |
| Droite | MANDATS_CPI | 0.5 | 15 |
| Droite | NEW_OFFENSIVE | 0.5335731414868106 | 417 |
| Droite | POST_CIJ | 0.5224358974358975 | 156 |
| Droite | POST_SINWAR | 0.5581395348837209 | 43 |
| Droite | RAFAH | 0.5347985347985348 | 273 |
| Gauche moderee | CEASEFIRE_BREACH | 0.5677966101694916 | 59 |
| Gauche moderee | CHOC | 0.575967261904762 | 224 |
| Gauche moderee | MANDATS_CPI | 0.55 | 10 |
| Gauche moderee | NEW_OFFENSIVE | 0.5485611510791367 | 278 |
| Gauche moderee | POST_CIJ | 0.5528169014084507 | 142 |
| Gauche moderee | POST_SINWAR | 0.5131578947368421 | 38 |
| Gauche moderee | RAFAH | 0.5552631578947368 | 190 |
| Gauche radicale | CEASEFIRE_BREACH | 0.5575620767494357 | 443 |
| Gauche radicale | CHOC | 0.5621693121693122 | 1134 |
| Gauche radicale | MANDATS_CPI | 0.5533980582524272 | 103 |
| Gauche radicale | NEW_OFFENSIVE | 0.5498631074606434 | 2435 |
| Gauche radicale | POST_CIJ | 0.5465116279069767 | 817 |
| Gauche radicale | POST_SINWAR | 0.5574162679425837 | 209 |
| Gauche radicale | RAFAH | 0.5601631543167913 | 1471 |


## 10 — Twitter vs AN

### stance_twitter_vs_an_by_deputy.csv (231 lignes)

| author_norm | month | bloc | stance_tw | n_tweets | engagement_mean | stance_an | n_an | delta | month_ts |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Adrien Quatennens | 2023-10 | Gauche radicale | 1.1666666666666667 | 6 | 931.6666666666666 | -1.0 | 2 | 2.166666666666667 | 2023-10-01 |
| Alexandre Sabatou | 2024-04 | Droite | -1.0 | 1 | 93.0 | 0.0 | 1 | -1.0 | 2024-04-01 |
| Alma Dufour | 2023-12 | Gauche radicale | 1.5 | 4 | 489.5 | 1.6666666666666667 | 3 | -0.1666666666666667 | 2023-12-01 |
| Alma Dufour | 2024-05 | Gauche radicale | 1.761904761904762 | 21 | 393.1904761904762 | 2.0 | 6 | -0.2380952380952381 | 2024-05-01 |
| Alma Dufour | 2025-01 | Gauche radicale | 1.0 | 4 | 651.5 | 2.0 | 3 | -1.0 | 2025-01-01 |
| Alma Dufour | 2025-06 | Gauche radicale | 1.5666666666666669 | 30 | 575.4666666666667 | 1.8 | 5 | -0.2333333333333334 | 2025-06-01 |
| Amélia Lakrafi | 2024-10 | Centre / Majorite | 0.3333333333333333 | 6 | 7.5 | -1.0 | 1 | 1.3333333333333333 | 2024-10-01 |
| Antoine Léaument | 2023-10 | Gauche radicale | 1.2142857142857142 | 14 | 893.3571428571429 | 0.0 | 2 | 1.2142857142857142 | 2023-10-01 |
| Antoine Léaument | 2024-05 | Gauche radicale | 1.75 | 8 | 887.25 | 1.0 | 1 | 0.75 | 2024-05-01 |
| Antoine Léaument | 2024-10 | Gauche radicale | 2.0 | 1 | 891.0 | -2.0 | 1 | 4.0 | 2024-10-01 |
| Antoine Léaument | 2025-03 | Gauche radicale | 2.0 | 1 | 624.0 | 1.0 | 1 | 1.0 | 2025-03-01 |
| Antoine Léaument | 2025-10 | Gauche radicale | 1.0 | 1 | 913.0 | 1.0 | 1 | 0.0 | 2025-10-01 |
| Aurore Bergé | 2024-11 | Centre / Majorite | -1.0 | 2 | 718.0 | -2.0 | 1 | 1.0 | 2024-11-01 |
| Aurore Bergé | 2025-01 | Centre / Majorite | -1.0 | 4 | 826.75 | -1.3333333333333333 | 3 | 0.3333333333333332 | 2025-01-01 |
| Aurore Bergé | 2025-02 | Centre / Majorite | -1.0 | 7 | 585.2857142857143 | -1.0 | 1 | 0.0 | 2025-02-01 |
| Aurore Bergé | 2025-03 | Centre / Majorite | -1.0 | 2 | 1037.5 | -1.1666666666666667 | 6 | 0.1666666666666667 | 2025-03-01 |
| Aurore Bergé | 2025-05 | Centre / Majorite | -1.0 | 1 | 1534.0 | -1.25 | 8 | 0.25 | 2025-05-01 |
| Aurore Bergé | 2025-07 | Centre / Majorite | -1.0 | 2 | 782.5 | -1.3333333333333333 | 6 | 0.3333333333333332 | 2025-07-01 |
| Aurélien Saintoul | 2023-10 | Gauche radicale | 1.5 | 4 | 289.0 | 0.0 | 1 | 1.5 | 2023-10-01 |
| Aurélien Saintoul | 2025-06 | Gauche radicale | 1.5 | 16 | 638.5 | 0.5 | 2 | 1.0 | 2025-06-01 |
| Ayda Hadizadeh | 2025-05 | Gauche moderee | 0.6666666666666666 | 3 | 78.66666666666667 | 2.0 | 1 | -1.3333333333333337 | 2025-05-01 |
| Ayda Hadizadeh | 2025-06 | Gauche moderee | 0.2857142857142857 | 7 | 242.14285714285717 | 1.3333333333333333 | 3 | -1.0476190476190474 | 2025-06-01 |
| Aymeric Caron | 2023-10 | Gauche radicale | 1.2 | 35 | 539.6285714285714 | 0.0 | 6 | 1.2 | 2023-10-01 |
| Aymeric Caron | 2024-06 | Gauche radicale | 1.0 | 3 | 893.6666666666666 | 2.0 | 3 | -1.0 | 2024-06-01 |
| Aymeric Caron | 2025-04 | Gauche radicale | 1.7377049180327868 | 61 | 500.2950819672131 | 2.0 | 4 | -0.2622950819672132 | 2025-04-01 |
| Aymeric Caron | 2025-05 | Gauche radicale | 1.9166666666666667 | 12 | 886.3333333333334 | -0.6666666666666666 | 3 | 2.583333333333333 | 2025-05-01 |
| Bastien Lachaud | 2024-05 | Gauche radicale | 1.625 | 8 | 278.5 | 2.0 | 1 | -0.375 | 2024-05-01 |
| Bastien Lachaud | 2025-03 | Gauche radicale | 2.0 | 1 | 143.0 | 0.0 | 1 | 2.0 | 2025-03-01 |
| Bastien Lachaud | 2025-05 | Gauche radicale | 2.0 | 1 | 1186.0 | 1.0 | 1 | 1.0 | 2025-05-01 |
| Bastien Lachaud | 2025-06 | Gauche radicale | 1.5 | 4 | 431.5 | 1.0 | 1 | 0.5 | 2025-06-01 |
| Boris Vallaud | 2023-10 | Gauche moderee | 1.0 | 4 | 400.0 | 0.8 | 10 | 0.1999999999999999 | 2023-10-01 |
| Brigitte Klinkert | 2025-06 | Centre / Majorite | -1.0 | 1 | 5.0 | -1.0 | 1 | 0.0 | 2025-06-01 |
| Bruno Fuchs | 2025-06 | Centre / Majorite | 0.25 | 4 | 18.25 | -1.0 | 1 | 1.25 | 2025-06-01 |
| Carlos Martens Bilongo | 2023-11 | Gauche radicale | 1.0 | 1 | 23.0 | 1.0 | 3 | 0.0 | 2023-11-01 |
| Caroline Abadie | 2023-10 | Centre / Majorite | -1.0 | 1 | 26.0 | -1.0 | 1 | 0.0 | 2023-10-01 |
| Caroline Yadan | 2023-10 | Centre / Majorite | -1.3333333333333333 | 3 | 459.3333333333333 | -1.5 | 4 | 0.1666666666666667 | 2023-10-01 |
| Caroline Yadan | 2023-11 | Centre / Majorite | -0.5714285714285714 | 7 | 231.8571428571429 | -1.0 | 3 | 0.4285714285714286 | 2023-11-01 |
| Caroline Yadan | 2024-01 | Centre / Majorite | -1.4210526315789471 | 19 | 216.21052631578948 | -1.0 | 1 | -0.4210526315789473 | 2024-01-01 |
| Caroline Yadan | 2024-02 | Centre / Majorite | -1.4210526315789471 | 19 | 265.89473684210526 | -1.3333333333333333 | 3 | -0.087719298245614 | 2024-02-01 |
| Caroline Yadan | 2024-03 | Centre / Majorite | -1.5 | 2 | 498.0 | -1.5 | 4 | 0.0 | 2024-03-01 |
| Caroline Yadan | 2024-11 | Centre / Majorite | -1.2 | 15 | 856.0 | -1.0 | 1 | -0.1999999999999999 | 2024-11-01 |
| Caroline Yadan | 2025-01 | Centre / Majorite | -1.0 | 1 | 250.0 | -1.3333333333333333 | 3 | 0.3333333333333332 | 2025-01-01 |
| Caroline Yadan | 2025-04 | Centre / Majorite | -1.0 | 4 | 652.0 | -1.6666666666666667 | 3 | 0.6666666666666667 | 2025-04-01 |
| Caroline Yadan | 2025-05 | Centre / Majorite | -0.6153846153846154 | 13 | 608.8461538461538 | -1.4705882352941178 | 17 | 0.8552036199095023 | 2025-05-01 |
| Caroline Yadan | 2025-06 | Centre / Majorite | -1.2 | 15 | 571.8 | -1.5 | 4 | 0.3 | 2025-06-01 |
| Caroline Yadan | 2025-10 | Centre / Majorite | -1.2307692307692308 | 13 | 689.4615384615385 | -1.7142857142857142 | 7 | 0.4835164835164833 | 2025-10-01 |
| Caroline Yadan | 2025-11 | Centre / Majorite | -2.0 | 2 | 1105.5 | -2.0 | 1 | 0.0 | 2025-11-01 |
| Caroline Yadan | 2025-12 | Centre / Majorite | -1.5 | 4 | 363.25 | -2.0 | 2 | 0.5 | 2025-12-01 |
| Claire Lejeune | 2025-07 | Gauche radicale | 2.0 | 4 | 485.5 | 2.0 | 1 | 0.0 | 2025-07-01 |
| Clémence Guetté | 2025-06 | Gauche radicale | 2.0 | 3 | 859.0 | 2.0 | 2 | 0.0 | 2025-06-01 |
| Constance Le Grip | 2023-10 | Centre / Majorite | -1.25 | 12 | 106.5 | -1.5 | 10 | 0.25 | 2023-10-01 |
| Constance Le Grip | 2024-10 | Centre / Majorite | -1.6666666666666667 | 3 | 26.666666666666668 | -1.5 | 2 | -0.1666666666666667 | 2024-10-01 |
| Constance Le Grip | 2025-02 | Centre / Majorite | -1.3333333333333333 | 3 | 23.0 | -1.0 | 1 | -0.3333333333333332 | 2025-02-01 |
| Constance Le Grip | 2025-06 | Centre / Majorite | -0.9230769230769232 | 13 | 75.3076923076923 | 0.0 | 1 | -0.9230769230769232 | 2025-06-01 |
| Cyrielle Chatelain | 2023-10 | Gauche moderee | 0.875 | 8 | 103.875 | 1.125 | 8 | -0.25 | 2023-10-01 |
| Cyrielle Chatelain | 2024-05 | Gauche moderee | 1.0 | 5 | 206.2 | 1.25 | 4 | -0.25 | 2024-05-01 |
| Cyrielle Chatelain | 2024-11 | Gauche moderee | 1.0 | 2 | 54.5 | 1.4 | 5 | -0.3999999999999999 | 2024-11-01 |
| Danièle Obono | 2024-01 | Gauche radicale | 1.903225806451613 | 31 | 309.8709677419355 | 2.0 | 1 | -0.096774193548387 | 2024-01-01 |
| Danièle Obono | 2024-03 | Gauche radicale | 1.6153846153846154 | 13 | 193.3846153846154 | 1.6666666666666667 | 3 | -0.0512820512820513 | 2024-03-01 |
| Danièle Obono | 2024-11 | Gauche radicale | 1.75 | 4 | 354.75 | 2.0 | 6 | -0.25 | 2024-11-01 |
| Danièle Obono | 2025-02 | Gauche radicale | 2.0 | 4 | 287.0 | -2.0 | 1 | 4.0 | 2025-02-01 |
| Danièle Obono | 2025-03 | Gauche radicale | 1.5 | 4 | 172.0 | 2.0 | 1 | -0.5 | 2025-03-01 |
| David Guiraud | 2023-10 | Gauche radicale | 1.6458333333333333 | 48 | 546.0208333333334 | 2.0 | 1 | -0.3541666666666667 | 2023-10-01 |
| David Guiraud | 2024-05 | Gauche radicale | 1.5 | 18 | 356.0 | 2.0 | 2 | -0.5 | 2024-05-01 |
| David Guiraud | 2024-11 | Gauche radicale | 1.8333333333333333 | 6 | 385.0 | 1.4285714285714286 | 7 | 0.4047619047619046 | 2024-11-01 |
| David Guiraud | 2025-05 | Gauche radicale | 2.0 | 7 | 632.5714285714286 | -0.3333333333333333 | 3 | 2.333333333333333 | 2025-05-01 |
| Didier Martin | 2023-10 | Centre / Majorite | -1.0 | 1 | 14.0 | -1.0 | 1 | 0.0 | 2023-10-01 |
| Dominique Potier | 2023-10 | Gauche moderee | 0.3333333333333333 | 3 | 23.666666666666668 | 0.0 | 1 | 0.3333333333333333 | 2023-10-01 |
| Elsa Faucillon | 2023-11 | Gauche radicale | 1.2 | 5 | 549.0 | 1.6666666666666667 | 6 | -0.4666666666666668 | 2023-11-01 |
| Elsa Faucillon | 2024-05 | Gauche radicale | 1.625 | 8 | 678.625 | 1.8571428571428568 | 7 | -0.2321428571428572 | 2024-05-01 |
| Elsa Faucillon | 2024-10 | Gauche radicale | 2.0 | 3 | 298.6666666666667 | 2.0 | 2 | 0.0 | 2024-10-01 |
| Elsa Faucillon | 2025-03 | Gauche radicale | 1.5 | 2 | 189.0 | 1.0 | 1 | 0.5 | 2025-03-01 |
| Elsa Faucillon | 2025-06 | Gauche radicale | 1.7857142857142858 | 14 | 306.1428571428572 | 2.0 | 1 | -0.2142857142857142 | 2025-06-01 |
| Elsa Faucillon | 2025-10 | Gauche radicale | 2.0 | 1 | 76.0 | 2.0 | 1 | 0.0 | 2025-10-01 |
| Emmanuel Fernandes | 2024-05 | Gauche radicale | 1.7272727272727273 | 11 | 105.27272727272728 | 2.0 | 1 | -0.2727272727272727 | 2024-05-01 |
| ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |
| Olivier Faure | 2025-01 | Gauche moderee | 1.0 | 2 | 792.5 | 0.0 | 1 | 1.0 | 2025-01-01 |
| Olivier Faure | 2025-06 | Gauche moderee | 1.1428571428571428 | 7 | 554.0 | 0.0 | 1 | 1.1428571428571428 | 2025-06-01 |
| Olivier Fayssat | 2025-07 | Droite | -1.25 | 4 | 20.0 | -1.5 | 2 | 0.25 | 2025-07-01 |
| Paul Vannier | 2024-03 | Gauche radicale | 2.0 | 2 | 391.5 | 2.0 | 1 | 0.0 | 2024-03-01 |
| Philippe Ballard | 2023-10 | Droite | -1.75 | 4 | 169.0 | -1.0 | 1 | -0.75 | 2023-10-01 |
| Philippe Juvin | 2025-10 | Droite | -1.0 | 2 | 160.5 | -1.0 | 1 | 0.0 | 2025-10-01 |
| Pierre Cazeneuve | 2024-10 | Centre / Majorite | -1.0 | 1 | 105.0 | 0.0 | 1 | -1.0 | 2024-10-01 |
| Pierre Meurin | 2023-10 | Droite | -1.5 | 2 | 29.5 | 2.0 | 1 | -3.5 | 2023-10-01 |
| Pierre-Henri Dumont | 2023-11 | Droite | -1.0 | 1 | 302.0 | -1.0 | 2 | 0.0 | 2023-11-01 |
| Pierre-Henri Dumont | 2024-03 | Droite | -2.0 | 1 | 106.0 | -2.0 | 3 | 0.0 | 2024-03-01 |
| Pierre-Henri Dumont | 2024-04 | Droite | -1.6 | 5 | 291.4 | -1.0 | 1 | -0.6000000000000001 | 2024-04-01 |
| Pierre-Yves Cadalen | 2024-10 | Gauche radicale | 1.25 | 4 | 66.25 | 2.0 | 1 | -0.75 | 2024-10-01 |
| Pierre-Yves Cadalen | 2025-06 | Gauche radicale | 1.5 | 36 | 299.8888888888889 | 2.0 | 4 | -0.5 | 2025-06-01 |
| Pierre-Yves Cadalen | 2025-12 | Gauche radicale | -1.0 | 1 | 416.0 | 2.0 | 1 | -3.0 | 2025-12-01 |
| Raphaël Arnault | 2025-01 | Gauche radicale | 1.75 | 4 | 728.25 | -2.0 | 1 | 3.75 | 2025-01-01 |
| Raphaël Arnault | 2025-02 | Gauche radicale | 0.6666666666666666 | 3 | 465.3333333333333 | 2.0 | 1 | -1.3333333333333337 | 2025-02-01 |
| Raphaël Arnault | 2025-05 | Gauche radicale | 1.8571428571428568 | 7 | 813.4285714285714 | 0.4285714285714285 | 7 | 1.4285714285714286 | 2025-05-01 |
| René Pilato | 2025-07 | Gauche radicale | 1.8461538461538465 | 13 | 282.2307692307692 | -2.0 | 1 | 3.8461538461538463 | 2025-07-01 |
| René Pilato | 2025-10 | Gauche radicale | -1.0 | 1 | 135.0 | 2.0 | 1 | -3.0 | 2025-10-01 |
| Roger Chudeau | 2024-04 | Droite | -1.0 | 1 | 20.0 | -2.0 | 2 | 1.0 | 2024-04-01 |
| Roger Chudeau | 2025-05 | Droite | -2.0 | 1 | 21.0 | -1.8333333333333333 | 6 | -0.1666666666666667 | 2025-05-01 |
| Roger Chudeau | 2025-07 | Droite | -2.0 | 1 | 20.0 | -1.8888888888888888 | 9 | -0.1111111111111111 | 2025-07-01 |
| Sabrina Sebaihi | 2023-10 | Gauche moderee | 1.0 | 3 | 114.66666666666669 | 1.5 | 2 | -0.5 | 2023-10-01 |
| Sabrina Sebaihi | 2023-12 | Gauche moderee | 0.3333333333333333 | 3 | 582.6666666666666 | 2.0 | 1 | -1.6666666666666667 | 2023-12-01 |
| Sabrina Sebaihi | 2024-02 | Gauche moderee | 1.3870967741935485 | 31 | 137.16129032258064 | 1.6666666666666667 | 3 | -0.2795698924731182 | 2024-02-01 |
| Sabrina Sebaihi | 2024-03 | Gauche moderee | 1.5384615384615383 | 13 | 196.53846153846155 | 2.0 | 3 | -0.4615384615384614 | 2024-03-01 |
| Sabrina Sebaihi | 2024-06 | Gauche moderee | 1.0 | 1 | 46.0 | 2.0 | 6 | -1.0 | 2024-06-01 |
| Sabrina Sebaihi | 2024-10 | Gauche moderee | 1.375 | 8 | 219.125 | 2.0 | 1 | -0.625 | 2024-10-01 |
| Sabrina Sebaihi | 2025-04 | Gauche moderee | 1.3333333333333333 | 3 | 560.0 | 1.75 | 4 | -0.4166666666666667 | 2025-04-01 |
| Sabrina Sebaihi | 2025-06 | Gauche moderee | 1.2142857142857142 | 14 | 134.85714285714286 | 2.0 | 1 | -0.7857142857142858 | 2025-06-01 |
| Sandrine Rousseau | 2023-10 | Gauche moderee | 1.4285714285714286 | 7 | 1039.0 | 1.25 | 4 | 0.1785714285714286 | 2023-10-01 |
| Sandrine Rousseau | 2024-06 | Gauche moderee | 0.0 | 1 | 284.0 | 2.0 | 1 | -2.0 | 2024-06-01 |
| Sarah Legrain | 2025-05 | Gauche radicale | 1.0 | 1 | 49.0 | 2.0 | 1 | -1.0 | 2025-05-01 |
| Soumya Bourouaha | 2024-02 | Gauche radicale | 0.9473684210526316 | 19 | 45.8421052631579 | 0.5 | 4 | 0.4473684210526315 | 2024-02-01 |
| Soumya Bourouaha | 2025-02 | Gauche radicale | 2.0 | 1 | 47.0 | 2.0 | 1 | 0.0 | 2025-02-01 |
| Soumya Bourouaha | 2025-06 | Gauche radicale | 1.4285714285714286 | 7 | 38.142857142857146 | 2.0 | 1 | -0.5714285714285714 | 2025-06-01 |
| Stéphane Peu | 2025-06 | Gauche radicale | 1.6666666666666667 | 3 | 488.3333333333333 | 0.0 | 1 | 1.6666666666666667 | 2025-06-01 |
| Stéphane Peu | 2025-09 | Gauche radicale | 1.3333333333333333 | 3 | 707.0 | 2.0 | 1 | -0.6666666666666667 | 2025-09-01 |
| Sylvain Maillard | 2023-10 | Centre / Majorite | -1.2222222222222223 | 9 | 397.55555555555554 | -1.0 | 2 | -0.2222222222222223 | 2023-10-01 |
| Sylvain Maillard | 2023-11 | Centre / Majorite | -1.0 | 1 | 1274.0 | -1.6666666666666667 | 3 | 0.6666666666666667 | 2023-11-01 |
| Sylvain Maillard | 2024-05 | Centre / Majorite | -0.8333333333333334 | 6 | 269.3333333333333 | -0.75 | 4 | -0.0833333333333333 | 2024-05-01 |
| Sylvain Maillard | 2025-05 | Centre / Majorite | -2.0 | 1 | 266.0 | -1.0 | 1 | -1.0 | 2025-05-01 |
| Sébastien Chenu | 2023-10 | Droite | -1.5263157894736843 | 19 | 442.2631578947368 | -2.0 | 1 | 0.4736842105263157 | 2023-10-01 |
| Sébastien Chenu | 2024-03 | Droite | -2.0 | 1 | 941.0 | -2.0 | 1 | 0.0 | 2024-03-01 |
| Sébastien Chenu | 2024-05 | Droite | -1.5 | 4 | 541.25 | -2.0 | 1 | 0.5 | 2024-05-01 |
| Sébastien Chenu | 2024-10 | Droite | -1.0 | 2 | 225.5 | 2.0 | 1 | -3.0 | 2024-10-01 |
| Sébastien Chenu | 2025-04 | Droite | -1.3333333333333333 | 3 | 492.0 | -2.0 | 1 | 0.6666666666666667 | 2025-04-01 |
| Sébastien Chenu | 2025-06 | Droite | -1.8333333333333333 | 6 | 710.3333333333334 | -2.0 | 2 | 0.1666666666666667 | 2025-06-01 |
| Sébastien Delogu | 2023-11 | Gauche radicale | 2.0 | 8 | 665.375 | -0.5 | 2 | 2.5 | 2023-11-01 |
| Sébastien Delogu | 2024-04 | Gauche radicale | 1.25 | 4 | 669.0 | 0.75 | 4 | 0.5 | 2024-04-01 |
| Sébastien Delogu | 2024-05 | Gauche radicale | 2.0 | 3 | 621.3333333333334 | 2.0 | 6 | 0.0 | 2024-05-01 |
| Sébastien Delogu | 2025-02 | Gauche radicale | 1.0 | 1 | 1022.0 | -2.0 | 1 | 3.0 | 2025-02-01 |
| Sébastien Jumel | 2023-10 | Gauche radicale | 0.875 | 16 | 181.5625 | 0.0 | 1 | 0.875 | 2023-10-01 |
| Ségolène Amiot | 2024-11 | Gauche radicale | 1.0 | 1 | 34.0 | -1.0 | 1 | 2.0 | 2024-11-01 |
| Ségolène Amiot | 2025-06 | Gauche radicale | 2.0 | 6 | 385.8333333333333 | 2.0 | 1 | 0.0 | 2025-06-01 |
| Ségolène Amiot | 2025-10 | Gauche radicale | 1.8 | 5 | 101.2 | 1.0 | 1 | 0.8 | 2025-10-01 |
| Thomas Portes | 2023-11 | Gauche radicale | 2.0 | 4 | 473.5 | -2.0 | 1 | 4.0 | 2023-11-01 |
| Thomas Portes | 2024-03 | Gauche radicale | 2.0 | 9 | 951.2222222222222 | 1.1111111111111112 | 9 | 0.8888888888888888 | 2024-03-01 |
| Thomas Portes | 2024-05 | Gauche radicale | 1.9411764705882355 | 68 | 808.5 | 2.0 | 1 | -0.0588235294117647 | 2024-05-01 |
| Thomas Portes | 2024-10 | Gauche radicale | 1.9090909090909087 | 11 | 687.6363636363636 | 2.0 | 3 | -0.0909090909090908 | 2024-10-01 |
| Thomas Portes | 2025-11 | Gauche radicale | 2.0 | 3 | 893.0 | 2.0 | 3 | 0.0 | 2025-11-01 |
| Théo Bernhardt | 2025-06 | Droite | -0.5 | 2 | 13.0 | -2.0 | 1 | 1.5 | 2025-06-01 |
| Ugo Bernalicis | 2025-07 | Gauche radicale | 1.7142857142857142 | 7 | 540.2857142857143 | 1.0 | 1 | 0.7142857142857142 | 2025-07-01 |
| Vincent Jeanbrun | 2025-03 | Droite | -2.0 | 2 | 115.0 | -0.8 | 5 | -1.2 | 2025-03-01 |
| Violette Spillebout | 2024-04 | Centre / Majorite | -0.5 | 8 | 350.0 | -0.6666666666666666 | 3 | 0.1666666666666666 | 2024-04-01 |
| Éric Bothorel | 2023-10 | Centre / Majorite | -0.5555555555555556 | 18 | 22.11111111111111 | 0.0 | 1 | -0.5555555555555556 | 2023-10-01 |
| Éric Ciotti | 2023-10 | Droite | -1.55 | 20 | 729.0 | -2.0 | 1 | 0.4499999999999999 | 2023-10-01 |
| Éric Ciotti | 2023-12 | Droite | -1.0 | 1 | 628.0 | -2.0 | 1 | 1.0 | 2023-12-01 |
| Éric Ciotti | 2025-05 | Droite | -1.5 | 2 | 385.0 | -1.0 | 1 | -0.5 | 2025-05-01 |
| Éric Ciotti | 2025-06 | Droite | -1.7142857142857142 | 7 | 789.5714285714286 | -1.3333333333333333 | 3 | -0.3809523809523809 | 2025-06-01 |
| Éric Coquerel | 2023-11 | Gauche radicale | 1.4 | 20 | 851.85 | 1.0 | 3 | 0.3999999999999999 | 2023-11-01 |
| Éric Coquerel | 2023-12 | Gauche radicale | 1.5 | 4 | 557.75 | 1.6 | 5 | -0.1 | 2023-12-01 |
| Éric Coquerel | 2024-02 | Gauche radicale | 1.0 | 1 | 152.0 | 1.3333333333333333 | 3 | -0.3333333333333332 | 2024-02-01 |
| Éric Coquerel | 2025-01 | Gauche radicale | 1.75 | 4 | 492.25 | 1.4 | 5 | 0.3500000000000001 | 2025-01-01 |

*(tronqué à 150 lignes — voir CSV pour données complètes)*


### regression_delta_stance.csv (12 lignes)

| param | coef | pvalue |
| --- | --- | --- |
| Intercept | 0.0317259432584357 | 0.9058235661870092 |
| C(bloc)[T.Droite] | -0.151646091358111 | 0.5169034301006096 |
| C(bloc)[T.Gauche moderee] | -0.4191473907737591 | 0.1320486705775218 |
| C(bloc)[T.Gauche radicale] | 0.5036437207249715 | 0.0107533964363849 |
| C(batch)[T.CHOC] | 0.1195775593296056 | 0.6559853987339928 |
| C(batch)[T.NEW_OFFENSIVE] | -0.0456273207592581 | 0.8567895688540537 |
| C(batch)[T.OTHER] | -0.3207608334495984 | 0.6426498124569917 |
| C(batch)[T.POST_CIJ] | -0.0965835566990968 | 0.7589630637575637 |
| C(batch)[T.POST_SINWAR] | -0.1684820519686332 | 0.6793499153191092 |
| C(batch)[T.RAFAH] | -0.4573809554273342 | 0.1191064579198283 |
| n_tweets | -0.0055714919763634 | 0.5007185582992828 |
| engagement_mean | 0.0003129118184793 | 0.1435158049359586 |


### fighting_words_twitter_vs_an.csv (120 lignes)

| bloc | word | z | arena_favorisee |
| --- | --- | --- | --- |
| Gauche radicale | vous | -21.70606931939261 | AN |
| Gauche radicale | mêmes | -13.638827726316208 | AN |
| Gauche radicale | monsieur | -12.426743345618176 | AN |
| Gauche radicale | ministre | -11.987248537101914 | AN |
| Gauche radicale | premier | -10.535803164082646 | AN |
| Gauche radicale | mouvements | -9.873008492043793 | AN |
| Gauche radicale | avez | -9.79647343175314 | AN |
| Gauche radicale | gaza | 8.52250848604871 | Twitter |
| Gauche radicale | madame | -8.114772094218557 | AN |
| Gauche radicale | première | -7.896696729441133 | AN |
| Gauche radicale | allez | -7.823358751814595 | AN |
| Gauche radicale | massacres | 7.2762827202003475 | Twitter |
| Gauche radicale | pour | 7.111364612177868 | Twitter |
| Gauche radicale | votre | -6.669162416454219 | AN |
| Gauche radicale | génocide | 6.638562804291101 | Twitter |
| Gauche radicale | bancs | -6.60814738170665 | AN |
| Gauche radicale | antisémitisme | -6.593824168066343 | AN |
| Gauche radicale | texte | -6.566044426439345 | AN |
| Gauche radicale | où | -6.359470059732859 | AN |
| Gauche radicale | quand | -6.294221526701564 | AN |
| Gauche radicale | lorsque | -6.016823801794573 | AN |
| Gauche radicale | êtes | -5.961882994501528 | AN |
| Gauche radicale | celle | -5.85524047681828 | AN |
| Gauche radicale | vingt | -5.835337630953293 | AN |
| Gauche radicale | pourtant | -5.73804026252108 | AN |
| Gauche radicale | nous | -5.708180000931137 | AN |
| Gauche radicale | huit | -5.4121736020838505 | AN |
| Gauche radicale | unies | -5.317015237443855 | AN |
| Gauche radicale | lutter | -5.281544172199325 | AN |
| Gauche radicale | dix | -5.18739843312411 | AN |
| Gauche moderee | vous | -8.571977564311783 | AN |
| Gauche moderee | gaza | 7.928277024954351 | Twitter |
| Gauche moderee | ministre | -6.469335704478247 | AN |
| Gauche moderee | palestine | 6.103173440285291 | Twitter |
| Gauche moderee | à | 5.623563083495684 | Twitter |
| Gauche moderee | nous | -5.44136007005175 | AN |
| Gauche moderee | votre | -5.365859650700457 | AN |
| Gauche moderee | dans | -4.127410212212851 | AN |
| Gauche moderee | question | -4.111748094119901 | AN |
| Gauche moderee | reconnaissance | 4.063165710330537 | Twitter |
| Gauche moderee | notre | -3.9876022595481455 | AN |
| Gauche moderee | cessez | 3.935009649611856 | Twitter |
| Gauche moderee | millions | -3.922431120276941 | AN |
| Gauche moderee | israël | 3.88433156408852 | Twitter |
| Gauche moderee | feu | 3.788679953783 | Twitter |
| Gauche moderee | génocide | 3.744860445443164 | Twitter |
| Gauche moderee | des | -3.734516817258016 | AN |
| Gauche moderee | avez | -3.691359368062807 | AN |
| Gauche moderee | netanyahou | 3.5607585166521702 | Twitter |
| Gauche moderee | pays | -3.5398476532330982 | AN |
| ... | ... | ... | ... |
| Centre / Majorite | antisémitisme | -4.083937509508805 | AN |
| Centre / Majorite | supérieur | -4.068627723448564 | AN |
| Centre / Majorite | affaires | -4.049302698657418 | AN |
| Centre / Majorite | université | -3.8968086876926185 | AN |
| Centre / Majorite | été | -3.837936487079517 | AN |
| Centre / Majorite | enseignement | -3.835065852694931 | AN |
| Centre / Majorite | étrangères | -3.8031239587143975 | AN |
| Centre / Majorite | monsieur | -3.7784628424013023 | AN |
| Centre / Majorite | terroristes | 3.75620032891367 | Twitter |
| Centre / Majorite | victimes | 3.729482569963894 | Twitter |
| Centre / Majorite | madame | -3.708665999109694 | AN |
| Centre / Majorite | insoumise | -3.657292990690608 | AN |
| Centre / Majorite | a | -3.6521178599142905 | AN |
| Centre / Majorite | aujourd | 3.637440823128332 | Twitter |
| Centre / Majorite | hui | 3.637440823128332 | Twitter |
| Centre / Majorite | mme | -3.6105078047681034 | AN |
| Centre / Majorite | devons | -3.608539731527595 | AN |
| Centre / Majorite | ai | 3.601842435886094 | Twitter |
| Centre / Majorite | dans | -3.591237448115037 | AN |
| Droite | hamas | 9.447881627831304 | Twitter |
| Droite | vous | -8.486762028213857 | AN |
| Droite | que | -7.215580679543791 | AN |
| Droite | du | 5.362430908967289 | Twitter |
| Droite | nous | -5.213519892695623 | AN |
| Droite | terroristes | 5.112720479361997 | Twitter |
| Droite | otages | 5.062142420267565 | Twitter |
| Droite | elle | -4.687766672643245 | AN |
| Droite | terroriste | 4.673138260235673 | Twitter |
| Droite | lfi | 4.661273768779885 | Twitter |
| Droite | avez | -4.614246551468504 | AN |
| Droite | aux | 4.479450699843227 | Twitter |
| Droite | dans | -4.298914974595958 | AN |
| Droite | étudiants | -4.105476944048768 | AN |
| Droite | ou | -4.0718958996703485 | AN |
| Droite | soutien | 4.028537653772237 | Twitter |
| Droite | madame | -4.004007616589296 | AN |
| Droite | victimes | 3.9481036177106112 | Twitter |
| Droite | ministre | -3.925912896501802 | AN |
| Droite | votre | -3.817835419847712 | AN |
| Droite | terrorisme | 3.766874094836001 | Twitter |
| Droite | face | 3.7310626014409856 | Twitter |
| Droite | s | -3.724677609100581 | AN |
| Droite | familles | 3.6697888481963057 | Twitter |
| Droite | texte | -3.5851761908663398 | AN |
| Droite | loi | -3.572716157923321 | AN |
| Droite | palestine | 3.452247274972632 | Twitter |
| Droite | barbarie | 3.376163813266471 | Twitter |
| Droite | islamiste | 3.3284655472717697 | Twitter |
| Droite | m | -3.2960952216617136 | AN |

*(tronqué à 100 lignes — voir CSV pour données complètes)*


## Lag adoption

### lag_adoption.csv (4 lignes)

| bloc | month_first_10pct | pct |
| --- | --- | --- |
| Centre / Majorite | 2023-12 | 0.3 |
| Droite | 2024-12 | 0.1333333333333333 |
| Gauche moderee | 2023-10 | 0.2026143790849673 |
| Gauche radicale | 2023-10 | 0.2325581395348837 |


## A3 — Tendances pré-événement

### pre_event_mann_kendall.csv (8 lignes)

| event | bloc | tau | p_mk |
| --- | --- | --- | --- |
| Cessez-le-feu | Gauche radicale | 0.1015542211495185 | 0.3394049110948445 |
| Mandats CPI | Gauche radicale | -0.0761963241627708 | 0.4298873487022532 |
| Cessez-le-feu | Gauche moderee | -0.1283554891036813 | 0.4490173786823463 |
| Mandats CPI | Gauche moderee | 0.0176473641438893 | 0.9073814937715244 |
| Cessez-le-feu | Centre / Majorite | 0.055508374608144 | 0.7649901927589428 |
| Mandats CPI | Centre / Majorite | 0.0454061981136653 | 0.7181852269295643 |
| Cessez-le-feu | Droite | 0.1283863482263554 | 0.4330082123207993 |
| Mandats CPI | Droite | 0.1098558087671399 | 0.3460260472497075 |


## Autres CSV

### emotional_register_v4.csv (161 lignes)

| batch | bloc | emotional_register | n | total | pct |
| --- | --- | --- | --- | --- | --- |
| CEASEFIRE_BREACH | Centre / Majorite | defiance | 7 | 132 | 5.303030303030303 |
| CEASEFIRE_BREACH | Centre / Majorite | grief | 21 | 132 | 15.909090909090908 |
| CEASEFIRE_BREACH | Centre / Majorite | indignation | 44 | 132 | 33.33333333333333 |
| CEASEFIRE_BREACH | Centre / Majorite | neutral | 55 | 132 | 41.66666666666667 |
| CEASEFIRE_BREACH | Centre / Majorite | solidarity | 5 | 132 | 3.787878787878788 |
| CEASEFIRE_BREACH | Droite | anger | 3 | 117 | 2.564102564102564 |
| CEASEFIRE_BREACH | Droite | defiance | 32 | 117 | 27.350427350427356 |
| CEASEFIRE_BREACH | Droite | fear | 4 | 117 | 3.418803418803419 |
| CEASEFIRE_BREACH | Droite | grief | 13 | 117 | 11.11111111111111 |
| CEASEFIRE_BREACH | Droite | indignation | 46 | 117 | 39.31623931623932 |
| CEASEFIRE_BREACH | Droite | neutral | 18 | 117 | 15.384615384615383 |
| CEASEFIRE_BREACH | Droite | solidarity | 1 | 117 | 0.8547008547008548 |
| CEASEFIRE_BREACH | Gauche moderee | anger | 3 | 59 | 5.084745762711865 |
| CEASEFIRE_BREACH | Gauche moderee | fear | 1 | 59 | 1.694915254237288 |
| CEASEFIRE_BREACH | Gauche moderee | grief | 11 | 59 | 18.64406779661017 |
| CEASEFIRE_BREACH | Gauche moderee | indignation | 16 | 59 | 27.11864406779661 |
| CEASEFIRE_BREACH | Gauche moderee | neutral | 24 | 59 | 40.67796610169492 |
| CEASEFIRE_BREACH | Gauche moderee | solidarity | 4 | 59 | 6.779661016949152 |
| CEASEFIRE_BREACH | Gauche radicale | anger | 35 | 443 | 7.900677200902935 |
| CEASEFIRE_BREACH | Gauche radicale | defiance | 3 | 443 | 0.6772009029345373 |
| CEASEFIRE_BREACH | Gauche radicale | grief | 34 | 443 | 7.674943566591422 |
| CEASEFIRE_BREACH | Gauche radicale | indignation | 257 | 443 | 58.013544018058695 |
| CEASEFIRE_BREACH | Gauche radicale | neutral | 62 | 443 | 13.99548532731377 |
| CEASEFIRE_BREACH | Gauche radicale | solidarity | 52 | 443 | 11.738148984198643 |
| CHOC | Centre / Majorite | defiance | 45 | 287 | 15.6794425087108 |
| CHOC | Centre / Majorite | fear | 11 | 287 | 3.8327526132404177 |
| CHOC | Centre / Majorite | grief | 17 | 287 | 5.923344947735192 |
| CHOC | Centre / Majorite | indignation | 72 | 287 | 25.08710801393728 |
| CHOC | Centre / Majorite | neutral | 112 | 287 | 39.02439024390244 |
| CHOC | Centre / Majorite | solidarity | 30 | 287 | 10.452961672473869 |
| CHOC | Droite | anger | 4 | 352 | 1.1363636363636365 |
| CHOC | Droite | defiance | 177 | 352 | 50.28409090909091 |
| CHOC | Droite | fear | 9 | 352 | 2.556818181818182 |
| CHOC | Droite | grief | 4 | 352 | 1.1363636363636365 |
| CHOC | Droite | indignation | 117 | 352 | 33.23863636363637 |
| CHOC | Droite | neutral | 27 | 352 | 7.670454545454546 |
| CHOC | Droite | solidarity | 14 | 352 | 3.977272727272727 |
| CHOC | Gauche moderee | anger | 1 | 182 | 0.5494505494505495 |
| CHOC | Gauche moderee | defiance | 1 | 182 | 0.5494505494505495 |
| CHOC | Gauche moderee | fear | 2 | 182 | 1.098901098901099 |
| CHOC | Gauche moderee | grief | 44 | 182 | 24.17582417582417 |
| CHOC | Gauche moderee | indignation | 40 | 182 | 21.978021978021975 |
| CHOC | Gauche moderee | neutral | 63 | 182 | 34.61538461538461 |
| CHOC | Gauche moderee | solidarity | 31 | 182 | 17.032967032967033 |
| CHOC | Gauche radicale | anger | 11 | 789 | 1.394169835234474 |
| CHOC | Gauche radicale | defiance | 10 | 789 | 1.2674271229404308 |
| CHOC | Gauche radicale | fear | 4 | 789 | 0.5069708491761723 |
| CHOC | Gauche radicale | grief | 111 | 789 | 14.068441064638783 |
| CHOC | Gauche radicale | indignation | 401 | 789 | 50.82382762991128 |
| CHOC | Gauche radicale | neutral | 147 | 789 | 18.631178707224336 |
| ... | ... | ... | ... | ... | ... |
| POST_CIJ | Gauche moderee | indignation | 12 | 46 | 26.08695652173913 |
| POST_CIJ | Gauche moderee | neutral | 12 | 46 | 26.08695652173913 |
| POST_CIJ | Gauche moderee | solidarity | 12 | 46 | 26.08695652173913 |
| POST_CIJ | Gauche radicale | anger | 11 | 217 | 5.0691244239631335 |
| POST_CIJ | Gauche radicale | grief | 27 | 217 | 12.442396313364055 |
| POST_CIJ | Gauche radicale | indignation | 124 | 217 | 57.14285714285714 |
| POST_CIJ | Gauche radicale | neutral | 20 | 217 | 9.216589861751151 |
| POST_CIJ | Gauche radicale | solidarity | 35 | 217 | 16.129032258064516 |
| POST_SINWAR | Centre / Majorite | defiance | 7 | 33 | 21.21212121212121 |
| POST_SINWAR | Centre / Majorite | grief | 5 | 33 | 15.151515151515152 |
| POST_SINWAR | Centre / Majorite | indignation | 5 | 33 | 15.151515151515152 |
| POST_SINWAR | Centre / Majorite | neutral | 16 | 33 | 48.48484848484848 |
| POST_SINWAR | Droite | anger | 1 | 43 | 2.3255813953488373 |
| POST_SINWAR | Droite | defiance | 22 | 43 | 51.16279069767442 |
| POST_SINWAR | Droite | fear | 1 | 43 | 2.3255813953488373 |
| POST_SINWAR | Droite | grief | 1 | 43 | 2.3255813953488373 |
| POST_SINWAR | Droite | indignation | 9 | 43 | 20.930232558139537 |
| POST_SINWAR | Droite | neutral | 9 | 43 | 20.930232558139537 |
| POST_SINWAR | Gauche moderee | grief | 1 | 7 | 14.285714285714285 |
| POST_SINWAR | Gauche moderee | indignation | 3 | 7 | 42.85714285714285 |
| POST_SINWAR | Gauche moderee | neutral | 3 | 7 | 42.85714285714285 |
| POST_SINWAR | Gauche radicale | anger | 4 | 154 | 2.5974025974025974 |
| POST_SINWAR | Gauche radicale | grief | 21 | 154 | 13.636363636363637 |
| POST_SINWAR | Gauche radicale | indignation | 111 | 154 | 72.07792207792207 |
| POST_SINWAR | Gauche radicale | neutral | 10 | 154 | 6.493506493506493 |
| POST_SINWAR | Gauche radicale | solidarity | 8 | 154 | 5.194805194805195 |
| RAFAH | Centre / Majorite | anger | 1 | 130 | 0.7692307692307693 |
| RAFAH | Centre / Majorite | defense | 1 | 130 | 0.7692307692307693 |
| RAFAH | Centre / Majorite | defiance | 6 | 130 | 4.615384615384616 |
| RAFAH | Centre / Majorite | grief | 13 | 130 | 10.0 |
| RAFAH | Centre / Majorite | indignation | 37 | 130 | 28.46153846153846 |
| RAFAH | Centre / Majorite | neutral | 70 | 130 | 53.84615384615385 |
| RAFAH | Centre / Majorite | solidarity | 2 | 130 | 1.5384615384615383 |
| RAFAH | Droite | defiance | 27 | 71 | 38.0281690140845 |
| RAFAH | Droite | fear | 1 | 71 | 1.4084507042253522 |
| RAFAH | Droite | grief | 3 | 71 | 4.225352112676056 |
| RAFAH | Droite | indignation | 34 | 71 | 47.88732394366197 |
| RAFAH | Droite | neutral | 6 | 71 | 8.450704225352112 |
| RAFAH | Gauche moderee | anger | 2 | 106 | 1.8867924528301887 |
| RAFAH | Gauche moderee | grief | 7 | 106 | 6.60377358490566 |
| RAFAH | Gauche moderee | indignation | 62 | 106 | 58.490566037735846 |
| RAFAH | Gauche moderee | neutral | 22 | 106 | 20.75471698113208 |
| RAFAH | Gauche moderee | solidarity | 13 | 106 | 12.264150943396226 |
| RAFAH | Gauche radicale | anger | 21 | 670 | 3.134328358208955 |
| RAFAH | Gauche radicale | defiance | 6 | 670 | 0.8955223880597015 |
| RAFAH | Gauche radicale | grief | 10 | 670 | 1.4925373134328357 |
| RAFAH | Gauche radicale | indignation | 499 | 670 | 74.4776119402985 |
| RAFAH | Gauche radicale | neutral | 53 | 670 | 7.91044776119403 |
| RAFAH | Gauche radicale | solidarity | 81 | 670 | 12.08955223880597 |

*(tronqué à 100 lignes — voir CSV pour données complètes)*

