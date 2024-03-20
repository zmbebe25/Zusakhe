import json

# Load the JSON file
with open('C:/Users/Zusakhe Mbebe/course-data/Zusakhe/Auto-requirements/Page67(DeleteFinal).json', 'r') as f:
    data = json.load(f)

# Define the key-value mapping for the changes
key_changes = {
    "0": "Qualification",
    "1": "Qualification Code",
    "2": "APS",
    "3": "English",
    "4": "Mathematics",
    "5": "Mathematics Literacy",
    "6": "Physical Sciences",
    "7": "OR",
    "8": "Life Sciences",
    "9": "Technical Mathematics",
    "10": "Technical Science",
    "11": "Description",
    "12": "CAMPUS",
}

# Iterate over the list and modify elements
for item in data:
    updated_item = {}
    for old_key, value in item.items():
        if old_key in key_changes:
            new_key = key_changes[old_key]
            updated_item[new_key] = value
        else:
            updated_item[old_key] = value
    item.clear()
    item.update(updated_item)

# Save the updated JSON back to the file
with open('C:/Users/Zusakhe Mbebe/course-data/Zusakhe/Auto-requirements/Page67(Final).json', 'w') as f:
    json.dump(data, f, indent=4)  # You can adjust the indent for formatting if needed
