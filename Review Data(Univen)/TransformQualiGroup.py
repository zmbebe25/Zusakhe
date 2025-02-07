import json

# Define the input and output file paths
input_path = "C:/Users/zusakhe_gradesmatch/Downloads/MatchedQualificationGroup_WithCounts(2023).json"  # Replace with your input file path
output_path = "C:/Users/zusakhe_gradesmatch/Downloads/MatchedQualificationGroup_WithCounts(2023).json"  # Replace with your output file path

# Load JSON data
with open(input_path, "r", encoding="utf-8") as file:
    data = json.load(file)

# Initialize the groups
grouped_data = {
    "CombinedTimeMinutes < 1": [],
    "1 <= CombinedTimeMinutes < 7": [],
    "7 <= CombinedTimeMinutes < 20": [],
    "20 <= CombinedTimeMinutes < 40": [],
    "40 <= CombinedTimeMinutes < 60": [],
    "60 <= CombinedTimeMinutes < 80": [],
    "80 <= CombinedTimeMinutes < 100": [],
    "100 <= CombinedTimeMinutes < 180": [],
    "CombinedTimeMinutes >= 180": []
}

# Group users by CombinedTimeMinutes
for user in data:
    combined_time = user.get("TotalReviewTime", {}).get("CombinedTimeMinutes", 0)
    
    if combined_time < 1:
        grouped_data["CombinedTimeMinutes < 1"].append(user)
    elif 1 <= combined_time < 7:
        grouped_data["1 <= CombinedTimeMinutes < 7"].append(user)
    elif 7 <= combined_time < 20:
        grouped_data["7 <= CombinedTimeMinutes < 20"].append(user)
    elif 20 <= combined_time < 40:
        grouped_data["20 <= CombinedTimeMinutes < 40"].append(user)
    elif 40 <= combined_time < 60:
        grouped_data["40 <= CombinedTimeMinutes < 60"].append(user)
    elif 60 <= combined_time < 80:
        grouped_data["60 <= CombinedTimeMinutes < 80"].append(user)
    elif 80 <= combined_time < 100:
        grouped_data["80 <= CombinedTimeMinutes < 100"].append(user)
    elif 100 <= combined_time < 180:
        grouped_data["100 <= CombinedTimeMinutes < 180"].append(user)
    else:
        grouped_data["CombinedTimeMinutes >= 180"].append(user)

# Save the grouped data to a new JSON file
with open(output_path, "w", encoding="utf-8") as file:
    json.dump(grouped_data, file, indent=4)

print(f"Grouped data has been saved to {output_path}")
