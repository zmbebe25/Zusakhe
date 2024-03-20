import json

def flip_description(description):
    words = description.split()
    flipped_description = ' '.join(reversed(words))
    return flipped_description

input_file_path = 'C:/Users/Zusakhe Mbebe/course-data/Zusakhe/Auto-requirements/Page86(Final4).json'
output_file_path = 'C:/Users/Zusakhe Mbebe/course-data/Zusakhe/Auto-requirements/Page86(Final5).json'

with open(input_file_path, 'r') as input_file:
    data = json.load(input_file)

for item in data:
    original_description = item.get("Description", "")
    flipped_description = flip_description(original_description)
    item["Description"] = flipped_description

with open(output_file_path, 'w') as output_file:
    json.dump(data, output_file, indent=4)
