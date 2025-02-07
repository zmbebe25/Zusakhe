import json

# Define input and output paths
json1_path = "C:/Users/zusakhe_gradesmatch/Downloads/User_Review(Outliers)(2023).json"
json2_path = "C:/Users/zusakhe_gradesmatch/Downloads/gradesmatch_reference.qualificationgroup.json"
output_path = "C:/Users/zusakhe_gradesmatch/Downloads/QualificationGroup(2023).json"

# Function to load JSON data from a file
def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

# Function to save JSON data to a file
def save_json(data, file_path):
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

# Function to find the qualification group
def find_qualification_group(qualification, qualification_mapping):
    if qualification is None:
        return None  # Return None if qualification is None
    for key, keywords in qualification_mapping.items():
        if qualification in keywords:
            return key
    return qualification

# Main function to process the JSON data
def process_json(json1_path, json2_path, output_path):
    # Load JSON data
    data1 = load_json(json1_path)
    data2 = load_json(json2_path)

    # Create a mapping from JSON 2
    qualification_mapping = {item['Name']: item['KeyWords'] for item in data2}

    # Update JSON 1
    for entry in data1:
        # Update ChosenQualifications
        for qual in entry.get("ChosenQualifications", []):
            if "Qualification" in qual:  # Check if "Qualification" key exists
                qual["QualificationGroup"] = find_qualification_group(qual.get("Qualification"), qualification_mapping)
        
        # Update PreferredQualifications
        for qual in entry.get("PreferredQualifications", []):
            if "Name" in qual:  # Check if "Name" key exists
                qual["QualificationGroup"] = find_qualification_group(qual.get("Name"), qualification_mapping)

    # Save the updated JSON 1 to the output path
    save_json(data1, output_path)
    print(f"Updated JSON saved to {output_path}")

# Run the process
process_json(json1_path, json2_path, output_path)