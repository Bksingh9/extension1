"""HMM-based market regime detection.

A 5-state Gaussian HMM is fit on daily features of the primary symbol
(default SPY). After fitting, hidden states are sorted by mean return so
the lowest-return state maps to "CRASH" and the highest to "EUPHORIA".

The trained model is persisted to disk via joblib.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd

from .features import HMM_FEATURES, build_features, select_hmm_matrix
from .logging_setup import get_logger
from .settings import ROOT, config

log = get_logger()

REGIME_CFG = config["regime"]
LABELS = [REGIME_CFG["labels"][str(i)] for i in range(REGIME_CFG["n_components"])]


@dataclass
class RegimeAssessment:
    label: str
    confidence: float
    state_index: int
    distribution: dict[str, float]


@dataclass
class RegimeModel:
    hmm: object  # GaussianHMM
    scaler: object  # StandardScaler
    state_to_label: dict[int, str]  # sorted by mean return
    feature_columns: list[str]

    def predict_current(self, feats: pd.DataFrame) -> RegimeAssessment:
        if feats.empty:
            return RegimeAssessment(
                label=REGIME_CFG["default_label_on_low_confidence"],
                confidence=0.0,
                state_index=-1,
                distribution={},
            )
        x = self.scaler.transform(select_hmm_matrix(feats))
        proba = self.hmm.predict_proba(x)
        last = proba[-1]
        idx = int(np.argmax(last))
        confidence = float(last[idx])
        label = self.state_to_label[idx]

        # Time-in-regime distribution from posterior probabilities.
        avg = proba.mean(axis=0)
        dist = {self.state_to_label[i]: float(avg[i]) for i in range(len(avg))}
        return RegimeAssessment(label=label, confidence=confidence, state_index=idx, distribution=dist)

    def transition_matrix(self) -> pd.DataFrame:
        # Reorder rows/cols by sorted-state mapping.
        n = self.hmm.transmat_.shape[0]
        order = [k for k, _ in sorted(self.state_to_label.items(), key=lambda kv: LABELS.index(kv[1]))]
        labels_ordered = [self.state_to_label[i] for i in order]
        mat = self.hmm.transmat_[np.ix_(order, order)]
        return pd.DataFrame(mat, index=labels_ordered, columns=labels_ordered)


def fit(bars: pd.DataFrame) -> RegimeModel:
    """Fit a Gaussian HMM on bars of the primary regime symbol."""
    from hmmlearn.hmm import GaussianHMM
    from sklearn.preprocessing import StandardScaler

    feats = build_features(bars)
    if len(feats) < 80:
        raise ValueError(f"not enough bars to fit regime model (got {len(feats)})")

    cols = [c for c in HMM_FEATURES if c in feats.columns]
    raw = feats[cols].to_numpy(dtype=float)
    scaler = StandardScaler().fit(raw)
    x = scaler.transform(raw)

    hmm = GaussianHMM(
        n_components=REGIME_CFG["n_components"],
        covariance_type=REGIME_CFG["covariance_type"],
        n_iter=REGIME_CFG["n_iter"],
        tol=1e-4,
        random_state=42,
    )
    hmm.fit(x)

    states = hmm.predict(x)
    feats_with_state = feats.copy()
    feats_with_state["state"] = states

    # Sort states by mean return so 0 = CRASH, 4 = EUPHORIA.
    mean_ret_by_state = (
        feats_with_state.groupby("state")["ret"].mean().sort_values()
    )
    sorted_state_indices = list(mean_ret_by_state.index)
    state_to_label: dict[int, str] = {}
    for rank, state_idx in enumerate(sorted_state_indices):
        state_to_label[int(state_idx)] = LABELS[rank]

    log.info(f"regime fit: states sorted by mean ret -> {state_to_label}")
    return RegimeModel(hmm=hmm, scaler=scaler, state_to_label=state_to_label, feature_columns=cols)


def save(model: RegimeModel, path: Optional[Path] = None) -> Path:
    import joblib
    target = Path(path) if path else (ROOT / REGIME_CFG["model_path"])
    target.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(
        {
            "hmm": model.hmm,
            "scaler": model.scaler,
            "state_to_label": model.state_to_label,
            "feature_columns": model.feature_columns,
        },
        target,
    )
    log.info(f"regime model saved to {target}")
    return target


def load(path: Optional[Path] = None) -> Optional[RegimeModel]:
    import joblib
    target = Path(path) if path else (ROOT / REGIME_CFG["model_path"])
    if not target.exists():
        return None
    blob = joblib.load(target)
    return RegimeModel(
        hmm=blob["hmm"],
        scaler=blob["scaler"],
        state_to_label=blob["state_to_label"],
        feature_columns=blob["feature_columns"],
    )


def assess_with_default(bars: pd.DataFrame) -> RegimeAssessment:
    """Return a regime assessment, falling back to NEUTRAL if no model."""
    model = load()
    if model is None:
        return RegimeAssessment(
            label=REGIME_CFG["default_label_on_low_confidence"],
            confidence=0.0,
            state_index=-1,
            distribution={},
        )
    feats = build_features(bars)
    return model.predict_current(feats)
