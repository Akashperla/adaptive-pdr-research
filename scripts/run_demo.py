from pathlib import Path
import json,sys
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/"src"))
from pdr.config import load_config
from pdr.simulate import generate_synthetic_imu
from pdr.activity import MovementClassifier
from pdr.engine import AdaptivePDREngine
from pdr.evaluation import evaluate_trajectory

def main():
    out=ROOT/"outputs"; out.mkdir(exist_ok=True); cfg=load_config(ROOT/"config.yaml")
    df=generate_synthetic_imu(fs=float(cfg["sampling_rate_hz"])); df.to_csv(out/"synthetic_imu.csv",index=False)
    split=int(.60*len(df)); clf=MovementClassifier(cfg).fit(df.iloc[:split].copy()); clf.save(out/"movement_model.joblib")
    result=AdaptivePDREngine(cfg,clf).run(df); result.trajectory.to_csv(out/"trajectory.csv",index=False); result.processed_imu.to_csv(out/"processed_imu.csv",index=False)
    metrics=evaluate_trajectory(result.trajectory,df); (out/"metrics.json").write_text(json.dumps(metrics,indent=2))
    plt.figure(figsize=(8,6)); plt.plot(df.gt_x,df.gt_y,label="Ground truth"); plt.plot(result.trajectory.x_m,result.trajectory.y_m,label="Adaptive PDR"); plt.xlabel("X (m)"); plt.ylabel("Y (m)"); plt.title("Synthetic Adaptive PDR Demo"); plt.axis("equal"); plt.grid(True,alpha=.3); plt.legend(); plt.tight_layout(); plt.savefig(out/"trajectory_plot.png",dpi=180); plt.close()
    print(json.dumps(metrics,indent=2)); print(f"Outputs: {out}")
if __name__=="__main__": main()
