import os
import json

def combine_json_files(folder_path, output_file):
    combined_data = []
    
    # Iterate through each file in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r') as file:
                # Load JSON data from the file
                data = json.load(file)
                # Append data to the combined list
                combined_data.append(data)
    
    # Write the combined data to the output file
    with open(output_file, 'w') as outfile:
        json.dump(combined_data, outfile, indent=4)

# Example usage:
folder_path = r'C:\Users\Zusakhe Mbebe\course-data\Zusakhe\Auto-requirements_updated'
output_file = r'C:\Users\Zusakhe Mbebe\course-data\Zusakhe\Auto-requirements_updated\combined_data.json'

combine_json_files(folder_path, output_file)
