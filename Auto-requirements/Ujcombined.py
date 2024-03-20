import json
import pdfplumber

pdf_path = "C:/Users/Zusakhe Mbebe/Downloads/uj-undergraduate-prospectus-2024.pdf"
output_json_path = "C:/Users/Zusakhe Mbebe/course-data/Zusakhe/Auto-requirements/Page95.json"

# Open the PDF file
with pdfplumber.open(pdf_path) as pdf:
    page = pdf.pages[94]  # Note: Python is 0-indexed, so page 32 is accessed by index 31
    
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
        keys_to_reverse = [3,4,5,6]
        for key in keys_to_reverse:
            if key in row_dict:
                row_dict[key] = row_dict[key][::-1]  # Reverse the string
        table_data.append(row_dict)

# Write the extracted data into a JSON file
with open(output_json_path, "w") as json_file:
    json.dump(table_data, json_file, indent=4)

print("Extraction completed. Data saved in:", output_json_path)

import json

# Function to check if a dictionary is fully populated
def is_fully_populated(dictionary):
    for value in dictionary.values():
        if not value:
            return False
    return True

# Input and output file paths
input_file_path = 'C:/Users/Zusakhe Mbebe/course-data/Zusakhe/Auto-requirements/Page95.json'
output_file_path = 'C:/Users/Zusakhe Mbebe/course-data/Zusakhe/Auto-requirements/Page95(DeleteFinal).json'

# Read data from input file
with open(input_file_path, 'r') as input_file:
    data = json.load(input_file)

# Filter out dictionaries that are not fully populated
filtered_data = [d for d in data if is_fully_populated(d)]

# Write the filtered data to the output file
with open(output_file_path, 'w') as output_file:
    json.dump(filtered_data, output_file, indent=4)

print("Filtered data has been written to:", output_file_path)

import json

# Load the JSON file
with open('C:/Users/Zusakhe Mbebe/course-data/Zusakhe/Auto-requirements/Page95(DeleteFinal).json', 'r') as f:
    data = json.load(f)

