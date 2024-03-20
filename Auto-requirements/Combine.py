# Function to read the contents of a file
def read_file(filename):
    with open(filename, 'r') as file:
        return file.read()

# Combine contents of six files
def combine_files(file1, file2, file3, file4, file5, file6, file7, file8):
    combined_code = ''
    combined_code += read_file(file1) + '\n'
    combined_code += read_file(file2) + '\n'
    combined_code += read_file(file3) + '\n'
    combined_code += read_file(file4) + '\n'
    combined_code += read_file(file5) + '\n'
    combined_code += read_file(file6) + '\n'
    combined_code += read_file(file7) + '\n'
    combined_code += read_file(file8)
    return combined_code

# Names of the files to be combined
file1 = 'C:/Users/Zusakhe Mbebe/course-data/Zusakhe/Auto-requirements/Uj.py'
file2 = 'C:/Users/Zusakhe Mbebe/course-data/Zusakhe/Auto-requirements/DeleteJson.py'
file3 = 'C:/Users/Zusakhe Mbebe/course-data/Zusakhe/Auto-requirements/Keys.py'
file4 = 'C:/Users/Zusakhe Mbebe/course-data/Zusakhe/Auto-requirements/Marks.py'
file5 = 'C:/Users/Zusakhe Mbebe/course-data/Zusakhe/Auto-requirements/APS.py'
file6 = 'C:/Users/Zusakhe Mbebe/course-data/Zusakhe/Auto-requirements/subject.py'
file7 = 'C:/Users/Zusakhe Mbebe/course-data/Zusakhe/Auto-requirements/reverseWords.py'
file8 = 'C:/Users/Zusakhe Mbebe/course-data/Zusakhe/Auto-requirements/ReverseDescription.py'


# Name of the file to save the combined code
combined_file = 'C:/Users/Zusakhe Mbebe/course-data/Zusakhe/Auto-requirements/Ujcombined.py'

# Combine the files
combined_code = combine_files(file1, file2, file3, file4, file5, file6, file7, file8)

# Write the combined code to a new file
with open(combined_file, 'w') as file:
    file.write(combined_code)

print(f"Combined code saved in {combined_file}")
