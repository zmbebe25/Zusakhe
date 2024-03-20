import os
import json

def convert_input(input_data):
    output = []
    for index, item in enumerate(input_data):
        qualification = item["Qualification"]
        qualification_code = item["Qualification Code"]
        aps = item["APS"]
        description = item["Description"]
        subjects = item["Subject"]

        entrance_criteria = ["AND"]
        or_subjects = []
        and_subjects = []

        for subject in subjects:
            subject_name = list(subject.keys())[0]
            subject_mark = subject[subject_name]
            if subject_name in ["Mathematics", "Mathematical Literacy", "Technical Mathematics"]:
                and_subjects.append({"subjectid": subject_name, "minmark": subject_mark, "required": True})
            else:
                or_subjects.append({"subjectid": subject_name, "minmark": subject_mark, "required": True})

        if or_subjects:
            entrance_criteria.append(["OR"] + or_subjects)
        if and_subjects:
            entrance_criteria.append(and_subjects)

        qualification_data = {
            "Qualification": qualification,
            "ID": 167 + index,
            "Qualification Code": qualification_code,
            "APS": aps,
            "Description": description,
            "ENTRANCE": entrance_criteria
        }
        output.append(qualification_data)

    return output

def process_files(input_folder_path, output_folder_path):
    # Ensure output folder exists
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    # Process each JSON file in the input folder
    for filename in os.listdir(input_folder_path):
        if filename.endswith('.json'):
            input_file_path = os.path.join(input_folder_path, filename)
            output_file_path = os.path.join(output_folder_path, filename)
            with open(input_file_path, 'r') as f:
                input_data = json.load(f)
                output_data = convert_input(input_data)
                with open(output_file_path, 'w') as out_file:
                    json.dump(output_data, out_file, indent=4)

# Define input and output folder paths
input_folder_path = 'C:/Users/Zusakhe Mbebe/course-data/Zusakhe/Auto-requirements'
output_folder_path = 'C:/Users/Zusakhe Mbebe/course-data/Zusakhe/_updated_Auto-requirements'

# Process files in the input folder and save the converted output in the output folder
process_files(input_folder_path, output_folder_path)
