import json
import pdfplumber

pdf_path = "C:/Users/Zusakhe Mbebe/Downloads/uj-undergraduate-prospectus-2024.pdf"
output_json_path = "C:/Users/Zusakhe Mbebe/course-data/Zusakhe/Auto-requirements/Page33.json"

# Open the PDF file
with pdfplumber.open(pdf_path) as pdf:
    # Access page 32
    page = pdf.pages[32]  # Note: Python is 0-indexed, so page 32 is accessed by index 31
    
    # Extract the table
    table = page.extract_table()
    
    # Convert the table to a list of dictionaries
    table_data = []
    for row in table:
        # Replace None values with an empty string
        row = ["" if cell is None else cell for cell in row]
        # Convert each row to a dictionary with column names as keys
        row_dict = dict(zip(range(len(row)), row))
        # Reverse specific fields
        keys_to_reverse = [1, 3, 4, 5, 6, 7]
        for key in keys_to_reverse:
            if key in row_dict:
                row_dict[key] = row_dict[key][::-1]  # Reverse the string
        table_data.append(row_dict)

# Write the extracted data into a JSON file
with open(output_json_path, "w") as json_file:
    json.dump(table_data, json_file, indent=4)

print("Extraction completed. Data saved in:", output_json_path)

import json

# Load the JSON file
with open('C:/Users/Zusakhe Mbebe/course-data/Zusakhe/Auto-requirements/Page33.json', 'r') as f:
    data = json.load(f)

# Define the key-value mapping for the changes
key_changes = {
    "0": "Qualification",
    "1": "Qualification Code",
    "2": "APS",
    "3": "English",
    "4": "First Additional Language",
    "5": "Mathematics",
    "6": "Mathematical Literacy",
    "7": "Technical Mathematics",
    "8": "Description"
}

# Iterate over the list and modify elements
for item in data:
    updated_item = {}
    for old_key, value in item.items():
        if old_key in key_changes:
            new_key = key_changes[old_key]
            updated_item[new_key] = value
        else:
            updated_item[old_key] = value
    item.clear()
    item.update(updated_item)

# Save the updated JSON back to the file
with open('C:/Users/Zusakhe Mbebe/course-data/Zusakhe/Auto-requirements/Page33(Final).json', 'w') as f:
    json.dump(data, f, indent=4)  # You can adjust the indent for formatting if needed

import re
import json

# Function to extract numeric values from string
def extract_numeric_value(s):
    numeric_value = re.search(r'(\d+)%', s)
    if numeric_value:
        return int(numeric_value.group(1))
    return None

# Read data from input file
input_file_path = 'C:/Users/Zusakhe Mbebe/course-data/Zusakhe/Auto-requirements/Page33(Final).json'
output_file_path = 'C:/Users/Zusakhe Mbebe/course-data/Zusakhe/Auto-requirements/Page33(Final1).json'

with open(input_file_path, 'r') as input_file:
    data = json.load(input_file)

# Process data to extract numeric values and replace '\n' with empty space
processed_data = []
for entry in data:
    processed_entry = entry.copy()
    processed_entry["English"] = extract_numeric_value(entry.get("English", "").replace('\n', ''))
    processed_entry["First Additional Language"] = extract_numeric_value(entry.get("First Additional Language", "").replace('\n', ''))
    processed_entry["Mathematics"] = extract_numeric_value(entry.get("Mathematics", "").replace('\n', ''))
    processed_entry["Mathematical Literacy"] = extract_numeric_value(entry.get("Mathematical Literacy", "").replace('\n', ''))
    processed_entry["Technical Mathematics"] = extract_numeric_value(entry.get("Technical Mathematics", "").replace('\n', ''))

    # Technical Mathematics remains the same
    processed_data.append(processed_entry)

# Write processed data to output file
with open(output_file_path, 'w') as output_file:
    json.dump(processed_data, output_file, indent=2)

import json

# Input and output file paths
input_file_path = 'Zusakhe/Auto-requirements/Page33(Final1).json'
output_file_path = 'Zusakhe/Auto-requirements/Page33(Final2).json'

# Read data from input file
with open(input_file_path, 'r') as input_file:
    data = json.load(input_file)

# Iterate over each entry in the data
for entry in data:
    # Extract APS value
    aps = entry["APS"]
    
    # Check if APS contains alphabetical characters
    if any(char.isalpha() for char in aps):
        # Reverse the last two digits of APS and convert to integer
        reversed_aps = int(aps[-1] + aps[-2])

        # Update APS value in the entry
        entry["APS"] = reversed_aps
    else:
        # Convert APS value to integer
        entry["APS"] = int(aps)

# Write modified data to output file
with open(output_file_path, 'w') as output_file:
    json.dump(data, output_file, indent=4)  # Adjust indent as needed

import json

# Input and output file paths
input_file_path = 'C:/Users/Zusakhe Mbebe/course-data/Zusakhe/Auto-requirements/Page33(Final2).json'
output_file_path = 'C:/Users/Zusakhe Mbebe/course-data/Zusakhe/Auto-requirements/Page33(Final3).json'

# Read input JSON
with open(input_file_path, 'r') as input_file:
    input_data = json.load(input_file)

# Iterate over each entry in the input JSON
output_data = []
for entry in input_data:
    # Extract subject-related fields and create a list of subject objects for each entry
    subjects = [
        {"English": entry["English"]},
        {"First Additional Language": entry["First Additional Language"]},
        {"Mathematics": entry["Mathematics"]},
        {"Mathematical Literacy": entry["Mathematical Literacy"]},
        {"Technical Mathematics": entry["Technical Mathematics"]}
    ]

    # Construct the entry with the "Subject" key
    entry_with_subject = {
        "Qualification": entry["Qualification"],
        "Qualification Code": entry["Qualification Code"],
        "APS": entry["APS"],
        "Description": entry["Description"],
        "9": entry["9"],
        "Subject": subjects
    }

    # Append the modified entry to the output data list
    output_data.append(entry_with_subject)

# Write the modified JSON to the output file
with open(output_file_path, 'w') as output_file:
    json.dump(output_data, output_file, indent=4)

print("Conversion completed. Output written to:", output_file_path)
