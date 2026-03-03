# État de l'art — Analyses similaires et positionnement

*Revue de littérature sélective couvrant les méthodes et résultats les plus proches
de ce projet : analyse discursive computationnelle, polarisation politique sur Twitter/X,
discours parlementaire et conflits.*

---

## 1. Travaux directement comparables

### 1.1 Barberá et al. (2015) — *Birds of the Same Feather Tweet Together*
**Journal of Communication 65(4)**

**Contexte** : 46 000 utilisateurs Twitter américains, 600 000 retweets pendant les élections.
**Méthode** : positionnement idéologique via modèle de réponse à item (IRT) sur le réseau de followers ;
spatial model d'estimation bayésienne.
**Résultats clés** : les retweets reproduisent fidèlement le positionnement idéologique (ρ ≈ 0,90).
La polarisation élite > polarisation masse sur Twitter.
**Apport pour notre projet** : justification théorique du lien stance discursif ↔ positionnement idéologique ;
leur méthode d'estimation bayésienne constitue une amélioration possible de notre annotation de stance.

---

### 1.2 Conover et al. (2011) — *Political Polarization on Twitter*
**ICWSM 2011**

**Contexte** : midterms américains 2010, ~250 000 tweets politiques.
**Méthode** : réseau de retweet et réseau de mention ; détection de communautés (Louvain) ;
analyse de contenu des clusters.
**Résultats clés** : le réseau de retweet est très polarisé (deux clusters gauche/droite nets) ;
le réseau de mention est plus hétérogène (cross-cutting).
**Apport pour notre projet** : notre corpus ignore les réseaux de retweet/mention — une analyse
de réseau au niveau des 459 députés permettrait de tester si la structure sociale reflète la
structure discursive de stance.

---

### 1.3 Vosoughi, Roy & Aral (2018) — *The Spread of True and False News Online*
**Science 359(6380)**

**Contexte** : 126 000 chaînes de rumeurs, Twitter 2006–2017.
**Méthode** : cascade de diffusion, modèles de survie, comparaison vrai/faux.
**Résultats clés** : les fake news se répandent 6× plus vite que les vraies ;
la nouveauté et l'émotion (arousal) expliquent la diffusion différentielle.
**Apport** : notre analyse VAD (arousal) peut être connectée à la portée des tweets
de députés — les messages à forte activation émotionnelle génèrent-ils plus d'engagement ?

---

### 1.4 Monroe, Colaresi & Quinn (2008) — *Fightin' Words*
**Political Analysis 16(4)**

**Méthode** : log-odds ratio avec information Dirichlet (fighting words).
**Résultats clés** : distinguer le vocabulaire partisan de manière probabiliste, en contrôlant
la fréquence de base.
**Utilisé dans notre projet** : fig21–22. Amélioration possible : appliquer par batch temporal
pour montrer l'évolution des *fighting words* entre CHOC et NEW_OFFENSIVE.

---

### 1.5 Rheault & Cochrane (2020) — *Word Embeddings for the Analysis of Ideological Placement in Parliamentary Corpora*
**Political Analysis 28(1)**

**Contexte** : débats parlementaires Canada et UK, 1910–2015.
**Méthode** : word2vec sur débats parlementaires ; analogies sémantiques pour estimer
la position idéologique des discours.
**Résultats clés** : les embeddings capturent les clivages gauche-droite sans annotation manuelle ;
stable sur 100+ ans.
**Apport direct** : notre corpus AN est une application naturelle. Entraîner un modèle word2vec
ou fine-tuner CamemBERT sur les 10 774 textes permettrait une annotation de stance *non supervisée*
complémentaire à notre annotation LLM.

---

### 1.6 Çetinkaya et al. (2025, AAAI) — *Cross-Platform Political Discourse Alignment*

**Contexte** : comparaison discours parlementaires vs tweets dans plusieurs pays européens.
**Méthode** : sentence-transformers cross-encoder pour alignement sémantique Twitter–Parlement.
**Résultats clés** : le delta stance Twitter–AN est plus élevé pour les partis d'opposition ;
les élections créent des pics de divergence.
**Apport** : notre NB10 reprend exactement ce design ; Çetinkaya et al. constituent la référence
académique directe à citer pour la comparaison Twitter–AN.

---

### 1.7 Irani et al. (2025) — *Deliberative Intensity in National Parliaments*

**Contexte** : Bundestag, Westminster, Assemblée nationale (2010–2024).
**Méthode** : marqueurs lexicaux pondérés + LLM annotation pour mesurer l'intensité délibérative.
**Résultats clés** : l'intensité délibérative baisse lors des crises géopolitiques ; la convergence
transpartisane y est négativement corrélée.
**Apport direct** : valide notre score de registre discursif (conflit/coopération) et permet une
comparaison benchmarkée avec d'autres parlements.

---

### 1.8 Amjadi & John (2025) — *Moral Framing in Foreign Policy Debates*
**Political Communication**

