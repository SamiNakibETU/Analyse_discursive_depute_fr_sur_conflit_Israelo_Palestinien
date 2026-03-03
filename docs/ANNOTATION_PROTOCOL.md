# Protocole d'annotation — Stance et cadres

*Ce fichier documente le protocole LLM utilisé pour produire `stance_v3` et `stance_v4`.
Il doit être complété avec les informations exactes sur le modèle utilisé.*

---

## ⚠️ À compléter par l'auteur

Les champs marqués **[À RENSEIGNER]** doivent être remplis avant toute soumission
ou partage public du projet.

---

## 1. Modèle d'annotation

| Paramètre | Valeur |
|-----------|--------|
| Fournisseur | **[À RENSEIGNER]** (ex. OpenAI, Mistral AI, Anthropic) |
| Modèle et version | **[À RENSEIGNER]** (ex. gpt-4-turbo-2024-04-09) |
| Date d'annotation v3 | **[À RENSEIGNER]** |
| Date d'annotation v4 | **[À RENSEIGNER]** |
| Température | **[À RENSEIGNER]** (ex. 0.0 pour reproductibilité) |
| Langue du prompt | Français |

---

## 2. Prompt v3 (corpus complet)

```
[À RENSEIGNER — Coller le prompt exact utilisé pour l'annotation v3]

Exemple de structure minimale :
"Lis le texte suivant d'un député français sur le conflit israélo-palestinien.
Attribue un score de stance sur l'échelle suivante :
-2 : très favorable à Israël / défense israélienne
-1 : plutôt favorable à Israël
 0 : neutre / ambigu / équilibré
+1 : plutôt favorable à la Palestine / cessez-le-feu
+2 : très favorable à la Palestine

Réponds uniquement par le score numérique.

Texte : {text}"
```

---

## 3. Prompt v4 (corpus événementiel — enrichi)

```
[À RENSEIGNER — Coller le prompt exact utilisé pour l'annotation v4,
incluant le contexte temporel et les événements pivot]
```

**Différences v4 vs v3** :
- Contexte temporel ajouté (date, événement pivot de la fenêtre)
- Variables additionnelles annotées : `genocide_framing`, `condemns_hamas_attack`,
  `state_recognition_mention`, `transpartisan_convergence`

---

## 4. Décisions de codage pour les cas ambigus

| Cas | Décision |
|-----|----------|
| Texte équilibré mentionnant les deux parties | Score 0 |
| Texte appelant au cessez-le-feu sans prendre parti | Score +1 par défaut |
| Texte condamnant Hamas ET demandant cessez-le-feu | Score 0 à +1 selon le poids relatif |
| Texte principalement factuel (vote, annonce) | Score 0 |
| Texte trop court (< 20 mots) | **[À RENSEIGNER]** |
| Retweet sans commentaire | **[À RENSEIGNER]** |

---

## 5. Biais documentés des LLM sur ce sujet

**Note importante** : plusieurs études montrent que les LLM présentent des biais
sur le conflit israélo-palestinien (Navigli et al. 2023, *Biases in Large Language Models*).

Actions recommandées :
1. Tester le biais du modèle sur un échantillon de textes extrêmes (± 2 attendus).
2. Comparer les scores LLM aux scores humains sur les 150 textes de validation.
3. Déclarer explicitement dans toute publication que l'annotation est LLM-assistée.

---

## 6. Reproductibilité

Pour ré-annoter avec exactement les mêmes paramètres :
```
[À RENSEIGNER — Script ou notebook d'annotation]
```

**Avertissement** : même avec température=0, les résultats peuvent varier selon
les versions d'API. Archiver les résultats d'annotation originaux.

---

## Références

- Navigli, R. et al. (2023). Biases in Large Language Models: Origins, Inventory and Discussion.
  *ACM Journal of Data and Information Quality*.
- Çetinkaya, D. et al. (2025). Cross-platform political discourse alignment. *AAAI 2025*.
