import json

# The path to the input JSON file.
input_path = 'C:\\Users\\Bheki Lushaba\\course-data\\up\\descriptions24\\descriptions.json'
# The path to the output JSON file.
output_path = 'C:\\Users\\Bheki Lushaba\\course-data\\up\\descriptions24\\descriptions.json'

# Open the input JSON file for reading.
with open(input_path, 'r') as json_file:
    data = json.load(json_file)

    # Iterate through the items in the JSON data.
    for item in data:
        prerequisite = item.get('Prerequisite', [])

        # Check if the length of the 'Prerequisite' field is greater than 1.
        if len(prerequisite) > 1:
            # Modify the 'Prerequisite' field as per the requirement.
            item['Prerequisite'] = [{"$and": prerequisite}]

# Open the output JSON file for writing.
with open(output_path, 'w') as file2:
    # Write the modified data to the output file in a pretty format.
    json.dump(data, file2, indent=2)
