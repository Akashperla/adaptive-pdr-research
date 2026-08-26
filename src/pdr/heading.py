from __future__ import annotations
import numpy as np
import pandas as pd

def wrap_pi(a):
    return (a + np.pi) % (2*np.pi) - np.pi

def tilt_compensated_mag_heading(ax, ay, az, mx, my, mz):
    ax, ay, az, mx, my, mz = [np.asarray(v, float) for v in (ax,ay,az,mx,my,mz)]
    roll = np.arctan2(ay, az)
    pitch = np.arctan2(-ax, np.sqrt(ay**2 + az**2) + 1e-12)
    mx_h = mx*np.cos(pitch) + mz*np.sin(pitch)
    my_h = mx*np.sin(roll)*np.sin(pitch) + my*np.cos(roll) - mz*np.sin(roll)*np.cos(pitch)
    return np.arctan2(-my_h, mx_h)

def fused_heading(df: pd.DataFrame, cfg: dict) -> np.ndarray:
    alpha = float(cfg["heading"]["complementary_alpha"])
    t = df["timestamp"].to_numpy(float)
    gz = df["gz_f"].to_numpy(float)
    if cfg["heading"].get("gyro_units") == "deg_s":
        gz = np.deg2rad(gz)
    mag = tilt_compensated_mag_heading(df.ax_f,df.ay_f,df.az_f,df.mx_f,df.my_f,df.mz_f)
    out = np.zeros(len(df), float)
    out[0] = mag[0]
    for i in range(1, len(df)):
        dt = max(1e-4, t[i]-t[i-1])
        pred = wrap_pi(out[i-1] + gz[i]*dt)
        out[i] = wrap_pi(pred + (1-alpha)*wrap_pi(mag[i]-pred))
    return out