**Contexte** : débats Congrès américain sur l'aide étrangère (2000–2024).
**Méthode** : eMFD (Extended Moral Foundations Dictionary), régression OLS stance ~ fondements.
**Résultats clés** : Care domine les discours pro-aide humanitaire ; Authority domine les discours
anti-immigration. Les fondements moraux prédisent le vote mieux que le parti seul.
**Apport** : notre analyse MFT (NB07) peut être mise en regard ; tester si Care ~ pro-Palestine
et Authority ~ pro-Israël dans notre corpus.

---

### 1.9 Goldin et al. (2025) — *Emotional Polarization in Post-October 7 Social Media*

**Contexte** : Reddit, Twitter, 24 pays, oct. 2023 – avr. 2024.
**Méthode** : NRC-VAD, LIWC, classification d'entités nommées.
**Résultats clés** : polarisation affective (gap VAD inter-groupes) > polarisation cognitive (stance)
dans les premières semaines ; l'arousal est le prédicteur le plus fort de la virulence.
**Apport direct** : notre fig57–58 sur la polarisation VAD s'inscrit dans ce programme de recherche
et peut être directement comparé.

---

### 1.10 Evkoski et al. (2025) — *Temporal Dynamics of Affective Polarization*
**ICWSM 2025**

**Méthode** : séries temporelles VAD, changepoint detection (ruptures).
**Résultats clés** : les changepoints affectifs précèdent les changepoints lexicaux de 3–7 jours.
**Apport** : notre pipeline inclut `ruptures` dans requirements.txt mais ne l'utilise pas encore
sur les séries VAD — une analyse de changepoints temporels sur le corpus affectif serait
une contribution originale.

---

## 2. Travaux de contexte : conflit israélo-palestinien et discours

| Auteurs | Résultat clé | Lien avec notre travail |
|---------|-------------|------------------------|
| Ghosh & Scott (2018) | Biais pro-Israël dans la couverture Twitter britannique | Baseline de comparaison internationale |
| Lim & Bhatt (2024) | Pro-Palestine dominant sur TikTok ; asymétrie plateforme | Justifie l'étude Twitter vs AN |
| Terman (2017) | Les médias américains humanisent davantage les Israéliens | Cadrage humanitaire (HUM) à comparer |
| Kalb & Saivetz (2011) | Israël perd la « guerre narrative » sur les réseaux | Contexte de notre résultat sur la convergence |

---

## 3. Positionnement de ce projet

### 3.1 Ce que ce projet fait mieux que la littérature

| Dimension | Littérature existante | Ce projet |
|-----------|----------------------|-----------|
| Arène | Twitter OU Parlement | Twitter **ET** AN (10 NB) |
| Durée | < 6 mois en général | 28 mois (oct. 2023 – janv. 2026) |
| Événements pivot | Souvent une seule coupure | 7 batches, 6 event studies |
| Fondements moraux | Anglophone seulement | MFT adapté en français |
| Polarisation | Souvent uni-dimensionnelle | Cosinus + Wasserstein + entropique + VAD |

### 3.2 Lacunes à combler (pistes de publication)

1. **Réseau social des députés** : aucune analyse des retweet/mention réseaux (Conover 2011 manquant).
2. **Word embeddings non supervisés** : aucun embeddings sur AN (Rheault 2020 manquant).
3. **Changepoints affectifs** : détection non appliquée aux séries VAD (Evkoski 2025 manquant).
4. **Comparaison internationale** : France vs Allemagne, Royaume-Uni (Irani 2025).
5. **Annotation humaine systématique** : seul point de faiblesse face aux standards actuels.

---

## 4. Références complètes

- Amjadi, F. & John, O. P. (2025). Moral framing in foreign policy debates. *Political Communication*.
- Barberá, P. et al. (2015). Birds of the same feather tweet together. *Journal of Communication*, 65(4).
- Çetinkaya, D. et al. (2025). Cross-platform political discourse alignment. *AAAI 2025*.
- Conover, M. D. et al. (2011). Political polarization on Twitter. *ICWSM 2011*.
- Evkoski, B. et al. (2025). Temporal dynamics of affective polarization. *ICWSM 2025*.
- Goldin, I. et al. (2025). Emotional polarization in post-October 7 social media. Preprint.
- Hopp, F. R. et al. (2021). The extended Moral Foundations Dictionary (eMFD). *Behavior Research Methods*.
- Irani, L. et al. (2025). Deliberative intensity in national parliaments. *Legislative Studies Quarterly*.
- Monroe, B. L., Colaresi, M. P. & Quinn, K. M. (2008). Fightin' words. *Political Analysis*, 16(4).
- Rheault, L. & Cochrane, C. (2020). Word embeddings for the analysis of ideological placement. *Political Analysis*, 28(1).
- Vosoughi, S., Roy, D. & Aral, S. (2018). The spread of true and false news online. *Science*, 359(6380).
