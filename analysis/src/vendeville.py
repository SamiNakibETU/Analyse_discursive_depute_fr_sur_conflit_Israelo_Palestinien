# -*- coding: utf-8 -*-
"""
Métriques de polarisation et convergence (Bao & Gill, Wasserstein, effective dimensionality).
arXiv:2603.02102 — Méthodes adaptées au corpus députés français.
"""

import numpy as np
import pandas as pd
from scipy.stats import wasserstein_distance

WD_MAX = 4.0  # Échelle stance -2 à +2


def binary_entropy_normalized(p):
    """H(p, 1-p) = 2^(-p·log₂(p)-(1-p)·log₂(1-p)) - 1. Retourne 0 si p=0 ou p=1."""
    if p <= 0 or p >= 1:
        return 0.0
    return 2 ** (-p * np.log2(p) - (1 - p) * np.log2(1 - p)) - 1


def entropic_polarization_bao_gill(values, k=5, val_range=(-2, 2)):
    """
    Polarisation entropique Bao & Gill (2024).
    Ec = [H(S₁,1-S₁) + ... + H(Sₖ₋₁,1-Sₖ₋₁)] / (k-1)
    Retourne 0 (consensus) à 1 (polarisation max).
    """
    values = np.asarray(values)
    values = values[np.isfinite(values)]
    if len(values) < 2:
        return np.nan
    bins = np.linspace(val_range[0] - 0.5, val_range[1] + 0.5, k + 1)
    counts, _ = np.histogram(values, bins=bins)
    if counts.sum() == 0:
        return np.nan
    probs = counts / counts.sum()
    S = np.cumsum(probs)
    total = sum(binary_entropy_normalized(float(S[j])) for j in range(k - 1))
    return total / (k - 1)


def wd_inter_blocs(df, pairs, stance_col="stance_v3", month_col="month"):
    """
    Distance de Wasserstein normalisée entre paires de blocs, par mois.
    Retourne DataFrame avec month, pair, wd_norm.
    """
    months = sorted(df[month_col].dropna().unique())
    rows = []
    for m in months:
        sub = df[df[month_col] == m]
        for b1, b2 in pairs:
            v1 = sub[sub["bloc"] == b1][stance_col].dropna()
            v2 = sub[sub["bloc"] == b2][stance_col].dropna()
            if len(v1) >= 5 and len(v2) >= 5:
                wd = wasserstein_distance(v1, v2) / WD_MAX
                rows.append({"month": m, "pair": f"{b1} vs {b2}", "wd_norm": wd})
    return pd.DataFrame(rows)


def wd_drift_intra_bloc(df, bloc, ref_month="2023-10", stance_col="stance_v3", month_col="month"):
    """
    Drift intra-bloc : WD entre la distribution du bloc à ref_month et chaque mois.
    Retourne DataFrame avec month, wd_norm.
    """
    ref = df[(df["bloc"] == bloc) & (df[month_col] == ref_month)][stance_col].dropna()
    if len(ref) < 5:
        return pd.DataFrame()
    months = sorted(df[month_col].dropna().unique())
    rows = []
    for m in months:
        curr = df[(df["bloc"] == bloc) & (df[month_col] == m)][stance_col].dropna()
        if len(curr) >= 5:
            wd = wasserstein_distance(ref, curr) / WD_MAX
            rows.append({"month": m, "bloc": bloc, "wd_norm": wd})
    return pd.DataFrame(rows)


def effective_dimensionality(X):
    """
    ED = exp(sum(-λₘ/M * log(λₘ/M))) à partir de la matrice de corrélation.
    X : array 2D (n_samples, n_features). Retourne un scalaire.
    """
    X = np.asarray(X, dtype=float)
    X = X[np.isfinite(X).all(axis=1)]
    if X.shape[0] < 5 or X.shape[1] < 2:
        return np.nan
    corr = np.corrcoef(X.T)
    if np.any(~np.isfinite(corr)):
        return np.nan
    eigenvalues = np.linalg.eigvalsh(corr)
    eigenvalues = np.maximum(eigenvalues, 0)
    M = eigenvalues.sum()
    if M <= 0:
        return np.nan
    probs = eigenvalues / M
    probs = probs[probs > 1e-10]
    ent = -np.sum(probs * np.log(probs))
    return np.exp(ent)
