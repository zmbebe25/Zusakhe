import json
import pandas as pd
import matplotlib.pyplot as plt

# Use a non-interactive backend for matplotlib
import matplotlib
matplotlib.use('Agg')

# Load Data
with open("c:/Users/zusakhe_gradesmatch/Downloads/User_Review(2024).json", "r") as file:
    data = json.load(file)

# Extract chosen institutions and review times
def extract_institution_review_times(category_summaries, review_type):
    institution_times = {}
    for category, summary in category_summaries.items():
        review = summary.get(review_type)
        if review:
            chosen_institutions = review["ChosenInstitutions"]
            review_time = pd.to_timedelta(review["ReviewTime"]).total_seconds() / 3600  # Convert to hours
            for institution in chosen_institutions:
                institution_times[institution] = institution_times.get(institution, 0) + review_time
    return institution_times

# Process fastest and slowest review times
fastest_institution_times = extract_institution_review_times(data["CategorySummaries"], "FastestReview")
slowest_institution_times = extract_institution_review_times(data["CategorySummaries"], "SlowestReview")

# Function to create a pie chart with a legend
def create_pie_chart_with_legend(data, title, output_file):
    plt.figure(figsize=(12, 12))  # Increased figure size
    wedges, texts, autotexts = plt.pie(
        data.values(),
        labels=None,  # Hide labels from the pie
        autopct='%1.1f%%',
        startangle=140,
        explode=[0.05] * len(data),  # Slightly explode each slice
        textprops={'fontsize': 14}  # Adjust percentage text font size
    )
    plt.setp(autotexts, size=14, weight="bold")  # Make percentage text bold and larger
    plt.title(title, fontsize=16, weight="bold")  # Larger and bold title font
    plt.legend(wedges, data.keys(), title="Institutions", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1), fontsize=12)  # Add a legend
    plt.tight_layout()  # Adjust layout for better spacing
    plt.savefig(output_file, dpi=300)  # Save chart as high-resolution image
    plt.close()

# Create pie chart for fastest review times
create_pie_chart_with_legend(
    fastest_institution_times,
    "Fastest Review Times by Chosen Institution",
    "pie_chart_fastest_chosen_institutions_weighted_with_legend.png"
)

# Create pie chart for slowest review times
create_pie_chart_with_legend(
    slowest_institution_times,
    "Slowest Review Times by Chosen Institution",
    "pie_chart_slowest_chosen_institutions_weighted_with_legend.png"
)

print("High-resolution weighted pie charts with legends for fastest and slowest review times saved.")
