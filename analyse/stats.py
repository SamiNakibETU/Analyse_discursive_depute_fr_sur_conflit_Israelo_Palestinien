"""Tests et indicateurs utilisés par l'analyse secondaire."""
import numpy as np
import pandas as pd
from scipy import stats
from scipy.spatial.distance import jensenshannon


def heterogeneite(moyennes, erreurs_types):
    """Q de Cochran, I² et τ (DerSimonian-Laird) pour une série de moyennes indépendantes.

    Q teste si les moyennes varient plus que ne le prévoit l'erreur d'échantillonnage.
    τ estime l'écart-type « réel » de la série une fois ce bruit retiré.
    """
    m = np.asarray(moyennes, float)
    w = 1 / np.asarray(erreurs_types, float) ** 2
    moy = (w * m).sum() / w.sum()
    q = (w * (m - moy) ** 2).sum()
    ddl = len(m) - 1
    i2 = max(0.0, (q - ddl) / q) if q > 0 else 0.0
    tau2 = max(0.0, (q - ddl) / (w.sum() - (w ** 2).sum() / w.sum()))
    return {"moyenne": moy, "Q": q, "ddl": ddl, "p": stats.chi2.sf(q, ddl), "I2": i2, "tau": np.sqrt(tau2)}


def tendance_proportions(succes, effectifs):
    """Test de tendance de Cochran-Armitage sur des proportions ordonnées (scores 0..k-1)."""
    x = np.asarray(succes, float)
    n = np.asarray(effectifs, float)
    s = np.arange(len(x), dtype=float)
    p = x.sum() / n.sum()
    t = (s * (x - n * p)).sum()
    v = p * (1 - p) * ((s ** 2 * n).sum() - (s * n).sum() ** 2 / n.sum())
    if v <= 0:
        return {"z": np.nan, "p": np.nan}
    z = t / np.sqrt(v)
    return {"z": z, "p": 2 * stats.norm.sf(abs(z))}


def tendance_monotone(serie):
    """τ de Kendall entre le rang temporel et la valeur (équivalent du test de Mann-Kendall sans ex-aequo)."""
    y = pd.Series(serie).dropna().to_numpy()
    tau, p = stats.kendalltau(np.arange(len(y)), y)
    return {"tau": tau, "p": p, "n": len(y)}


def divergence_js(p, q):
    """Divergence de Jensen-Shannon en base 2 (0 = distributions identiques, 1 = disjointes)."""
    p = np.asarray(p, float)
    q = np.asarray(q, float)
    return float(jensenshannon(p / p.sum(), q / q.sum(), base=2) ** 2)


def gini(valeurs):
    x = np.sort(np.asarray(valeurs, float))
    n = len(x)
    return float((2 * (np.arange(1, n + 1) * x).sum()) / (n * x.sum()) - (n + 1) / n)


def comparer_proportions(a, n_a, b, n_b):
    """Test du khi² (2×2) entre deux proportions."""
    table = [[a, n_a - a], [b, n_b - b]]
    chi2, p, _, _ = stats.chi2_contingency(table)
    return {"p_a": a / n_a, "p_b": b / n_b, "chi2": chi2, "p": p}


def taux_poisson(compte, exposition, par=10_000):
    """Taux pour `par` unités avec intervalle exact de Poisson à 95 %."""
    bas = stats.chi2.ppf(0.025, 2 * compte) / 2 if compte > 0 else 0.0
    haut = stats.chi2.ppf(0.975, 2 * (compte + 1)) / 2
    return compte / exposition * par, bas / exposition * par, haut / exposition * par


def kappa_pondere(a, b, categories=(-2, -1, 0, 1, 2)):
    """Kappa de Cohen non pondéré et pondéré quadratique."""
    from sklearn.metrics import cohen_kappa_score
    return {
        "kappa": cohen_kappa_score(a, b, labels=list(categories)),
        "kappa_quadratique": cohen_kappa_score(a, b, labels=list(categories), weights="quadratic"),
    }
