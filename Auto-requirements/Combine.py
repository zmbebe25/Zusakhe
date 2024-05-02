# Function to read the contents of a file
def read_file(filename):
    with open(filename, 'r') as file:
        return file.read()

# Combine contents of six files
def combine_files(file1, file2, file3, file4):
    combined_code = ''
    combined_code += read_file(file1) + '\n'
    combined_code += read_file(file2) + '\n'
    combined_code += read_file(file3) + '\n'
    combined_code += read_file(file4) + '\n'

    return combined_code

# Names of the files to be combined
file1 = 'UP Data/Extract.py'
file2 = 'UP Data/Cleaner1.py'
file3 = 'UP Data/Clearner2.py'
file4 = 'UP Data/Codes.py'



# Name of the file to save the combined code
combined_file = 'UP Data/UPMissingData.py'

# Combine the files
combined_code = combine_files(file1, file2, file3, file4)

# Write the combined code to a new file
with open(combined_file, 'w') as file:
    file.write(combined_code)

print(f"Combined code saved in {combined_file}")
