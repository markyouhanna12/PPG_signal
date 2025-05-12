import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('Non-diabatic(Short periods).csv')

df_features = df.iloc[:, 1:]

df_features = df_features.select_dtypes(include='number')

for column in df_features.columns:
    feature_values = df_features[column].dropna().values.reshape(-1, 1)

    distance_matrix = np.sqrt((feature_values - feature_values.T) ** 2)

    plt.figure(figsize=(8, 6))
    sns.heatmap(distance_matrix, cmap='viridis', annot=True, fmt=".2f")
    plt.title(f'Euclidean Distance Heatmap - {column}')
    plt.xlabel('Sample Index')
    plt.ylabel('Sample Index')
    plt.show()
