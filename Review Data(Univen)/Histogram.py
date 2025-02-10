# Use a non-interactive backend for matplotlib
import matplotlib
matplotlib.use('Agg')

import json
import matplotlib.pyplot as plt
import numpy as np

# Load Data
with open("C:/Users/zusakhe_gradesmatch/Downloads/MatchedQualificationGroup_WithCounts(2023).json", "r", encoding="utf-8") as file_2023:
    data_2023 = json.load(file_2023)

with open("C:/Users/zusakhe_gradesmatch/Downloads/MatchedQualificationGroup_WithCounts(2024).json", "r", encoding="utf-8") as file_2024:
    data_2024 = json.load(file_2024)

# Extract MatchPercentages
match_percentages_2023 = [entry.get("MatchPercentage", 0) for entry in data_2023]
match_percentages_2024 = [entry.get("MatchPercentage", 0) for entry in data_2024]

# Configure bins for both datasets
bins = np.linspace(0, 100, 11)  # 10 bins from 0% to 100%

# Plot the histograms
plt.figure(figsize=(12, 8))
hist_2023, bin_edges_2023, _ = plt.hist(match_percentages_2023, bins=bins, color='skyblue', alpha=0.7, label="2023", edgecolor='black')
hist_2024, bin_edges_2024, _ = plt.hist(match_percentages_2024, bins=bins, color='lightcoral', alpha=0.7, label="2024", edgecolor='black')

# Add percentage labels on top of each bar for 2023
for count, x in zip(hist_2023, bin_edges_2023[:-1]):
    percentage_label = f"{count / len(match_percentages_2023) * 100:.1f}%"
    plt.text(x + (bin_edges_2023[1] - bin_edges_2023[0]) / 4, count + 1, percentage_label,
             ha='center', fontsize=10, color='black')

# Add percentage labels on top of each bar for 2024
for count, x in zip(hist_2024, bin_edges_2024[:-1]):
    percentage_label = f"{count / len(match_percentages_2024) * 100:.1f}%"
    plt.text(x + 3 * (bin_edges_2024[1] - bin_edges_2024[0]) / 4, count + 1, percentage_label,
             ha='center', fontsize=10, color='black')

# Configure plot details
plt.title(f"Distribution of Qualification Match Percentage 2023 (n={len(match_percentages_2023)}) vs 2024 (n={len(match_percentages_2024)})", fontsize=14, weight='bold')
plt.xlabel(" Qualification Match Percentage (%)", fontsize=12)
plt.ylabel("Number of Users", fontsize=12)
plt.legend(fontsize=12)
plt.grid(axis='y', alpha=0.75)

# Save the combined histogram
output_histogram_path = "C:/Users/zusakhe_gradesmatch/Downloads/MatchPercentage_Histogram_2023_2024_Labeled.png"
plt.savefig(output_histogram_path, dpi=300)
plt.close()

print(f"Histogram comparing 2023 and 2024 saved to {output_histogram_path}")
