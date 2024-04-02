import json

# Paths to the input files and the output file
course_data_file = 'univen/Zuks/UnivenHealth(final).json'
desc_prereq_file = 'univen/Zuks/UnivenAddData.json' # Update this path
output_file = 'univen/Zuks/UnivenHealth(final1).json'

# Load JSON data from a file
def load_json_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Save JSON data to a file
def save_json_data(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

# Main function to merge course data with descriptions and prerequisites
def merge_course_data(course_file, desc_prereq_file, output_file):
    # Load the course data and the description/prerequisites data
    courses = load_json_data(course_file)
    desc_prereqs = load_json_data(desc_prereq_file)['courses']

    # Create a dictionary for quick lookup of descriptions and prerequisites by course code
    desc_prereqs_dict = {course['Code']: course for course in desc_prereqs}

    # Iterate over the courses to append the description and prerequisites
    for course in courses:
        course_code = course['Code']
        if course_code in desc_prereqs_dict:
            course['Description'] = desc_prereqs_dict[course_code].get('Description', '')
            course['prerequisites'] = desc_prereqs_dict[course_code].get('prerequisites', [])
    
    # Save the merged data to the output file
    save_json_data(courses, output_file)
    print(f"Data has been processed and saved to {output_file}")

# Call the main function
merge_course_data(course_data_file, desc_prereq_file, output_file)
