import re
import json

# Function to extract numeric values from string
def extract_numeric_value(s):
    numeric_value = re.search(r'(\d+)%', s)
    if numeric_value:
        return int(numeric_value.group(1))
    return None

# Read data from input file
input_file_path = 'Presentation/output3.json'
output_file_path = 'Presentation/output4.json'

with open(input_file_path, 'r') as input_file:
    data = json.load(input_file)

# Process data to extract numeric values and replace '\n' with empty space
processed_data = []
for entry in data:
    processed_entry = entry.copy()
    processed_entry["English"] = extract_numeric_value(entry.get("English", "").replace('\n', ''))
    processed_entry["Mathematics"] = extract_numeric_value(entry.get("Mathematics", "").replace('\n', ''))
    processed_entry["Mathematics Literacy"] = extract_numeric_value(entry.get("Physical Sciences", "").replace('\n', ''))
    processed_entry["Technical Mathematics"] = extract_numeric_value(entry.get("Technical Mathematics", "").replace('\n', ''))

    # Technical Mathematics remains the same
    processed_data.append(processed_entry)

# Write processed data to output file
with open(output_file_path, 'w') as output_file:
    json.dump(processed_data, output_file, indent=2)
