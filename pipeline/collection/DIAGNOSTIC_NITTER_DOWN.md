# 🔴 DIAGNOSTIC - Instances Nitter Indisponibles

**Date**: 20 octobre 2025, 19:00 UTC
**Problème**: Timeouts massifs lors du scraping
**Impact**: Scraping bloqué après 2-3 députés

---

## 🧪 TESTS INSTANCES NITTER

### nitter.net (Instance principale utilisée)
```bash
curl -I --max-time 10 "https://nitter.net"
```
**Résultat**: ❌ **TIMEOUT après 10 secondes**
**Status**: DOWN / Très lent
**Erreur script**: `net::ERR_CONNECTION_TIMED_OUT`

### nitter.cz
```bash
curl -I --max-time 10 "https://nitter.cz"
```
**Résultat**: ⚠️ **HTTP 302 Redirect** (répond mais redirige)
**Status**: Partiellement fonctionnel
**Test page profil**: 0 timeline-item trouvés (possiblement redirection vers page erreur)

### xcancel.com
```bash
curl -I --max-time 10 "https://xcancel.com"
```
**Résultat**: ❌ **HTTP 403 Forbidden**
**Status**: Bloqué / Cloudflare protection

### nitter.privacydev.net
```bash
curl -I --max-time 10 "https://nitter.privacydev.net"
```
**Résultat**: ❌ **Could not resolve host**
**Status**: DOWN / DNS ne résout pas

### nitter.poast.org
```bash
curl -I --max-time 10 "https://nitter.poast.org"
```
**Résultat**: ❌ **HTTP 403 Forbidden**
**Status**: Bloqué

---

## 📊 IMPACT SUR LE SCRAPING

### Données Collectées Avant Panne
- **Députés scrapés avec succès**: 3/378
  1. @mathildepanot - 1,475 tweets (21 mois)
  2. @abomangoli - 1,989 tweets (23 mois)
  3. @laualexandre12 - 124 tweets (7 mois partiels)

- **Total tweets collectés**: ~3,600 tweets
- **Fichiers mensuels générés**: 51 fichiers

### Erreurs Observées
```
⚠️  Erreur (tentative 1/3): Navigation timeout of 30000 ms exceeded
⚠️  Erreur (tentative 2/3): net::ERR_CONNECTION_TIMED_OUT at https://nitter.net/search?f=tweets&q=...
⏳ Attente 5s avant retry...
⏳ Attente 10s avant retry...
❌ Échec après 3 tentatives
```

**Pattern**:
- Timeouts systématiques sur nitter.net
- 3 tentatives de retry (5s, 10s, 20s backoff)
- Toutes les tentatives échouent

---

## 🔍 CAUSE RACINE

### Hypothèses

**1. Surcharge de nitter.net** ⭐ (Plus probable)
- Instance populaire probablement surchargée
- Trop de requêtes simultanées d'autres utilisateurs
- Rate limiting côté serveur

**2. Maintenance / Panne**
- Instance down pour maintenance
- Problèmes serveur temporaires

**3. Blocage géographique / IP**
- IP bloquée après trop de requêtes
- Rate limit atteint (même avec délais de 3s)

**4. Changement infrastructure Nitter**
- Nitter.net a peut-être fermé / migré
- Plusieurs instances mortes suggèrent problème général Nitter

### Vérification Statut Nitter Général

URL à vérifier: https://status.d420.de/ (Nitter status page)
Ou: https://github.com/zedeus/nitter/wiki/Instances

**Note**: Beaucoup d'instances Nitter publiques ont fermé en 2024-2025 suite aux changements API Twitter.

---

## 💡 SOLUTIONS POSSIBLES

### Solution 1: Attendre Retour Service ⏰
**Action**: Attendre quelques heures/jours que nitter.net revienne
**Avantages**:
- ✅ Aucun changement code nécessaire
- ✅ Données déjà scrapées préservées
**Inconvénients**:
- ❌ Délai indéterminé
- ❌ Risque que l'instance soit définitivement down

**Implémentation**:
```bash
# Relancer le même script dans quelques heures
node scripts/scrape_nitter_search_monthly.js --input data/interim/extracted_accounts.json
```

---

### Solution 2: Trouver Instances Nitter Alternatives ✅ (RECOMMANDÉ)
**Action**: Identifier instances Nitter fonctionnelles et modifier script

**Étapes**:
1. Consulter liste instances: https://github.com/zedeus/nitter/wiki/Instances
2. Tester manuellement 5-10 instances
3. Garder 2-3 instances fonctionnelles
4. Modifier `CONFIG.nitterUrl` dans script
5. Ajouter rotation automatique entre instances

