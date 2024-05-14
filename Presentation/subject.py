import json

# Input and output file paths
input_file_path = 'Presentation/output5.json'
output_file_path = 'Presentation/output6.json'

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
        {"Mathematics Literacy": entry["Mathematics Literacy"]},
        {"Technical Mathematics": entry["Technical Mathematics"]},
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
