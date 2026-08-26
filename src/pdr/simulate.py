import numpy as np
import pandas as pd

def generate_synthetic_imu(duration_s=80.0,fs=50.0,seed=42):
    rng=np.random.default_rng(seed); n=int(duration_s*fs); t=np.arange(n)/fs
    def mode(x):
        p=x/duration_s
        return "normal" if p<.25 else "fast" if p<.5 else "stairs" if p<.75 else "incline"
    labels=np.array([mode(x) for x in t],dtype=object)
    freq={"normal":1.8,"fast":2.4,"stairs":1.6,"incline":1.7}; amp={"normal":1.6,"fast":2.5,"stairs":2.0,"incline":1.4}; speed={"normal":1.2,"fast":1.8,"stairs":.8,"incline":1.0}
    phase=np.zeros(n); a=0.0
    for i in range(1,n): a+=2*np.pi*freq[labels[i]]/fs; phase[i]=a
    ax=.25*np.sin(phase+.4)+rng.normal(0,.12,n); ay=.18*np.sin(.5*phase)+rng.normal(0,.10,n); az=9.81+np.array([amp[m] for m in labels])*np.maximum(0,np.sin(phase))+rng.normal(0,.15,n)
    heading=.2*np.sin(2*np.pi*t/duration_s)+.7*(t/duration_s); rate=np.gradient(heading,1/fs)
    gx=.03*np.sin(phase)+rng.normal(0,.01,n); gy=.02*np.cos(phase)+rng.normal(0,.01,n); gz=rate+rng.normal(0,.008,n)
    field=45.0; mx=field*np.cos(heading)+rng.normal(0,.8,n); my=-field*np.sin(heading)+rng.normal(0,.8,n); mz=8+rng.normal(0,.5,n)
    gt_x=np.zeros(n); gt_y=np.zeros(n)
    for i in range(1,n):
        v=speed[labels[i]]; dt=1/fs; gt_x[i]=gt_x[i-1]+v*np.cos(heading[i])*dt; gt_y[i]=gt_y[i-1]+v*np.sin(heading[i])*dt
    return pd.DataFrame({"timestamp":t,"ax":ax,"ay":ay,"az":az,"gx":gx,"gy":gy,"gz":gz,"mx":mx,"my":my,"mz":mz,"label":labels,"gt_x":gt_x,"gt_y":gt_y})
