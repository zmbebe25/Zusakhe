import json

# File paths
input_file = 'univen/Zuks/UnivenHealth.json'
output_file = 'univen/Zuks/UnivenHealth(final).json'

# Function to update the NQF value based on the Code
def update_nqf(data):
    for module in data:
        code = module["Code"]
        # Extract the first digit from the code
        digit_1 = next((char for char in code if char.isdigit()), None)
        if digit_1:
            digit_1 = int(digit_1)
            # Update NQF value based on the digit
            if digit_1 == 1:
                module['NQF'] = 5
            elif digit_1 == 2:
                module['NQF'] = 6
            elif digit_1 == 3:
                module['NQF'] = 7
            elif digit_1 == 4:
                module['NQF'] = 8
    return data

# Read the JSON data from the input file
with open(input_file, 'r') as file:
    data = json.load(file)

# Update the data
updated_data = update_nqf(data)

# Write the updated data back to the output file
with open(output_file, 'w') as file:
    json.dump(updated_data, file, indent=4)

print(f"The data has been successfully updated and saved to {output_file}.")
