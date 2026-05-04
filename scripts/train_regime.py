"""Train the HMM regime model on historical bars of the primary symbol.

Usage:
    python3 scripts/train_regime.py
    python3 scripts/train_regime.py --symbol QQQ --days 504

Reads bars via yfinance (no broker needed), fits the HMM, prints a
regime distribution + transition matrix, and saves the model to
`models/regime.joblib`.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import pandas as pd  # noqa: E402

from src.features import build_features  # noqa: E402
from src.regime import fit, save  # noqa: E402
from src.settings import config  # noqa: E402


def _bars(symbol: str, days: int) -> pd.DataFrame:
    import yfinance as yf
    df = yf.download(symbol, period=f"{days+50}d", interval="1d", progress=False, auto_adjust=False)
    if df is None or df.empty:
        return pd.DataFrame()
    df.columns = [c.lower() if isinstance(c, str) else c[0].lower() for c in df.columns]
    return df.tail(days)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--symbol", default=config["regime"]["primary_symbol"])
    p.add_argument("--days", type=int, default=config["regime"]["lookback_days"])
    args = p.parse_args()

    print(f"Fetching {args.days} days of {args.symbol}...")
    bars = _bars(args.symbol, args.days)
    if bars.empty:
        print("ERROR: no bars fetched. Check network / yfinance.")
        return 1

    print(f"Fitting HMM on {len(bars)} bars...")
    model = fit(bars)
    save(model)

    feats = build_features(bars)
    assessment = model.predict_current(feats)
    print(f"\nCurrent regime: {assessment.label} (confidence {assessment.confidence:.2f})")
    print("\nRegime distribution (avg posterior over training window):")
    for k, v in sorted(assessment.distribution.items()):
        print(f"  {k:10s} {v*100:5.1f}%")
    print("\nTransition matrix:")
    print(model.transition_matrix().round(3).to_string())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
