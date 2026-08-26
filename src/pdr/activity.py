from __future__ import annotations
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from .preprocessing import preprocess_imu
from .features import window_features

NONFEATURE={"start_idx","end_idx","center_idx","timestamp","label"}

class MovementClassifier:
    def __init__(self,cfg):
        self.cfg=cfg; a=cfg["activity"]
        self.model=RandomForestClassifier(n_estimators=int(a["n_estimators"]),random_state=int(a["random_state"]),min_samples_leaf=int(a["min_samples_leaf"]),class_weight="balanced_subsample",n_jobs=-1)
        self.feature_columns=[]; self.is_fitted=False
    def fit(self,df):
        if "label" not in df.columns: raise ValueError("Training requires a 'label' column.")
        feats=window_features(preprocess_imu(df,self.cfg),self.cfg)
        self.feature_columns=[c for c in feats.columns if c not in NONFEATURE]
        y=feats.label.astype(str)
        if y.nunique()<2: raise ValueError("Need at least two movement classes.")
        self.model.fit(feats[self.feature_columns].fillna(0),y); self.is_fitted=True; return self
    def predict_windows(self,proc_df):
        feats=window_features(proc_df,self.cfg)
        if len(feats)==0: return pd.DataFrame(columns=["start_idx","end_idx","center_idx","timestamp","mode"])
        if self.is_fitted: pred=self.model.predict(feats[self.feature_columns].fillna(0))
        else:
            std=feats.acc_dyn_std.to_numpy(); gyro=feats.gyro_mag_mean.to_numpy(); q1=np.quantile(std,.35); q2=np.quantile(std,.75); g2=np.quantile(gyro,.75)
            pred=np.array(["fast" if s>=q2 else "stairs" if g>=g2 else "incline" if s<=q1 else "normal" for s,g in zip(std,gyro)],dtype=object)
        out=feats[["start_idx","end_idx","center_idx","timestamp"]].copy(); out["mode"]=pred; return out
    def sample_modes(self,proc_df):
        wins=self.predict_windows(proc_df); modes=np.empty(len(proc_df),dtype=object); modes[:]=None
        for r in wins.itertuples(): modes[int(r.start_idx):int(r.end_idx)+1]=str(r.mode)
        return pd.Series(modes).ffill().bfill().fillna("normal").to_numpy(object)
    def save(self,path): joblib.dump({"model":self.model,"feature_columns":self.feature_columns,"is_fitted":self.is_fitted},path)
    def load(self,path):
        p=joblib.load(path); self.model=p["model"]; self.feature_columns=p["feature_columns"]; self.is_fitted=p["is_fitted"]; return self
