import json

# Input and output file paths
input_file_path = 'Zusakhe/Auto-requirements/Page67(Final2).json'
output_file_path = 'Zusakhe/Auto-requirements/Page67(Final3).json'

# Read input JSON
with open(input_file_path, 'r') as input_file:
    input_data = json.load(input_file)

# Iterate over each entry in the input JSON
output_data = []
for entry in input_data:
    # Extract subject-related fields and create a list of subject objects for each entry
    subjects = [
        {"English": entry["English"]},
        {"Mathematics": entry["Mathematics"]},
        {"Physical Sciences": entry["Physical Sciences"]},
        {"Life Sciences": entry["Life Sciences"]},
        {"Technical Mathematics": entry["Technical Mathematics"]},
        {"Technical Science": entry["Technical Science"]}
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
