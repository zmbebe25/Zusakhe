import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
import os

# Use a non-interactive backend for matplotlib
matplotlib.use('Agg')

# Define input and output file paths
json_path = "C:/Users/zusakhe_gradesmatch/Downloads/MatchedQualificationGroup_WithCounts(2023).json"  # Replace with your JSON file path
output_folder = "C:/Users/zusakhe_gradesmatch/Downloads/Heatmaps/"  # Output folder for individual heatmaps

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Load JSON data
with open(json_path, "r", encoding="utf-8") as file:
    grouped_data = json.load(file)

# Extract schools by CombinedTimeMinutes categories and their counts
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
heatmap_data = {category: {} for category in categories}

# Populate heatmap_data based on school occurrences in each category
for entry in grouped_data:
    school_name = entry.get("School", None)
    if school_name:
        combined_time = entry["TotalReviewTime"]["CombinedTimeMinutes"]
        for category in categories:
            if category == "CombinedTimeMinutes < 1" and combined_time < 1:
                heatmap_data[category][school_name] = heatmap_data[category].get(school_name, 0) + 1
            elif category == "7 <= CombinedTimeMinutes < 20" and 7 <= combined_time < 20:
                heatmap_data[category][school_name] = heatmap_data[category].get(school_name, 0) + 1
            elif category == "20 <= CombinedTimeMinutes < 40" and 20 <= combined_time < 40:
                heatmap_data[category][school_name] = heatmap_data[category].get(school_name, 0) + 1
            elif category == "40 <= CombinedTimeMinutes < 60" and 40 <= combined_time < 60:
                heatmap_data[category][school_name] = heatmap_data[category].get(school_name, 0) + 1
            elif category == "60 <= CombinedTimeMinutes < 80" and 60 <= combined_time < 80:
                heatmap_data[category][school_name] = heatmap_data[category].get(school_name, 0) + 1
            elif category == "80 <= CombinedTimeMinutes < 100" and 80 <= combined_time < 100:
                heatmap_data[category][school_name] = heatmap_data[category].get(school_name, 0) + 1
            elif category == "100 <= CombinedTimeMinutes < 180" and 100 <= combined_time < 180:
                heatmap_data[category][school_name] = heatmap_data[category].get(school_name, 0) + 1
            elif category == "CombinedTimeMinutes >= 180" and combined_time >= 180:
                heatmap_data[category][school_name] = heatmap_data[category].get(school_name, 0) + 1

# Convert the dictionary to a DataFrame
heatmap_df = pd.DataFrame(heatmap_data).fillna(0).astype(int)

# Select the top 30 schools by the total count
top_schools = heatmap_df.sum(axis=1).sort_values(ascending=False).head(30).index
heatmap_df = heatmap_df.loc[top_schools]

# Generate separate heatmaps for categories with the most impact (highest total counts)
impactful_categories = heatmap_df.sum(axis=0).sort_values(ascending=False).index[:3]  # Top 3 impactful categories

for category in impactful_categories:
    category_data = heatmap_df[[category]].sort_values(by=category, ascending=False)
    plt.figure(figsize=(10, 8))
    sns.heatmap(
        category_data,
        annot=True,
        fmt="d",
        cmap="Blues",
        linewidths=0.5,
        linecolor='gray'
    )

    # Add titles and labels
    plt.title(f"Heatmap of {category} (2023)", fontsize=14)
    plt.xlabel("Combined Time Category", fontsize=12)
    plt.ylabel("Schools", fontsize=12)

    # Save the heatmap for this category
    category_output_path = f"{output_folder}{category.replace(' ', '_').replace('<', 'lt').replace('>', 'gt')}.png"
    plt.savefig(category_output_path, dpi=300, bbox_inches="tight")
    plt.close()

print(f"Heatmaps for impactful categories have been saved in {output_folder}")
