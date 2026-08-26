from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/"src"))
from pdr.config import load_config
from pdr.simulate import generate_synthetic_imu
from pdr.preprocessing import preprocess_imu
from pdr.step_detection import detect_steps
from pdr.heading import fused_heading

def test_pipeline_smoke():
    cfg=load_config(ROOT/"config.yaml"); df=generate_synthetic_imu(duration_s=10,fs=cfg["sampling_rate_hz"]); proc=preprocess_imu(df,cfg); steps=detect_steps(proc,cfg); h=fused_heading(proc,cfg)
    assert len(proc)==len(df); assert len(h)==len(df); assert len(steps)>0
