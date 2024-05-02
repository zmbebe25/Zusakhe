import json

# Function to load JSON data from a file, specifying the encoding
def load_json_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        return json.load(file)

# Load data from files
json_data1 = load_json_file('UP Data/Faculty-VET.json')
json_data2 = load_json_file('UP Data/UPcourse data.json')

# Extract the list of codes from the second file
codes_in_second_file = {course['Code'] for course in json_data2}

# Initialize dictionaries to store codes that exist and do not exist
codes_exist = []
codes_do_not_exist = []

# Check for each code in the first file if it exists in the second file
for course in json_data1:
    if course['Code'] in codes_in_second_file:
        codes_exist.append(course['Code'])
    else:
        codes_do_not_exist.append(course['Code'])

# Group results into a dictionary
result_dict = {
    "exist_in_json_data2": codes_exist,
    "do_not_exist_in_json_data2": codes_do_not_exist
}

# Save the result dictionary to a new JSON file
with open('UP Data/Faculty-VETresult_codes.json', 'w', encoding='utf-8') as file:
    json.dump(result_dict, file, ensure_ascii=False, indent=4)

print("Result dictionary saved to 'result_codes.json'.")
