import pdfplumber

pdf_path = "C:/Users/Zusakhe Mbebe/Downloads/Faculty-EMS-Full (1).pdf"
output_path = 'C:/Users/Zusakhe Mbebe/Downloads/Zusakhe/UP Data/Faculty-EMS.txt'

def extract_text_from_pdf(pdf_path, output_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text()
    
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(text)

extract_text_from_pdf(pdf_path, output_path)

# Assuming 'data' is a list of lines read from a text file where each module's name appears right before the line that starts with 'Module credits'.

modules = []
with open('UP Data/Faculty-EMS.txt', 'r', encoding='utf-8') as file:
    data = file.readlines()

for i in range(1, len(data)):  # Start from 1 since we look back at i-1
    line = data[i].strip()
    if line.startswith('Qualification Undergraduate'):
        name = data[i-1].strip()  # Get the name from the previous line
        modules.append(name)

with open('UP Data/Faculty-EMS.txt', 'w', encoding='utf-8') as file:
    for module in modules:
        file.write(module + '\n')

print(modules)

import json
import re

def convert_to_json(input_file_path, output_file_path):
    modules = []
    
    with open(input_file_path, 'r') as file:
        for line in file:
            # Extracting module name and module code using regex
            match = re.match(r"(.+)\s\((.+)\)", line.strip())
            if match:
                module_name = match.group(1).strip()
                module_code = match.group(2).strip().replace(" ", "")  # Remove spaces in module_code
                modules.append({
                    "module_name": module_name,
                    "module_code": module_code
                })

    with open(output_file_path, 'w') as json_file:
        json.dump(modules, json_file, indent=4)

# Example usage
convert_to_json('C:/Users/Zusakhe Mbebe/Downloads/Zusakhe/UP Data/Faculty-EMS.txt', 'C:/Users/Zusakhe Mbebe/Downloads/Zusakhe/UP Data/Faculty-EMS.json')

import json

# Function to load JSON data from a file, specifying the encoding
def load_json_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        return json.load(file)

# Load data from files
json_data1 = load_json_file('UP Data/Faculty-EMS.json')
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
with open('UP Data/Faculty-EMSresult_codes.json', 'w', encoding='utf-8') as file:
    json.dump(result_dict, file, ensure_ascii=False, indent=4)

print("Result dictionary saved to 'result_codes.json'.")

