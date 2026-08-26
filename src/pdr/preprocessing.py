from __future__ import annotations
import numpy as np
import pandas as pd
from scipy.signal import butter, filtfilt
from .io import validate_imu_frame

def _safe_lowpass(x, fs, cutoff, order):
    x = np.asarray(x, dtype=float)
    if len(x) < max(20, order * 6):
        return x.copy()
    b, a = butter(order, min(cutoff/(0.5*fs), 0.99), btype="low")
    return filtfilt(b, a, x)

def preprocess_imu(df: pd.DataFrame, cfg: dict) -> pd.DataFrame:
    validate_imu_frame(df)
    out = df.copy()
    fs = float(cfg["sampling_rate_hz"])
    p = cfg["preprocessing"]
    order = int(p["filter_order"])
    for cols, cutoff in [
        (("ax","ay","az"), float(p["accel_lowpass_hz"])),
        (("gx","gy","gz"), float(p["gyro_lowpass_hz"])),
        (("mx","my","mz"), float(p["mag_lowpass_hz"]))]:
        for c in cols:
            out[f"{c}_f"] = _safe_lowpass(out[c].to_numpy(), fs, cutoff, order)
    out["acc_mag"] = np.sqrt(out.ax_f**2 + out.ay_f**2 + out.az_f**2)
    out["acc_dyn"] = out["acc_mag"] - float(np.median(out["acc_mag"]))
    return out
