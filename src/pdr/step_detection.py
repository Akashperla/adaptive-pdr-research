from __future__ import annotations
import numpy as np
import pandas as pd
from scipy.signal import find_peaks

def detect_steps(df: pd.DataFrame, cfg: dict) -> pd.DataFrame:
    fs = float(cfg["sampling_rate_hz"])
    scfg = cfg["step_detection"]
    x = df["acc_dyn"].to_numpy(float)
    peaks, props = find_peaks(
        x,
        distance=max(1, int(float(scfg["min_step_interval_s"]) * fs)),
        prominence=float(scfg["prominence"]),
        height=float(np.median(x) + float(scfg["height_offset"])),
    )
    if len(peaks) == 0:
        return pd.DataFrame(columns=["sample_idx","timestamp","peak_value","prominence"])
    return pd.DataFrame({
        "sample_idx": peaks.astype(int),
        "timestamp": df["timestamp"].to_numpy()[peaks],
        "peak_value": x[peaks],
        "prominence": props.get("prominences", np.nan),
    })
