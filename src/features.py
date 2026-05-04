"""Feature engineering for the HMM regime model.

Inputs: a pandas.DataFrame of daily OHLCV bars with columns
  open, high, low, close, volume

Outputs:
  build_features(bars) -> pd.DataFrame with engineered features (NaN rows
    dropped). Columns:
      ret, log_ret, vol_20, vol_60, mean_ret_20,
      rsi_14, macd_hist, bb_width, vol_ratio, atr_14,
      mom_5, mom_20, mom_60, realized_vol_ann
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from .indicators import atr, bollinger, macd, rsi


HMM_FEATURES = ["ret", "log_ret", "vol_20", "vol_60", "vol_ratio"]


def build_features(bars: pd.DataFrame) -> pd.DataFrame:
    if bars is None or bars.empty:
        return pd.DataFrame()

    close = bars["close"].astype(float)
    high = bars["high"].astype(float)
    low = bars["low"].astype(float)
    volume = bars["volume"].astype(float)

    ret = close.pct_change()
    log_ret = np.log(close / close.shift(1))

    vol_20 = ret.rolling(20).std()
    vol_60 = ret.rolling(60).std()
    mean_ret_20 = ret.rolling(20).mean()

    r = rsi(close, 14)
    _, _, hist = macd(close)
    upper, mid, lower = bollinger(close, 20, 2.0)
    bb_width = (upper - lower) / mid

    avg_vol_20 = volume.rolling(20).mean()
    vol_ratio = volume / avg_vol_20

    a = atr(high, low, close, 14)

    mom_5 = close.pct_change(5)
    mom_20 = close.pct_change(20)
    mom_60 = close.pct_change(60)

    realized_vol_ann = ret.rolling(20).std() * np.sqrt(252)

    feats = pd.DataFrame(
        {
            "ret": ret,
            "log_ret": log_ret,
            "vol_20": vol_20,
            "vol_60": vol_60,
            "mean_ret_20": mean_ret_20,
            "rsi_14": r,
            "macd_hist": hist,
            "bb_width": bb_width,
            "vol_ratio": vol_ratio,
            "atr_14": a,
            "mom_5": mom_5,
            "mom_20": mom_20,
            "mom_60": mom_60,
            "realized_vol_ann": realized_vol_ann,
        }
    )
    return feats.dropna()


def select_hmm_matrix(feats: pd.DataFrame) -> np.ndarray:
    """Pick the columns the HMM trains on, return as numpy array."""
    cols = [c for c in HMM_FEATURES if c in feats.columns]
    if not cols:
        return np.empty((0, 0))
    return feats[cols].to_numpy(dtype=float)
