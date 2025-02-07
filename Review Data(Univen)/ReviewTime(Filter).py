import json
from datetime import datetime

# Input and output file paths
input_data_path = "C:/Users/zusakhe_gradesmatch/Downloads/exported_data2(2023).json"
output_file = "C:/Users/zusakhe_gradesmatch/Downloads/ReviewTimesFinal(2023).json"

# Function to calculate time differences for each user and time frame
def calculate_review_time(data):
    user_results = {}

    for user_id, entries in data.items():
        results = {}
        total_time_seconds = 0

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
        total_combined_time = minutes + seconds / 60

        if 1 <= total_combined_time <= 7:
            user_results[user_id] = {
                "ReviewTimes": results,
                "TotalReviewTime": {
                    "Minutes": int(minutes),
                    "Seconds": seconds,
                    "CombinedTimeMinutes": total_combined_time
                }
            }

    return user_results

# Load data from the input file
with open(input_data_path, 'r') as file:
    data = json.load(file)

# Calculate the review times
user_review_times = calculate_review_time(data)

# Save the results to the output file
with open(output_file, 'w') as file:
    json.dump(user_review_times, file, indent=4)

# Print the results
print("Review Times by User and Time Frame:")
for user_id, review_data in user_review_times.items():
    print(f"UserID: {user_id}")
    for time_frame, seconds in review_data["ReviewTimes"].items():
        print(f"  {time_frame}: {seconds:.3f} seconds")
    total = review_data["TotalReviewTime"]
    print(f"  Total Review Time: {total['Minutes']} minutes and {total['Seconds']:.3f} seconds")
    print(f"  Combined Time in Minutes: {total['CombinedTimeMinutes']:.3f}\n")
