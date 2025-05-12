import csv
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt

def butter_lowpass(cutoff, fs, order=5):
    nyquist = 0.5 * fs  # Nyquist frequency
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def apply_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    filtered_data = filtfilt(b, a, data)
    return filtered_data

numbers_array = []

with open("C:/Users/marky/OneDrive/Desktop/graduation/Graduation/test(short period -non filtered)/Z_8.csv", 'r') as file:
    reader = csv.reader(file)
    next(reader)
    for row in reader:
        numbers_array.append(float(row[0]))

def main():
    fs = 1000
    cutoff = 100
    order = 4
    data =numbers_array
    filtered_signal = apply_filter(data, cutoff, fs, order)
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    axes[0].plot(data, label="Original data")
    axes[0].set_title("Original Data")
    axes[1].plot(filtered_signal, label="butterworth filter")
    axes[1].set_title("butterworth filter")
    plt.show()

    with open("test_12_35pm.csv", 'w', newline='') as file:
        writer = csv.writer(file)
        for value in filtered_signal:
            writer.writerow([value])


if __name__ == "__main__":
    main()