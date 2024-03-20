import os
import json

# Input and output folder paths
input_folder_path = 'C:/Users/Zusakhe Mbebe/course-data/Zusakhe/Auto-requirements'
output_folder_path = 'C:/Users/Zusakhe Mbebe/course-data/Zusakhe/Auto-requirements'

# Ensure the output folder exists, create if not
if not os.path.exists(output_folder_path):
    os.makedirs(output_folder_path)

# Iterate through all files in the input folder
for filename in os.listdir(input_folder_path):
    # Check if the file is a JSON file
    if filename.endswith('.json'):
        # Construct input and output file paths for each file
        input_file_path = os.path.join(input_folder_path, filename)
        output_file_path = os.path.join(output_folder_path, filename)

        # Read data from the input JSON file
        with open(input_file_path, 'r') as input_file:
            data = json.load(input_file)

        # Perform the splitting operation on the data
        for entry in data:
            if "Subject" in entry:
                new_subjects = []
                for sub_dict in entry["Subject"]:
                    for key, value in sub_dict.items():
                        if "/" in key:
                            keys = key.split("/")
                            for split_key in keys:
                                new_subjects.append({split_key: value})
                        else:
                            new_subjects.append({key: value})
                entry["Subject"] = new_subjects

        # Write the modified data to the output JSON file
        with open(output_file_path, 'w') as output_file:
            json.dump(data, output_file, indent=4)

        print(f"Splitting operation completed. Data saved to {output_file_path}")
