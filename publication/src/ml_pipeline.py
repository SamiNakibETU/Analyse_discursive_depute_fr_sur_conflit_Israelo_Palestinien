# -*- coding: utf-8 -*-
"""
Pipeline ML : embeddings, classification stance, validation croisée.
Exploite corpus_v3 pour fine-tuner un modèle ou entraîner un classifieur sur embeddings.

Modes :
  1. embeddings + LogisticRegression (léger, CPU)
  2. fine-tuning CamemBERT (GPU recommandé)
  3. validation croisée : corrélation LLM vs ML

Usage :
    python src/ml_pipeline.py --mode embeddings   # ~5 min CPU
    python src/ml_pipeline.py --mode finetune      # ~30 min GPU
    python src/ml_pipeline.py --mode validate      # compare LLM vs embeddings
"""

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, classification_report, confusion_matrix

sys.path.insert(0, str(Path(__file__).resolve().parent))
from config import CORPUS_V3, RESULTS_DIR, PROCESSED_DIR

RESULTS_DIR.mkdir(parents=True, exist_ok=True)
MODELS_DIR = PROCESSED_DIR.parent / "models"
MODELS_DIR.mkdir(parents=True, exist_ok=True)

STANCE_LABELS = {-2: 0, -1: 1, 0: 2, 1: 3, 2: 4}
INV_STANCE = {v: k for k, v in STANCE_LABELS.items()}


def load_corpus(min_confidence: float = 0.0) -> pd.DataFrame:
    """Charge corpus_v3 et filtre par confiance."""
    if not CORPUS_V3.exists():
        raise FileNotFoundError(f"Corpus absent : {CORPUS_V3}")
    df = pd.read_parquet(CORPUS_V3)
    df = df[df["text_clean"].notna() & (df["text_clean"].str.len() >= 20)].copy()
    df = df[df["stance_v3"].notna()]
    df["stance_v3"] = df["stance_v3"].round().astype(int)
    df = df[df["stance_v3"].between(-2, 2)]
    if "confidence_v3" in df.columns and min_confidence > 0:
        df = df[df["confidence_v3"] >= min_confidence]
    df["stance_label"] = df["stance_v3"].map(STANCE_LABELS)
    return df


def run_embeddings_mode(df: pd.DataFrame, n_splits: int = 5) -> dict:
    """
    Mode embeddings : sentence-transformers + LogisticRegression.
    Léger, exécutable sur CPU.
    """
    try:
        from sentence_transformers import SentenceTransformer
    except ImportError:
        print("Installer : pip install sentence-transformers")
        return {}

    texts = df["text_clean"].fillna("").astype(str).tolist()
    y = df["stance_label"].values

    print("Chargement modèle sentence-transformers (paraphrase-multilingual-MiniLM)...")
    model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
    X = model.encode(texts, show_progress_bar=True)

    print("Validation croisée 5-fold (LogisticRegression)...")
    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)
    clf = LogisticRegression(max_iter=1000, class_weight="balanced", random_state=42)
    y_pred = cross_val_predict(clf, X, y, cv=skf)

    acc = accuracy_score(y, y_pred)
    f1_macro = f1_score(y, y_pred, average="macro")
    print(f"\nRésultats : Accuracy={acc:.3f}, F1-macro={f1_macro:.3f}")
    print(classification_report(y, y_pred, target_names=[str(INV_STANCE[i]) for i in range(5)]))
    print("\nMatrice de confusion (labels -2 à +2) :")
    print(confusion_matrix(y, y_pred))

    # Corrélation prédit vs LLM (stance continu)
    y_pred_stance = np.array([INV_STANCE[int(i)] for i in y_pred])
    corr = np.corrcoef(df["stance_v3"], y_pred_stance)[0, 1]
    print(f"\nCorrélation prédictions ML vs LLM : ρ = {corr:.3f}")

    out = {
        "accuracy": acc,
        "f1_macro": f1_macro,
        "correlation_llm": corr,
        "confusion_matrix": confusion_matrix(y, y_pred),
    }
    pd.DataFrame([out]).to_csv(RESULTS_DIR / "ml_embeddings_metrics.csv", index=False)
    return out


