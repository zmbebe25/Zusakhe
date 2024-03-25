import json

input_json_path = "C:/Users/Zusakhe Mbebe/Downloads/Zusakhe/Auto-requirements/Univen_page13.json"
output_json_path = "C:/Users/Zusakhe Mbebe/Downloads/Zusakhe/Auto-requirements/Univen_page13(final).json"

# Function to extract APS value from Description
def extract_aps(description):
    try:
        aps_index = description.index("NSC") + 4
        aps_value = int(description[aps_index:].split()[0])
        return aps_value
    except ValueError:
        return None

# Read JSON data from input file
with open(input_json_path, 'r') as file:
    data = json.load(file)

# Add APS key to each qualification object
for qualification in data:
    if "Description" in qualification:
        aps_value = extract_aps(qualification["Description"])
        if aps_value is not None:
            qualification["APS"] = aps_value

# Write the updated JSON data to output file
with open(output_json_path, 'w') as file:
    json.dump(data, file, indent=4)

print("Updated JSON data has been written to:", output_json_path)
