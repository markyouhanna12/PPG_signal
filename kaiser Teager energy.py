import csv
import matplotlib.pyplot as plt
from scipy.stats import skew
import numpy as np

numbers_array = []

with open("filtered_data_12.csv", 'r') as file:
    reader = csv.reader(file)
    next(reader)
    for row in reader:
        numbers_array.append(float(row[0]))


numbers_array = np.array(numbers_array)

def teager_kaiser_energy(signal):
    # Apply TKEO: psi[x(n)] = x(n)^2 - x(n-1)*x(n+1)
    tke = np.zeros_like(signal)
    tke[1:-1] = signal[1:-1]**2 - signal[:-2] * signal[2:]
    return tke

# Apply TKEO to the signal
tke_signal = teager_kaiser_energy(numbers_array)

tke_mean=np.mean(tke_signal)
tke_variance=np.var(tke_signal)
tke_skew=skew(tke_signal)
print(tke_mean)
print(tke_variance)
print(tke_skew)



# Plot the original signal and its TKE
plt.figure(figsize=(12, 6))

plt.subplot(2, 1, 1)
plt.plot(numbers_array, label='Original Signal')
plt.title('Original Signal')
plt.xlabel('Sample Index')
plt.ylabel('Amplitude')
plt.grid(True)
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(tke_signal, color='orange', label='Teager-Kaiser Energy')
plt.title('Teager-Kaiser Energy Operator')
plt.xlabel('Sample Index')
plt.ylabel('Energy')
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()
