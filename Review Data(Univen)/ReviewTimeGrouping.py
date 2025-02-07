import json

# Function to load JSON data from a file
def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

# Function to save JSON data to a file
def save_json(data, file_path):
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

# Function to group JSON data by CombinedTimeMinutes range and include counts
def group_by_combined_time(data):
    grouped_data = {
        "CombinedTimeMinutes < 1": {"count": 0, "entries": []},
        "1 <= CombinedTimeMinutes < 7": {"count": 0, "entries": []},
        "7 <= CombinedTimeMinutes < 20": {"count": 0, "entries": []},
        "20 <= CombinedTimeMinutes < 40": {"count": 0, "entries": []},
        "40 <= CombinedTimeMinutes < 60": {"count": 0, "entries": []},
        "60 <= CombinedTimeMinutes < 80": {"count": 0, "entries": []},
        "80 <= CombinedTimeMinutes < 100": {"count": 0, "entries": []},
        "100 <= CombinedTimeMinutes < 180": {"count": 0, "entries": []},
        "CombinedTimeMinutes >= 180": {"count": 0, "entries": []}
    }

    for entry in data:
        combined_time = entry["TotalReviewTime"]["CombinedTimeMinutes"]
        if combined_time < 1:
            grouped_data["CombinedTimeMinutes < 1"]["entries"].append(entry)
            grouped_data["CombinedTimeMinutes < 1"]["count"] += 1
        elif 1 <= combined_time < 7:
            grouped_data["1 <= CombinedTimeMinutes < 7"]["entries"].append(entry)
            grouped_data["1 <= CombinedTimeMinutes < 7"]["count"] += 1
        elif 7 <= combined_time < 20:
            grouped_data["7 <= CombinedTimeMinutes < 20"]["entries"].append(entry)
            grouped_data["7 <= CombinedTimeMinutes < 20"]["count"] += 1
        elif 20 <= combined_time < 40:
            grouped_data["20 <= CombinedTimeMinutes < 40"]["entries"].append(entry)
            grouped_data["20 <= CombinedTimeMinutes < 40"]["count"] += 1
        elif 40 <= combined_time < 60:
            grouped_data["40 <= CombinedTimeMinutes < 60"]["entries"].append(entry)
            grouped_data["40 <= CombinedTimeMinutes < 60"]["count"] += 1
        elif 60 <= combined_time < 80:
            grouped_data["60 <= CombinedTimeMinutes < 80"]["entries"].append(entry)
            grouped_data["60 <= CombinedTimeMinutes < 80"]["count"] += 1
        elif 80 <= combined_time < 100:
            grouped_data["80 <= CombinedTimeMinutes < 100"]["entries"].append(entry)
            grouped_data["80 <= CombinedTimeMinutes < 100"]["count"] += 1
        elif 100 <= combined_time < 180:
            grouped_data["100 <= CombinedTimeMinutes < 180"]["entries"].append(entry)
            grouped_data["100 <= CombinedTimeMinutes < 180"]["count"] += 1
        else:
            grouped_data["CombinedTimeMinutes >= 180"]["entries"].append(entry)
            grouped_data["CombinedTimeMinutes >= 180"]["count"] += 1

    return grouped_data

# Main function to process the JSON data
def process_json(input_path, output_path):
    # Load JSON data
    data = load_json(input_path)

    # Group the data
    grouped_data = group_by_combined_time(data)

    # Save the grouped data to the output path
    save_json(grouped_data, output_path)
    print(f"Grouped JSON with counts saved to {output_path}")

# Define input and output paths
input_path = "C:/Users/zusakhe_gradesmatch/Downloads/User_Review(Outliers)(2023).json"  # Replace with your input file path
output_path = "C:/Users/zusakhe_gradesmatch/Downloads/Grouped_User_Review_With_Counts(2023).json"  # Replace with your desired output file path

# Run the process
process_json(input_path, output_path)
