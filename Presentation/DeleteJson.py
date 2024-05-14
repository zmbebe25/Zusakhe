import json

# Function to check if a dictionary is fully populated
def is_fully_populated(dictionary):
    for value in dictionary.values():
        if not value:
            return False
    return True

# Input and output file paths
input_file_path = 'Presentation/output1.json'
output_file_path = 'Presentation/output2.json'

# Read data from input file
with open(input_file_path, 'r') as input_file:
    data = json.load(input_file)

# Filter out dictionaries that are not fully populated
filtered_data = [d for d in data if is_fully_populated(d)]

# Write the filtered data to the output file
with open(output_file_path, 'w') as output_file:
    json.dump(filtered_data, output_file, indent=4)

print("Filtered data has been written to:", output_file_path)
