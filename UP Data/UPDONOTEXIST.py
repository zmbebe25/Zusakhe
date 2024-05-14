import json

# Load the JSON data from files
with open('UP Data/Faculty-SCIresult_codes.json', 'r') as file:
    json_data1 = json.load(file)

with open('UP Data/Faculty-SCI.json', 'r') as file:
    json_data2 = json.load(file)

# Create a dictionary to store the mappings of codes to names
code_to_name = {}

# Populate the dictionary from the second JSON file
for item in json_data2:
    code_to_name[item['Code']] = item['Name']

# List to store the JSON objects
output_list = []

# Iterate through the "do_not_exist_in_json_data2" list in the first JSON file
for code in json_data1['do_not_exist_in_json_data2']:
    # If the code is found in the dictionary, create a JSON object with Name and Code populated
    if code in code_to_name:
        obj = {
            "Name": code_to_name[code],
            "Code": code,
            "Credit": "TO BE UPDATED",
            "NQF": "TO BE UPDATED",
            "Prerequisite": {
                "Comment": "TO BE UPDATED."
            },
            "Duration": "Semester",
            "Period": [1],
            "Description": "TO BE UPDATED",
            "Institution": "University of Pretoria"
        }
        output_list.append(obj)

# Save the output list as a JSON file
with open('UP Data/UPoutput.json', 'w') as outfile:
    json.dump(output_list, outfile, indent=4)
