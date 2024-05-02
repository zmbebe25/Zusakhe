import json
import os
from hashlib import md5

def hash_dict(d):
    """Create a hash for a dictionary."""
    d_hash = md5(json.dumps(d, sort_keys=True).encode('utf-8')).hexdigest()
    return d_hash

def combine_json_files(folder_path, output_file):
    """Combine JSON files from a folder into one file, removing duplicates."""
    json_objects = {}
    files = [f for f in os.listdir(folder_path) if f.endswith('.json')]
    
    # Read each file and add its contents to json_objects if not already present
    for file_name in files:
        with open(os.path.join(folder_path, file_name), 'r') as file:
            data = json.load(file)
            for entry in data:
                entry_hash = hash_dict(entry)
                if entry_hash not in json_objects:
                    json_objects[entry_hash] = entry

    # Write the unique JSON objects to the output file
    with open(output_file, 'w') as file:
        json.dump(list(json_objects.values()), file, indent=4)

    print(f'Combined JSON written to {output_file}')

# Example usage
folder_path = 'C:/Users/Zusakhe Mbebe/course-data/univen/descriptions24'
output_file = 'Univencombined_output.json'
combine_json_files(folder_path, output_file)
