import csv
import numpy as np
from scipy.signal import find_peaks
import matplotlib.pyplot as plt


numbers_array = []

with open("filtered_data_12.csv", 'r') as file:
    reader = csv.reader(file)
    next(reader)
    for row in reader:
        numbers_array.append(float(row[0]))


numbers_array = np.array(numbers_array)

ppg_signal = numbers_array
fs =20

peaks, _ = find_peaks(ppg_signal, distance=fs*0.5)  # assuming heart rate > 60 bpm

# 2. Compute peak-to-peak intervals
peak_intervals = np.diff(peaks) / fs  # convert sample difference to time in seconds

# Now you can analyze the intervals
print("Peak-to-peak intervals (s):", peak_intervals)

# Optional: plot the signal with peaks
plt.plot(ppg_signal)
plt.plot(peaks, ppg_signal[peaks], "x")
plt.title("PPG Signal with Detected Peaks")
plt.show()


