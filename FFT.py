import numpy as np
import csv
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import welch

numbers_array=[]
with open('filtered_data_12.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader)
    for row in reader:
        numbers_array.append(float(row[0]))



fs = 1000  # sampling frequency in Hz
t = np.linspace(0, 1, fs, endpoint=False)  # 1 second duration
signal = numbers_array

# Perform FFT
N = len(signal)
frequencies = np.fft.fftfreq(N, d=1/fs)
fft_values = np.fft.fft(signal)

positive_freqs = frequencies[:N // 2]
magnitude = np.abs(fft_values[:N // 2]) * 2 / N  # normalize
phase = np.angle(fft_values[:N // 2])

def spectral_entropy(ppg, fs):
    freqs, psd = welch(ppg, fs=fs)
    psd_norm = psd / np.sum(psd)  # Normalize
    se = -np.sum(psd_norm * np.log2(psd_norm + 1e-12))  # Add epsilon to avoid log(0)
    print(se)


# ------------------ Print the Feature ------------------
spectral_entropy(signal,100)

# Plot the magnitude spectrum
plt.figure(figsize=(10, 4))
plt.plot(positive_freqs, magnitude)
plt.title("Magnitude Spectrum (Fourier Approximation)")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Amplitude")
plt.grid(True)
plt.show()

