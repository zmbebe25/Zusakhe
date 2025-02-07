import json

# Define input and output paths
json1_path = "C:/Users/zusakhe_gradesmatch/Downloads/gradesmatch_core.user(User2024).json"
json2_path = "C:/Users/zusakhe_gradesmatch/Downloads/Filtered_Performance_Category_Outliers(2024).json"
output_path = "C:/Users/zusakhe_gradesmatch/Downloads/User_Review(Outliers)(2024).json"

# Load JSON data from files
with open(json1_path, 'r') as file1, open(json2_path, 'r') as file2:
    json1_data = json.load(file1)
    json2_data = json.load(file2)

# Initialize merged data
merged_data = []

# Process json1
for user_entry in json1_data:
    user_id = user_entry["_id"]["$oid"]  # Extract the $oid as the user ID

    # Check if the user exists in json2
    if user_id in json2_data:
        # Add ReviewTimes and TotalReviewTime from json2
        review_data = json2_data[user_id]
        user_entry["ReviewTimes"] = review_data.get("ReviewTimes", {})
        user_entry["TotalReviewTime"] = review_data.get("TotalReviewTime", {})
        # Append enriched user entry to merged_data
        merged_data.append(user_entry)

# Write the result to the output file
with open(output_path, "w") as output_file:
    json.dump(merged_data, output_file, indent=2)

print(f"Merged data has been successfully saved to {output_path}")
