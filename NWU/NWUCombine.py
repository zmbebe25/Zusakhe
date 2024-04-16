import os
import json

def combine_json_files(input_directory, output_file):
    combined_data = []

    # Iterate over all files in the directory
    for filename in os.listdir(input_directory):
        if filename.endswith('.json'):
            file_path = os.path.join(input_directory, filename)
            # Read the content of each JSON file
            with open(file_path, 'r') as file:
                data = json.load(file)
                combined_data.extend(data)

    # Write the combined data to a single JSON file
    with open(output_file, 'w') as outfile:
        json.dump(combined_data, outfile, indent=4)

# Input directory containing JSON files
input_directory = 'C:/Users/Zusakhe Mbebe/Downloads/Zusakhe/NWU'
# Output file path for combined JSON
output_file = 'C:/Users/Zusakhe Mbebe/Downloads/Zusakhe/NWUcombine.json'

combine_json_files(input_directory, output_file)
