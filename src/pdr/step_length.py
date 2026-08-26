from __future__ import annotations
import numpy as np
import pandas as pd

def estimate_step_length(df: pd.DataFrame, sample_idx: int, mode: str, cfg: dict) -> float:
    fs = float(cfg["sampling_rate_hz"])
    scfg = cfg["step_length"]
    radius = max(1, int(float(scfg["neighborhood_s"])*fs))
    lo, hi = max(0,sample_idx-radius), min(len(df),sample_idx+radius+1)
    seg = df["acc_dyn"].iloc[lo:hi].to_numpy(float)
    amp = max(0.0, float(np.max(seg)-np.min(seg)))
    base = float(scfg["weinberg_k"]) * (amp**0.25 if amp > 0 else 0.0)
    scale = float(cfg["mode_parameters"].get(mode,cfg["mode_parameters"]["normal"])["step_scale"])
    return float(np.clip(base*scale, float(scfg["min_m"]), float(scfg["max_m"])))
