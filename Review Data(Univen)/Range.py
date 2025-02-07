import json
from datetime import datetime

# Input and output file paths
input_data_path = "C:/Users/zusakhe_gradesmatch/Downloads/cleaned_review_data(2024).json"
output_file = "C:/Users/zusakhe_gradesmatch/Downloads/cleaned_review_data1(2024).json"

# Function to calculate time differences for each time frame
def calculate_review_time(data):
    results = {}
    total_time_seconds = 0

    for user_id, entries in data.items():
        # Group by time frame (hour-level precision)
        grouped_by_hour = {}
        for entry in entries:
            created_time = datetime.fromisoformat(entry['CreatedTime'])
            time_frame = created_time.strftime('%Y-%m-%dT%H')
            if time_frame not in grouped_by_hour:
                grouped_by_hour[time_frame] = []
            grouped_by_hour[time_frame].append(created_time)

        # Calculate total time for each time frame
        for time_frame, times in grouped_by_hour.items():
            earliest = min(times)
            latest = max(times)
            total_seconds = (latest - earliest).total_seconds()
            results[time_frame] = total_seconds
            total_time_seconds += total_seconds

    # Convert total time to minutes and seconds
    minutes, seconds = divmod(total_time_seconds, 60)
    return results, minutes, seconds

# Load data from the input file
with open(input_data_path, 'r') as file:
    data = json.load(file)

# Calculate the review times
review_times, total_minutes, total_seconds = calculate_review_time(data)

# Save the results to the output file
output_data = {
    "ReviewTimes": review_times,
    "TotalReviewTime": {
        "Minutes": int(total_minutes),
        "Seconds": total_seconds
    }
}

with open(output_file, 'w') as file:
    json.dump(output_data, file, indent=4)

# Print the results
print("Review Times by Time Frame:")
for time_frame, seconds in review_times.items():
    print(f"{time_frame}: {seconds:.3f} seconds")

print("\nTotal Review Time:")
print(f"{int(total_minutes)} minutes and {total_seconds:.3f} seconds")
