import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
import random

# Use a non-interactive backend for matplotlib
matplotlib.use('Agg')

# Define input and output file paths
json_path = "C:/Users/zusakhe_gradesmatch/Downloads/MatchedQualificationGroup_WithCounts(2024).json"  # Replace with your JSON file path
output_path = "C:/Users/zusakhe_gradesmatch/Downloads/Top20_Qualifications_Heatmap.png"  # Output heatmap path

# Load JSON data
with open(json_path, "r", encoding="utf-8") as file:
    grouped_data = json.load(file)

# Extract qualifications by CombinedTimeMinutes categories and their counts
categories = [
    "CombinedTimeMinutes < 1",
    "7 <= CombinedTimeMinutes < 20",
    "20 <= CombinedTimeMinutes < 40",
    "40 <= CombinedTimeMinutes < 60",
    "60 <= CombinedTimeMinutes < 80",
    "80 <= CombinedTimeMinutes < 100",
    "100 <= CombinedTimeMinutes < 180",
    "CombinedTimeMinutes >= 180"
]

# Prepare a dictionary to store data
heatmap_data = {}

for category in categories:
    heatmap_data[category] = {}
    for entry in grouped_data.get(category, []):
        for qualification in entry.get("MatchedQualifications", []):
            heatmap_data[category][qualification] = heatmap_data[category].get(qualification, 0) + 1

# Convert the dictionary to a DataFrame
heatmap_df = pd.DataFrame(heatmap_data).fillna(0).astype(int)

# Select the top 20 qualifications randomly
if len(heatmap_df) > 20:
    selected_qualifications = random.sample(list(heatmap_df.index), 20)
    heatmap_df = heatmap_df.loc[selected_qualifications]

# Generate a heatmap for the selected qualifications
plt.figure(figsize=(15, 10))
sns.heatmap(
    heatmap_df,
    annot=True,  # Include counts on the heatmap
    fmt="d",  # Format annotations as integers
    cmap="Blues",
    linewidths=0.5,
    linecolor='gray'
)

# Add titles and labels
plt.title("Heatmap of Top 20 Randomly Selected Matched Qualification Groups(2024)", fontsize=14)
plt.xlabel("Combined Time Categories", fontsize=12)
plt.ylabel("Matched Qualifications", fontsize=12)

# Save the heatmap
plt.savefig(output_path, dpi=300, bbox_inches="tight")
plt.close()

print(f"Heatmap saved to {output_path}")
