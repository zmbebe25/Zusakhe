import json
from collections import defaultdict

# Function to load JSON data from a file
def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

# Function to save JSON data to a file
def save_json(data, file_path):
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

# Function to count school occurrences by category
def count_schools_by_category(data):
    school_counts = {}

    # Iterate through categories and count school names
    for category, details in data.items():
        if category not in school_counts:
            school_counts[category] = {"Schools": defaultdict(int)}  # Initialize dynamically

        for entry in details["entries"]:
            school_name = entry.get("School", "Unknown")
            if school_name:  # Ensure school name is valid
                school_counts[category]["Schools"][school_name] += 1

    # Convert defaultdicts to regular dicts for JSON serialization
    for category in school_counts:
        school_counts[category]["Schools"] = dict(school_counts[category]["Schools"])

    return school_counts

# Main function
def process_json(input_path, output_path):
    # Load input JSON
    data = load_json(input_path)

    # Count schools by category
    school_counts = count_schools_by_category(data)

    # Save the results to the output path
    save_json(school_counts, output_path)
    print(f"School counts have been saved to {output_path}")

# Define input and output paths
input_path = "C:/Users/zusakhe_gradesmatch/Downloads/Grouped_User_Review_With_Counts(2024).json"  # Replace with your input file path
output_path = "C:/Users/zusakhe_gradesmatch/Downloads/School_Counts_By_Category(2024).json"  # Replace with your desired output file path

# Run the process
process_json(input_path, output_path)
