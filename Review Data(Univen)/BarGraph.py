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

# Process review times
def process_review_times(data):
    category_times = {}
    for category, entries in data.items():
        for entry_dict in entries:
            for user_id, details in entry_dict.items():
                total_time_minutes = details["TotalReviewTime"]["CombinedTimeMinutes"]

                # Aggregate review times by performance category
                if category not in category_times:
                    category_times[category] = []
                category_times[category].append(total_time_minutes)
    return category_times

category_times_2023 = process_review_times(data_2023)
category_times_2024 = process_review_times(data_2024)

# Calculate statistics (total, count, average)
def calculate_statistics(data):
    stats = {}
    for key, times in data.items():
        total = sum(times)
        count = len(times)
        average = total / count if count > 0 else 0
        stats[key] = {"Total": total, "Count": count, "Average": average}
    return stats

category_stats_2023 = calculate_statistics(category_times_2023)
category_stats_2024 = calculate_statistics(category_times_2024)

# Combine data for plotting
categories = sorted(set(category_stats_2023.keys()).union(category_stats_2024.keys()))
averages_2023 = [category_stats_2023.get(cat, {"Average": 0})["Average"] for cat in categories]
averages_2024 = [category_stats_2024.get(cat, {"Average": 0})["Average"] for cat in categories]

# Plot bar chart with annotations
def plot_combined_bar_chart(categories, averages_2023, averages_2024, title, xlabel, ylabel, output_file):
    x = np.arange(len(categories))  # Label locations
    width = 0.35  # Bar width

    plt.figure(figsize=(12, 8))
    bars_2023 = plt.bar(x - width / 2, averages_2023, width, label="2023", color='skyblue')
    bars_2024 = plt.bar(x + width / 2, averages_2024, width, label="2024", color='lightgreen')

    # Annotate bars with average values
    for bars, averages in zip([bars_2023, bars_2024], [averages_2023, averages_2024]):
        for bar, avg in zip(bars, averages):
            height = bar.get_height()
            if height > 0:
                plt.text(
                    bar.get_x() + bar.get_width() / 2,
                    height + 0.1,
                    f"{avg:.2f}",
                    ha='center',
                    va='bottom',
                    fontsize=10
                )

    plt.xlabel(xlabel, fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    plt.title(title, fontsize=14, weight='bold')
    plt.xticks(x, categories, rotation=45, fontsize=10)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_file, dpi=300)
    plt.close()

# Generate combined graph
plot_combined_bar_chart(
    categories,
    averages_2023,
    averages_2024,
    "Average Review Time per Performance Category (2023 vs 2024)",
    "Performance Category",
    "Review Time (Minutes)",
    "combined_review_time_per_category_2023_2024.png"
)

print("Combined graph for 2023 and 2024 has been saved successfully.")
