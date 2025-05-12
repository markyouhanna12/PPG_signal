import numpy as np
import csv
import matplotlib.pyplot as plt


numbers_array = []

with open("filtered_data_12.csv", 'r') as file:
    reader = csv.reader(file)
    next(reader)
    for row in reader:
        numbers_array.append(float(row[0]))


numbers_array = np.array(numbers_array)
ppg_signal = numbers_array

# Parameters
frame_size = 50  # Number of samples per frame
epsilon = 1e-10  # To avoid log(0)
log_energy = []

# Sliding window
for i in range(0, len(ppg_signal), frame_size):
    frame = ppg_signal[i:i+frame_size]
    energy = np.sum(frame ** 2)
    log_energy.append(np.log(energy + epsilon))

log_energy_array = np.array(log_energy)

features = {
"interquartile_range": np.percentile(log_energy_array, 75) - np.percentile(log_energy_array, 25),
    "mean": np.mean(log_energy_array),
    "variance": np.var(log_energy_array),}

print("Extracted Log Energy Features:")
for k, v in features.items():
    print(f"{k}: {v:.4f}")


# Plot original PPG and log energy
plt.figure(figsize=(12, 5))
plt.subplot(2, 1, 1)
plt.plot(ppg_signal, label='PPG Signal')
plt.title('Original PPG Signal')
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(log_energy, label='Log Energy', color='orange')
plt.title('Logarithmic Energy (Frame-wise)')
plt.legend()
plt.tight_layout()
plt.show()