import pandas as pd
import matplotlib.pyplot as plt
import csv

numbers_array = []

with open("zankalony.csv", 'r') as file:
    reader = csv.reader(file)
    next(reader)
    for row in reader:
        numbers_array.append(int(row[0]))

arr = numbers_array
window_size = 6

numbers_series = pd.Series(arr)

windows = numbers_series.rolling(window_size)
moving_averages = windows.mean()

moving_averages_list = moving_averages.tolist()

final_list = moving_averages_list[window_size - 1:]
fig, axes = plt.subplots(1, 2, figsize=(15, 6))
axes[0].plot(arr,label="Original data")
axes[0].set_title("Original Data")

axes[1].plot(final_list,label="Moving average Filter")
axes[1].set_title("Moving average Filter")
plt.show()

with open("filtered_data.csv", 'w', newline='') as file:
    writer = csv.writer(file)
    for value in final_list:
        writer.writerow([value])