def run_finetune_mode(df: pd.DataFrame, epochs: int = 3, batch_size: int = 16) -> dict:
    """
    Fine-tuning CamemBERT pour classification stance.
    Nécessite torch et transformers. GPU recommandé.
    """
    try:
        import torch
        from transformers import CamembertForSequenceClassification, CamembertTokenizer
        from torch.utils.data import Dataset
        from transformers import Trainer, TrainingArguments
    except ImportError as e:
        print(f"Fine-tuning nécessite torch et transformers : {e}")
        return {}

    texts = df["text_clean"].fillna("").astype(str).tolist()
    y = df["stance_label"].values
    n_classes = 5

    # Train/val split
    from sklearn.model_selection import train_test_split
    X_train, X_val, y_train, y_val = train_test_split(
        texts, y, test_size=0.15, stratify=y, random_state=42
    )

    model_name = "camembert-base"
    tokenizer = CamembertTokenizer.from_pretrained(model_name)
    model = CamembertForSequenceClassification.from_pretrained(model_name, num_labels=n_classes)

    class StanceDataset(Dataset):
        def __init__(self, texts, labels, tokenizer, max_len=256):
            self.texts = texts
            self.labels = labels
            self.tokenizer = tokenizer
            self.max_len = max_len

        def __len__(self):
            return len(self.texts)

        def __getitem__(self, i):
            enc = self.tokenizer(
                self.texts[i],
                padding="max_length",
                max_length=self.max_len,
                truncation=True,
                return_tensors="pt",
            )
            return {
                "input_ids": enc["input_ids"].squeeze(0),
                "attention_mask": enc["attention_mask"].squeeze(0),
                "labels": torch.tensor(self.labels[i], dtype=torch.long),
            }

    train_ds = StanceDataset(X_train, y_train, tokenizer)
    val_ds = StanceDataset(X_val, y_val, tokenizer)

    args = TrainingArguments(
        output_dir=str(MODELS_DIR / "camembert_stance"),
        num_train_epochs=epochs,
        per_device_train_batch_size=batch_size,
        per_device_eval_batch_size=32,
        learning_rate=2e-5,
        eval_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        metric_for_best_model="f1",
        greater_is_better=True,
    )

    def compute_metrics(eval_pred):
        preds, labels = eval_pred
        preds = np.argmax(preds, axis=1)
        return {"accuracy": float(accuracy_score(labels, preds)), "f1": float(f1_score(labels, preds, average="macro"))}

    trainer = Trainer(
        model=model,
        args=args,
        train_dataset=train_ds,
        eval_dataset=val_ds,
        compute_metrics=compute_metrics,
    )
    trainer.train()
    metrics = trainer.evaluate()
    print(f"\nFine-tuning terminé. Metrics : {metrics}")

    model.save_pretrained(MODELS_DIR / "camembert_stance")
    tokenizer.save_pretrained(MODELS_DIR / "camembert_stance")

    out = {"accuracy": metrics.get("eval_accuracy", 0), "f1": metrics.get("eval_f1", 0)}
    pd.DataFrame([out]).to_csv(RESULTS_DIR / "ml_finetune_metrics.csv", index=False)
    return out


def run_validate_mode(df: pd.DataFrame) -> dict:
    """
    Compare prédictions embeddings vs LLM, par bloc et par arena.
    Produit un rapport de cohérence.
    """
    try:
        from sentence_transformers import SentenceTransformer
    except ImportError:
        print("Installer : pip install sentence-transformers")
        return {}

    texts = df["text_clean"].fillna("").astype(str).tolist()
    model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
    X = model.encode(texts, show_progress_bar=True)

    clf = LogisticRegression(max_iter=1000, class_weight="balanced", random_state=42)
    clf.fit(X, df["stance_label"])

    pred_labels = clf.predict(X)
    pred_stance = np.array([INV_STANCE[int(i)] for i in pred_labels])

    df = df.copy()
    df["stance_ml"] = pred_stance
    df["delta_llm_ml"] = df["stance_v3"] - df["stance_ml"]

    # Corrélation par bloc
    corr_bloc = df.groupby("bloc").apply(
        lambda g: np.corrcoef(g["stance_v3"], g["stance_ml"])[0, 1] if len(g) > 10 else np.nan
    )
    corr_arena = df.groupby("arena").apply(
        lambda g: np.corrcoef(g["stance_v3"], g["stance_ml"])[0, 1] if len(g) > 10 else np.nan
    )

    report = pd.DataFrame([
        {"dimension": "bloc", "level": k, "correlation_llm_ml": v}
        for k, v in corr_bloc.items()
    ] + [
        {"dimension": "arena", "level": str(k), "correlation_llm_ml": v}
        for k, v in corr_arena.items()
    ])
    report.to_csv(RESULTS_DIR / "ml_validation_par_bloc_arena.csv", index=False)
    print(report)
    return {"corr_bloc": dict(corr_bloc), "corr_arena": dict(corr_arena)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["embeddings", "finetune", "validate"], default="embeddings")
    parser.add_argument("--min-confidence", type=float, default=0.70)
    parser.add_argument("--epochs", type=int, default=3)
    args = parser.parse_args()

    print(f"Chargement corpus (min_confidence={args.min_confidence})...")
    df = load_corpus(min_confidence=args.min_confidence)
    print(f"  {len(df):,} textes, stance -2 à +2")

    if args.mode == "embeddings":
        run_embeddings_mode(df)
    elif args.mode == "finetune":
        run_finetune_mode(df, epochs=args.epochs)
    elif args.mode == "validate":
        run_validate_mode(df)

    print("\nPipeline ML terminé.")


if __name__ == "__main__":
    main()