# Define the key-value mapping for the changes
key_changes = {
   "0": "Qualification",
    "1": "Qualification Code",
    "2": "APS",
    "3": "English",
    "4": "Mathematics/ Technical Mathematics",
    "5": "Physical Science",
    "6": "Life Science",
    "7": "Description",
    "8": "CAMPUS",
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
with open('C:/Users/Zusakhe Mbebe/course-data/Zusakhe/Auto-requirements/Page95(Final).json', 'w') as f:
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
input_file_path = 'C:/Users/Zusakhe Mbebe/course-data/Zusakhe/Auto-requirements/Page95(Final).json'
output_file_path = 'C:/Users/Zusakhe Mbebe/course-data/Zusakhe/Auto-requirements/Page95(Final1).json'

with open(input_file_path, 'r') as input_file:
    data = json.load(input_file)

# Process data to extract numeric values and replace '\n' with empty space
processed_data = []
for entry in data:
    processed_entry = entry.copy()
    processed_entry["English"] = extract_numeric_value(entry.get("English", "").replace('\n', ''))
    processed_entry["Mathematics/ Technical Mathematics"] = extract_numeric_value(entry.get("Mathematics/ Technical Mathematics", "").replace('\n', ''))
    processed_entry["Physical Science"] = extract_numeric_value(entry.get("Physical Science", "").replace('\n', ''))
    processed_entry["Life Science"] = extract_numeric_value(entry.get("Life Science", "").replace('\n', ''))




    

   




    # Technical Mathematics remains the same
    processed_data.append(processed_entry)

# Write processed data to output file
with open(output_file_path, 'w') as output_file:
    json.dump(processed_data, output_file, indent=2)

import json

# Input and output file paths
input_file_path = 'Zusakhe/Auto-requirements/Page95(Final1).json'
output_file_path = 'Zusakhe/Auto-requirements/Page95(Final2).json'

# Function to reverse integer pairs and choose the largest pair
def reverse_and_choose_largest_pair(aps):
    # Split the string by whitespace to get pairs
    pairs = aps.split()
    reversed_pairs = []
    for pair in pairs:
        # Remove non-numeric characters from pair
        pair = ''.join(filter(str.isdigit, pair))
        if pair:  # Check if pair is not empty
            # Reverse the pair and append to the reversed_pairs list
            reversed_pair = pair[::-1]
            reversed_pairs.append(reversed_pair)
    if reversed_pairs:  # Check if there are reversed pairs
        # Sort the pairs in descending order based on the first number of each pair
        sorted_pairs = sorted(reversed_pairs, key=lambda x: int(x), reverse=True)
        # Choose the largest pair
        largest_pair = sorted_pairs[0]
        return largest_pair
    else:
        return '0'  # Return '0' if there are no valid pairs

# Read data from input file
with open(input_file_path, 'r') as input_file:
    data = json.load(input_file)

# Iterate over each entry in the data
for entry in data:
    # Extract APS value
    aps = entry["APS"]
    
    # Check if APS contains alphabetical characters
    if any(char.isalpha() for char in aps):
        # Reverse the integer pairs and choose the largest pair
        largest_pair = reverse_and_choose_largest_pair(aps)
        # Convert the largest pair to an integer
        largest_pair = int(largest_pair)
        # Update APS value in the entry
        entry["APS"] = largest_pair
    else:
        # Convert APS value to integer
        entry["APS"] = int(aps)

# Write modified data to output file
with open(output_file_path, 'w') as output_file:
    json.dump(data, output_file, indent=4)  # Adjust indent as needed

import json

# Input and output file paths
input_file_path = 'Zusakhe/Auto-requirements/Page95(Final2).json'
output_file_path = 'Zusakhe/Auto-requirements/Page95(Final3).json'

# Read input JSON
with open(input_file_path, 'r') as input_file:
    input_data = json.load(input_file)

# Iterate over each entry in the input JSON
output_data = []
for entry in input_data:
    # Extract subject-related fields and create a list of subject objects for each entry
    subjects = [
        {"English": entry["English"]},
        {"Mathematics/ Technical Mathematics": entry["Mathematics/ Technical Mathematics"]},
        {"Physical Science": entry["Physical Science"]},
        {"Life Science": entry["Life Science"]},



        
 
  

        
        
        
    ]

    # Construct the entry with the "Subject" key
    entry_with_subject = {
        "Qualification": entry["Qualification"],
        "Qualification Code": entry["Qualification Code"],
        "APS": entry["APS"],
        "Description": entry["Description"],
        "Subject": subjects
    }

    # Append the modified entry to the output data list
    output_data.append(entry_with_subject)

# Write the modified JSON to the output file
with open(output_file_path, 'w') as output_file:
    json.dump(output_data, output_file, indent=4)

print("Conversion completed. Output written to:", output_file_path)

import json

def reverse_words(description):
    # Split the description into words
    words = description.split()
    # Reverse each word and join them back together
    reversed_description = ' '.join(word[::-1] for word in words)
    return reversed_description

# Load the JSON data
with open('C:/Users/Zusakhe Mbebe/course-data/Zusakhe/Auto-requirements/Page95(Final3).json', 'r') as file:
    data = json.load(file)

# Iterate through each object in the JSON array
for obj in data:
    # Reverse the words in the 'Description' key
    obj['Qualification Code'] = reverse_words(obj['Qualification Code'])

# Save the modified JSON data
with open('C:/Users/Zusakhe Mbebe/course-data/Zusakhe/Auto-requirements/Page95(Final4).json', 'w') as file:
    json.dump(data, file, indent=4)

import json

def flip_description(description):
    words = description.split()
    flipped_description = ' '.join(reversed(words))
    return flipped_description

input_file_path = 'C:/Users/Zusakhe Mbebe/course-data/Zusakhe/Auto-requirements/Page95(Final4).json'
output_file_path = 'C:/Users/Zusakhe Mbebe/course-data/Zusakhe/Auto-requirements/Page95(Final5).json'

with open(input_file_path, 'r') as input_file:
    data = json.load(input_file)

for item in data:
    original_description = item.get("Qualification Code", "")
    flipped_description = flip_description(original_description)
    item["Qualification Code"] = flipped_description

with open(output_file_path, 'w') as output_file:
    json.dump(data, output_file, indent=4)
