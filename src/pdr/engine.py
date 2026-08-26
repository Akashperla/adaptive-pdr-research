from __future__ import annotations
from dataclasses import dataclass
import numpy as np
import pandas as pd
from .preprocessing import preprocess_imu
from .step_detection import detect_steps
from .step_length import estimate_step_length
from .heading import fused_heading, wrap_pi
from .activity import MovementClassifier

@dataclass
class PDRResult:
    trajectory: pd.DataFrame
    processed_imu: pd.DataFrame
    steps: pd.DataFrame

class AdaptivePDREngine:
    def __init__(self,cfg,movement_classifier=None):
        self.cfg=cfg; self.classifier=movement_classifier or MovementClassifier(cfg)
    def run(self,df):
        proc=preprocess_imu(df,self.cfg); headings=fused_heading(proc,self.cfg); proc["heading_rad"]=headings
        modes=self.classifier.sample_modes(proc); proc["mode"]=modes; steps=detect_steps(proc,self.cfg)
        x=y=0.0; rows=[{"step_number":0,"timestamp":float(proc.timestamp.iloc[0]),"sample_idx":0,"mode":"start","step_length_m":0.0,"heading_rad":float(headings[0]),"x_m":0.0,"y_m":0.0}]
        for k,s in enumerate(steps.itertuples(),1):
            idx=int(s.sample_idx); mode=str(modes[idx]); L=estimate_step_length(proc,idx,mode,self.cfg)
            corr=float(self.cfg["mode_parameters"].get(mode,self.cfg["mode_parameters"]["normal"])["heading_correction"])
            theta=float(wrap_pi(headings[idx]*corr)); x+=L*np.cos(theta); y+=L*np.sin(theta)
            rows.append({"step_number":k,"timestamp":float(s.timestamp),"sample_idx":idx,"mode":mode,"step_length_m":L,"heading_rad":theta,"x_m":float(x),"y_m":float(y)})
        return PDRResult(pd.DataFrame(rows),proc,steps)