**Instances potentielles à tester**:
```bash
# À tester manuellement
curl -I "https://nitter.it"
curl -I "https://nitter.pussthecat.org"
curl -I "https://nitter.fdn.fr"
curl -I "https://nitter.kavin.rocks"
curl -I "https://nitter.unixfox.eu"
curl -I "https://nitter.moomoo.me"
```

**Modification script**:
```javascript
const CONFIG = {
  nitterInstances: [
    'https://nitter.it',
    'https://nitter.fdn.fr',
    'https://nitter.kavin.rocks'
  ],
  currentInstance: 0
};

// Rotation automatique sur erreur
function getNextInstance() {
  CONFIG.currentInstance = (CONFIG.currentInstance + 1) % CONFIG.nitterInstances.length;
  return CONFIG.nitterInstances[CONFIG.currentInstance];
}
```

---

### Solution 3: Twitter API Officielle 💰
**Action**: Basculer sur Twitter API v2

**Plans disponibles**:
- **Free** : 500k tweets/mois, 7 jours historique ❌ (insuffisant)
- **Basic** : $100/mois, 10k tweets/mois, historique complet ❌ (trop cher pour volume)
- **Pro** : $5,000/mois ❌ (trop cher)
- **Academic Research** : GRATUIT, 10M tweets/mois, historique complet ✅

**Recommandation**: Demander Academic Research Access
- URL: https://developer.twitter.com/en/products/twitter-api/academic-research
- Justification: Recherche politique/académique sur discours députés
- Délai approbation: 2-4 semaines
- Avantage: Données officielles, fiables, aucune limite

---

### Solution 4: Alternative - Utiliser Données Existantes ♻️
**Action**: Exploiter les 3,600 tweets déjà collectés

**Données disponibles**:
- 3 députés complets (dont Mathilde Panot)
- 3,600 tweets sur période 2023-2025
- 51 fichiers mensuels déjà sauvegardés

**Analyses possibles MAINTENANT**:
1. Étude de cas approfondie Mathilde Panot (1,475 tweets)
2. Évolution discours 2023 vs 2024 vs 2025
3. Analyse tweets Gaza/Palestine (155 tweets identifiés)
4. Prototype méthodologie pour future collecte large

**Commande consolidation**:
```bash
node scripts/consolidate_monthly_data.js
node scripts/analyze_gaza_tweets.js
```

---

## 🚀 PLAN D'ACTION RECOMMANDÉ

### Phase 1: Test Instances Alternatives (30 min)
1. Tester manuellement 10 instances Nitter de la liste GitHub
2. Identifier 2-3 instances fonctionnelles
3. Vérifier qu'elles supportent `/search?f=tweets&q=...`

### Phase 2: Modifier Script (15 min)
1. Ajouter rotation automatique instances
2. Augmenter timeout (30s → 60s)
3. Ajouter plus de délai entre requêtes (3s → 5s)

### Phase 3: Test Reprise (10 min)
1. Tester script modifié sur 1 député
2. Vérifier que skip fichiers existants fonctionne
3. Confirmer collecte reprend où elle s'était arrêtée

### Phase 4: Relance Scraping Complet
1. Lancer script en background
2. Monitoring toutes les heures
3. Objectif: 378 députés × 34 mois

### Phase 5 (Parallèle): Demande Twitter API Academic
1. Remplir formulaire Academic Research Access
2. Backup plan si Nitter définitivement HS
3. Délai: 2-4 semaines

---

## 📝 COMMANDES UTILES

### Vérifier Progression Actuelle
```bash
cd "D:\Users\Proprietaire\Desktop\Projets\Revirement_politique_fr_gaza\FINAL"
node scripts/monitor_progress.js
```

### Consolider Données Existantes
```bash
node scripts/consolidate_monthly_data.js
node scripts/analyze_gaza_tweets.js
```

### Tester Nouvelle Instance
```bash
# Modifier CONFIG.nitterUrl dans scripts/scrape_nitter_search_monthly.js
# Puis tester sur 1 député
node scripts/scrape_nitter_search_monthly.js --input data/interim/test_deputes.json --test --months 3
```

---

## ✅ CONCLUSION

**Problème**: Toutes les instances Nitter testées sont DOWN ou bloquées
**Impact**: Scraping interrompu après 3/378 députés
**Données sauvées**: 3,600 tweets préservés dans data/interim/twitter_monthly/

**Action immédiate**:
1. Tester instances Nitter alternatives
2. Modifier script avec rotation instances
3. Relancer scraping

**Backup plan**: Demander Twitter API Academic Research Access (gratuit, 2-4 semaines)

**Données exploitables dès maintenant**:
- Mathilde Panot: 1,475 tweets analysables
- 155 tweets Gaza/Palestine identifiés
- Étude de cas possible pendant résolution problème Nitter
