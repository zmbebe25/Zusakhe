import json

# Define input and output file paths
input_path = "C:/Users/zusakhe_gradesmatch/Downloads/ReviewTimes(2023).json"
output_path = "c:/Users/zusakhe_gradesmatch/Downloads/Filtered_Performance_Category_Outliers(2023).json"

# Load the JSON data from the input file
with open(input_path, 'r') as file:
    data = json.load(file)

# Initialize an empty dictionary to store the filtered results
filtered_data = {}

# Iterate through each entry in the JSON data
for user_id, user_data in data.items():
    combined_time_minutes = user_data['TotalReviewTime']['CombinedTimeMinutes']
    
    # Print the CombinedTimeMinutes for debugging
    print(f"User ID: {user_id}, CombinedTimeMinutes: {combined_time_minutes}")
    
    # Check if CombinedTimeMinutes is less than 1 or greater than 7
    if combined_time_minutes < 1 or combined_time_minutes > 7:
        filtered_data[user_id] = user_data

# Save the filtered dictionary to the output file
with open(output_path, 'w') as file:
    json.dump(filtered_data, file, indent=4)

print(f"Filtered data saved to {output_path}")