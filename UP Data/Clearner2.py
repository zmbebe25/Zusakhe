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
convert_to_json('UP Data/Bachelor of Education (Intermediate Phase Teaching).txt', 'UP Data/Bachelor of Education (Intermediate Phase Teaching).json')
