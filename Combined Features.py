import numpy as np
import pandas as pd
from scipy.stats import skew
import csv
import os
from scipy.signal import welch

input_file = "test_12_35pm.csv"
output_file = "Non-diabatic(Short periods).csv"


with open(input_file, 'r') as file:
    reader = csv.reader(file)
    next(reader)
    signal = np.array([float(row[0]) for row in reader])

def teager_kaiser_energy(signal):
    tke = np.zeros_like(signal)
    tke[1:-1] = signal[1:-1]**2 - signal[:-2] * signal[2:]
    return tke

tke_signal = teager_kaiser_energy(signal)
tke_mean = np.mean(tke_signal)
tke_variance = np.var(tke_signal)
tke_skew = skew(tke_signal)

frame_size = 50
epsilon = 1e-10
log_energy = [
    np.log(np.sum(signal[i:i+frame_size] ** 2) + epsilon)
    for i in range(0, len(signal), frame_size)
]
log_energy = np.array(log_energy)
logE_iqr = np.percentile(log_energy, 75) - np.percentile(log_energy, 25)
logE_mean = np.mean(log_energy)
logE_variance = np.var(log_energy)

def spectral_entropy(ppg, fs):
    freqs, psd = welch(ppg, fs=fs)
    psd_norm = psd / np.sum(psd)  # Normalize
    return psd_norm

psd_norm=spectral_entropy(signal,100)
se = -np.sum(psd_norm * np.log2(psd_norm + 1e-12))

# ---------- Collect features ----------
features = {
    "source_file": input_file,
    "Spectral Entropy": se,
    "TKE(MEAN)": tke_mean,
    "TKE (variance)": tke_variance,
    "TKE (skewness)": tke_skew,
    "logE(interquartile range)": logE_iqr,
    "logE(mean)": logE_mean,
    "logE(variance)": logE_variance,}



df = pd.DataFrame([features])
if not os.path.exists(output_file):
    df.to_csv(output_file, index=False)
else:
    df.to_csv(output_file, mode='a', header=False, index=False)

print(f"Features from {input_file} saved to {output_file}")
