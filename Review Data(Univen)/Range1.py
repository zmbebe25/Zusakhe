import json
import pandas as pd
import matplotlib.pyplot as plt

# Use a non-interactive backend for matplotlib
import matplotlib
matplotlib.use('Agg')

# Load Data
with open("c:/Users/zusakhe_gradesmatch/Downloads/User_Review(2024).json", "r") as file:
    data = json.load(file)

# Extract institution review times
def extract_institution_review_times(data):
    institution_times = {}
    for entry in data:
        # Ensure "PreferredInsitutions" and "ReviewTimes" exist
        preferred_institutions = entry.get("PreferredInsitutions", [])
        if not preferred_institutions:
            continue

        review_times = entry.get("ReviewTimes", {})
        if not review_times:
            continue

        # Calculate total review time in hours
        total_review_time_hours = sum(review_times.values()) / 3600

        for institution in preferred_institutions:
            institution_name = institution.get("Name")
            if not isinstance(institution_name, str) or institution_name is None:
                print(f"Skipping invalid institution entry: {institution}")
                continue
            institution_times[institution_name] = institution_times.get(institution_name, 0) + total_review_time_hours
    return institution_times

# Process review times
institution_review_times = extract_institution_review_times(data)

# Create a bar chart for review times by institution
def create_bar_chart(data, title, output_file):
    institutions = list(data.keys())
    review_times = list(data.values())

    if not institutions or not review_times:
        print("No valid data to plot.")
        return

    plt.figure(figsize=(12, 8))
    plt.barh(institutions, review_times)
    plt.xlabel("Review Time (Hours)", fontsize=14)
    plt.ylabel("Institutions", fontsize=14)
    plt.title(title, fontsize=16, weight="bold")
    plt.tight_layout()
    plt.savefig(output_file, dpi=300)  # Save chart as high-resolution image
    plt.close()

# Create bar chart for review times
create_bar_chart(
    institution_review_times,
    "Total Review Times by Institution",
    "bar_chart_review_times_by_institution.png"
)

print("Bar chart for total review times by institution saved.")
