import json
import matplotlib.pyplot as plt
import numpy as np

# Use a non-interactive backend for matplotlib
import matplotlib
matplotlib.use('Agg')

# Load Data
with open("c:/Users/zusakhe_gradesmatch/Downloads/Filtered_Performance_Category(2023).json", "r") as file_2023:
    data_2023 = json.load(file_2023)

with open("c:/Users/zusakhe_gradesmatch/Downloads/Filtered_Performance_Category(2024).json", "r") as file_2024:
    data_2024 = json.load(file_2024)

# Process review times by category
def process_review_times(data):
    performance_times = {}
    for category, entries in data.items():
        for entry_dict in entries:
            for user_id, details in entry_dict.items():
                combined_time = details["TotalReviewTime"]["CombinedTimeMinutes"]
                if category not in performance_times:
                    performance_times[category] = []
                performance_times[category].append(combined_time)
    return performance_times

performance_times_2023 = process_review_times(data_2023)
performance_times_2024 = process_review_times(data_2024)

# Combine data for plotting
categories = sorted(set(performance_times_2023.keys()).union(performance_times_2024.keys()))
combined_data = []
combined_labels = []
colors = []

for category in categories:
    if category in performance_times_2023:
        combined_data.append(performance_times_2023[category])
        combined_labels.append(f"{category} (2023)")
        colors.append("skyblue")  # Color for 2023
    if category in performance_times_2024:
        combined_data.append(performance_times_2024[category])
        combined_labels.append(f"{category} (2024)")
        colors.append("lightcoral")  # Color for 2024

# Plot Combined Box Plot with Unique Colors and Statistics Annotated
def plot_combined_box_plot_with_stats(data, labels, colors, title, xlabel, ylabel, output_file):
    if not data:
        print(f"No valid data to plot for {title}.")
        return

    plt.figure(figsize=(16, 10))
    boxprops = dict(linestyle='-', linewidth=2)
    medianprops = dict(color='black', linewidth=1.5)

    boxplot = plt.boxplot(data, labels=labels, patch_artist=True, boxprops=boxprops, medianprops=medianprops)

    # Apply unique colors to each box
    for patch, color in zip(boxplot['boxes'], colors):
        patch.set_facecolor(color)

    plt.xlabel(xlabel, fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    plt.title(title, fontsize=16, weight='bold')
    plt.xticks(rotation=45)

    # Annotate statistics on the plot
    for i, value in enumerate(data):
        if value:
            stats = {
                "Min": np.min(value),
                "Q1": np.percentile(value, 25),
                "Median": np.median(value),
                "Q3": np.percentile(value, 75),
                "Max": np.max(value),
            }
            # Position the text above each box
            x_position = i + 1
            y_max = stats["Max"]
            annotation_text = (
                f"Min: {stats['Min']:.2f}\n"
                f"Q1: {stats['Q1']:.2f}\n"
                f"Median: {stats['Median']:.2f}\n"
                f"Q3: {stats['Q3']:.2f}\n"
                f"Max: {stats['Max']:.2f}"
            )
            plt.text(
                x_position,
                y_max + 0.5,  # Adjust position above the max
                annotation_text,
                ha='center',
                fontsize=10,
                bbox=dict(facecolor='white', alpha=0.6, edgecolor='black', boxstyle='round,pad=0.3')
            )

    plt.tight_layout()
    plt.savefig(output_file, dpi=300)
    plt.close()

# Generate combined boxplot
plot_combined_box_plot_with_stats(
    combined_data,
    combined_labels,
    colors,
    "Review Time Distribution by Performance Category (2023 vs 2024)",
    "Performance Category",
    "Review Time (Minutes)",
    "review_time_distribution_combined_2023_2024_colored.png"
)

print("Combined boxplot with unique colors and annotated statistics has been saved.")
