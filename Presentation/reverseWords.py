import json

def reverse_words(description):
    # Split the description into words
    words = description.split()
    # Reverse each word and join them back together
    reversed_description = ' '.join(word[::-1] for word in words)
    return reversed_description

# Load the JSON data
with open('C:/Users/Zusakhe Mbebe/course-data/Zusakhe/Auto-requirements/Page86(Final3).json', 'r') as file:
    data = json.load(file)

# Iterate through each object in the JSON array
for obj in data:
    # Reverse the words in the 'Description' key
    obj['Description'] = reverse_words(obj['Description'])

# Save the modified JSON data
with open('C:/Users/Zusakhe Mbebe/course-data/Zusakhe/Auto-requirements/Page86(Final4).json', 'w') as file:
    json.dump(data, file, indent=4)
