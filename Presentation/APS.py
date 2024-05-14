
import json

# Input and output file paths
input_file_path = 'Presentation/output4.json'
output_file_path = 'Presentation/output5Auto-requirements/subject1.pyAuto-requirements/subject1.py.json'

# Function to reverse integer pairs and choose the largest pair
def reverse_and_choose_largest_pair(aps):
    # Split the string by whitespace to get pairs
    pairs = aps.split()
    reversed_pairs = []
    for pair in pairs:
        # Remove non-numeric characters from pair
        pair = ''.join(filter(str.isdigit, pair))
        if pair:  # Check if pair is not empty
            # Reverse the pair and append to the reversed_pairs list
            reversed_pair = pair[::-1]
            reversed_pairs.append(reversed_pair)
    if reversed_pairs:  # Check if there are reversed pairs
        # Sort the pairs in descending order based on the first number of each pair
        sorted_pairs = sorted(reversed_pairs, key=lambda x: int(x), reverse=True)
        # Choose the largest pair
        largest_pair = sorted_pairs[0]
        return largest_pair
    else:
        return '0'  # Return '0' if there are no valid pairs

# Read data from input file
with open(input_file_path, 'r') as input_file:
    data = json.load(input_file)

# Iterate over each entry in the data
for entry in data:
    # Extract APS value
    aps = entry["APS"]
    
    # Check if APS contains alphabetical characters
    if any(char.isalpha() for char in aps):
        # Reverse the integer pairs and choose the largest pair
        largest_pair = reverse_and_choose_largest_pair(aps)
        # Convert the largest pair to an integer
        largest_pair = int(largest_pair)
        # Update APS value in the entry
        entry["APS"] = largest_pair
    else:
        # Convert APS value to integer
        entry["APS"] = int(aps)

# Write modified data to output file
with open(output_file_path, 'w') as output_file:
    json.dump(data, output_file, indent=4)  # Adjust indent as needed