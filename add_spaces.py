import json

path = 'C:\\Users\\Bheki Lushaba\\course-data\\uj\\descreptions25\\fada.json'
with open(path, 'r') as json_file:
    data = json.load(json_file)

    for item in data:  # Assuming 'data' is a list of dictionaries
        if 'Description' in item:  # Check if 'Description' key exists
            description = item['Description']
            # Split the description into words
            words = description.split()
            # Insert '\n' after every 10th word
            for i in range(15, len(words), 16):  # Start at 10, step by 11 to account for newly added '\n'
                words.insert(i, '\n')
            # Reconstruct the description
            modified_description = ' '.join(words)
            # Update the item with the modified description
            item['Description'] = modified_description


with open(path, 'w') as file:
    json.dump(data, file, indent=2)