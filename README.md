# Adaptive Pedestrian Dead Reckoning (PDR)

A runnable Python research baseline for a mode-aware Pedestrian Dead Reckoning system using smartphone IMU data.

## Pipeline
1. Accelerometer + gyroscope + magnetometer ingestion
2. Low-pass preprocessing
3. Step detection
4. Window-based movement recognition
5. Mode-aware parameters
6. Step-length estimation
7. Tilt-compensated magnetometer heading + gyro complementary fusion
8. Position update
9. Ground-truth evaluation
10. Synthetic end-to-end demo

## Important note
The source report specifies the high-level architecture, but not every low-level algorithm. This code therefore uses modern baseline engineering choices: Butterworth filtering, SciPy peak detection, RandomForest classification, a Weinberg-style step-length model, and complementary heading fusion. These are implementation choices for a reproducible research prototype.

## CSV format
Required columns:
`timestamp, ax, ay, az, gx, gy, gz, mx, my, mz`

Optional:
`label, gt_x, gt_y`

Default units: seconds, m/s^2, rad/s, microtesla.

## Run
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
python scripts/run_demo.py
```

Outputs appear in `outputs/`:
- synthetic_imu.csv
- processed_imu.csv
- movement_model.joblib
- trajectory.csv
- trajectory_plot.png
- metrics.json

## Recommended research extensions
- compare RandomForest, SVM, 1D-CNN, and LSTM
- add wavelet or EMD decomposition
- compare Madgwick/Mahony/EKF attitude estimation
- add zero-velocity updates
- personalize step length by subject
- fuse PDR with Wi-Fi/BLE/GPS
- evaluate phone placement robustness
- run leave-one-subject-out validation
