import json

# Function to update the "Subject" key based on the specified conditions
def update_subject(subject_data):
    updated_subject = []
    for subject in subject_data:
        if isinstance(subject, dict):
            for key, value in subject.items():
                if key == "AND":
                    updated_subject.extend(process_and_condition(value))
                elif key == "OR":
                    updated_subject.extend(process_or_condition(value))
                else:
                    updated_subject.append({
                        "subjectid": key.strip(),
                        "minmark": str(value),
                        "required": True
                    })
        elif isinstance(subject, str):
            updated_subject.append({
                "subjectid": subject.strip(),
                "required": True
            })
    return updated_subject

# Process "AND" condition
def process_and_condition(and_condition):
    subjects = []
    for sub_condition in and_condition:
        subjects.append({
            "subjectid": sub_condition["subjectid"].strip(),
            "minmark": str(sub_condition["minmark"]),
            "required": sub_condition.get("required", True)
        })
    return subjects

# Process "OR" condition
def process_or_condition(or_condition):
    subjects = []
    for sub_condition in or_condition:
        subjects.append({
            "subjectid": sub_condition["subjectid"].strip(),
            "minmark": str(sub_condition["minmark"]),
            "required": sub_condition.get("required", True)
        })
    return subjects

# Function to update the JSON file
def update_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    for entry in data:
        entry["Subject"] = update_subject(entry["Subject"])
    
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

# Path to your JSON folder
json_folder_path = "C:/Users/Zusakhe Mbebe/course-data/Zusakhe/Auto-requirements/Final"

# Update each JSON file in the folder
import os
for filename in os.listdir(json_folder_path):
    if filename.endswith(".json"):
        file_path = os.path.join(json_folder_path, filename)
        update_json_file(file_path)
        print(f"Updated {filename}")

print("All files updated successfully.")
