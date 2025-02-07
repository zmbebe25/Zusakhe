import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib

# Use a non-interactive backend for matplotlib
matplotlib.use('Agg')

# Define input and output file paths
json_path = "C:/Users/zusakhe_gradesmatch/Downloads/Grouped_User_Data.json"  # Replace with your JSON file path
output_dir = "C:/Users/zusakhe_gradesmatch/Downloads/"  # Directory to save the heatmaps

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

# Split the DataFrame into chunks for better visualization
chunk_size = 10  # Number of qualifications per heatmap
qualification_chunks = [
    heatmap_df.iloc[i:i + chunk_size] for i in range(0, len(heatmap_df), chunk_size)
]

# Generate a heatmap for each chunk
for idx, chunk in enumerate(qualification_chunks):
    plt.figure(figsize=(15, 10))
    sns.heatmap(
        chunk,
        annot=True,  # Include counts on the heatmap
        fmt="d",  # Format annotations as integers
        cmap="Blues",
        linewidths=0.5,
        linecolor='gray'
    )

    # Add titles and labels
    plt.title(f"Heatmap of Matched Qualifications (Part {idx + 1})", fontsize=14)
    plt.xlabel("Combined Time Categories", fontsize=12)
    plt.ylabel("Matched Qualifications", fontsize=12)

    # Save each heatmap
    output_image_path = f"{output_dir}Heatmap_CombinedTimeMinutes_Part{idx + 1}.png"
    plt.savefig(output_image_path, dpi=300, bbox_inches="tight")
    plt.close()

    print(f"Heatmap saved to {output_image_path}")
