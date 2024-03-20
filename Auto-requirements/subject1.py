import json

# Input and output file paths
input_file_path = 'Zusakhe/Auto-requirements/outputpage32(final3).json'
output_file_path = 'Zusakhe/Auto-requirements/outputpage32(final4).json'

# Read the input JSON file
with open(input_file_path, 'r') as input_file:
    provided_output = json.load(input_file)

# Transform the data according to the desired format
desired_output = []

for item in provided_output:
    desired_item = item.copy()
    subject_conditions = [
        {"English": item.get("English")},
        {"First Additional Language": item.get("First Additional Language")},
        ["OR",
            {"Mathematics": item.get("Mathematics")},
            {"Mathematical Literacy": item.get("Mathematical Literacy")},
            {"Technical Mathematics": item.get("Technical Mathematics")}
        ]
    ]
    # Remove entries with None values
    subject_conditions = [condition for condition in subject_conditions if all(condition.values())]
    desired_item["Subject"] = ["AND"] + subject_conditions
    desired_output.append(desired_item)

# Write the modified data to a new JSON file
with open(output_file_path, 'w') as output_file:
    json.dump(desired_output, output_file, indent=4)

print("Output file has been generated successfully.")
