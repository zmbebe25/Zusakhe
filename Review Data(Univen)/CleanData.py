import json
import random

# Define input and output file paths
input_path = "c:/Users/zusakhe_gradesmatch/Downloads/User_Review(Performance_Category(2023)).json"
output_path = "c:/Users/zusakhe_gradesmatch/Downloads/Filtered_Performance_Category(2023).json"

# Load data from JSON
with open(input_path, "r") as file:
    data = json.load(file)

# Define time thresholds for each performance category as ranges (min, max)
time_thresholds = {
    "Inadequate Learner": (5, 7),   # 5-7 minutes
    "Moderate Learner": (5, 6),     # 5-6 minutes
    "Adequate Learner": (4, 5),     # 4-5 minutes
    "Good Learner": (3, 4),         # 3-4 minutes
    "Proficient Learner": (2, 3),   # 2-3 minutes
    "Excellent Learner": (1, 2)     # 1-2 minutes
}

# Maximum number of IDs per category
sample_size = 1000

# Initialize filtered categories
filtered_data = {category: [] for category in time_thresholds.keys()}

# Filter and limit entries
for category, entries in data.items():
    if category in time_thresholds:
        min_time, max_time = time_thresholds[category]
        # Filter entries by CombinedTimeMinutes
        valid_entries = [
            entry for entry in entries
            if all(
                min_time <= details["TotalReviewTime"]["CombinedTimeMinutes"] <= max_time
                for user_id, details in entry.items()
            )
        ]
        # Limit to the sample size
        if len(valid_entries) > sample_size:
            filtered_data[category] = random.sample(valid_entries, sample_size)
        else:
            filtered_data[category] = valid_entries

# Save the filtered data to a new JSON file
with open(output_path, "w") as file:
    json.dump(filtered_data, file, indent=4)

print(f"Filtered performance category data has been saved to {output_path}")
