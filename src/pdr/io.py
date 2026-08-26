from __future__ import annotations
import pandas as pd

REQUIRED_COLUMNS = ["timestamp","ax","ay","az","gx","gy","gz","mx","my","mz"]

def validate_imu_frame(df: pd.DataFrame) -> None:
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required IMU columns: {missing}")
    if len(df) < 10:
        raise ValueError("IMU frame is too short for PDR processing.")
    if not df["timestamp"].is_monotonic_increasing:
        raise ValueError("timestamp must be monotonically increasing.")

def load_imu_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    validate_imu_frame(df)
    return df
