from __future__ import annotations
import numpy as np
import pandas as pd

CHANNELS = ["ax_f","ay_f","az_f","gx_f","gy_f","gz_f","mx_f","my_f","mz_f","acc_dyn"]

def _stats(x, prefix):
    x = np.asarray(x,float)
    return {f"{prefix}_{k}":v for k,v in {
        "mean":float(np.mean(x)),"std":float(np.std(x)),"min":float(np.min(x)),
        "max":float(np.max(x)),"rms":float(np.sqrt(np.mean(x**2))),
        "energy":float(np.mean(x**2)),"ptp":float(np.ptp(x))}.items()}

def window_features(df: pd.DataFrame, cfg: dict) -> pd.DataFrame:
    fs=float(cfg["sampling_rate_hz"]); win=max(5,int(float(cfg["features"]["window_s"])*fs)); hop=max(1,int(float(cfg["features"]["hop_s"])*fs))
    rows=[]
    for start in range(0,max(1,len(df)-win+1),hop):
        end=start+win
        if end>len(df): break
        w=df.iloc[start:end]
        row={"start_idx":start,"end_idx":end-1,"center_idx":start+win//2,"timestamp":float(w.timestamp.iloc[win//2])}
        for c in CHANNELS: row.update(_stats(w[c].to_numpy(),c))
        row["acc_sma"]=float(np.mean(np.abs(w.ax_f))+np.mean(np.abs(w.ay_f))+np.mean(np.abs(w.az_f)))
        row["gyro_mag_mean"]=float(np.mean(np.sqrt(w.gx_f**2+w.gy_f**2+w.gz_f**2)))
        if "label" in w.columns:
            m=w.label.mode(dropna=True); row["label"]=m.iloc[0] if len(m) else "normal"
        rows.append(row)
    return pd.DataFrame(rows)
