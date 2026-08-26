import numpy as np

def evaluate_trajectory(trajectory,imu_df):
    if not {"gt_x","gt_y"}.issubset(imu_df.columns): return {"note":"No gt_x/gt_y columns found.","num_steps":int(max(0,len(trajectory)-1))}
    gt=imu_df[["timestamp","gt_x","gt_y"]].dropna().sort_values("timestamp")
    t=trajectory.timestamp.to_numpy(float); gx=np.interp(t,gt.timestamp,gt.gt_x); gy=np.interp(t,gt.timestamp,gt.gt_y)
    e=np.sqrt((trajectory.x_m.to_numpy()-gx)**2+(trajectory.y_m.to_numpy()-gy)**2)
    return {"num_steps":int(max(0,len(trajectory)-1)),"endpoint_error_m":float(e[-1]),"trajectory_rmse_m":float(np.sqrt(np.mean(e**2))),"mean_position_error_m":float(np.mean(e))}
