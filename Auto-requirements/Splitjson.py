data = [
    {
        "Qualification": "CIVIL ENGINEERING",
        "Qualification Code": "B6CISQ",
        "APS": 32,
        "Description": "Plan, design and construction of infrastructure.",
        "Subject": [
            {
                "English": 60
            },
            {
                "Mathematics/Technical Mathematics": 60
            },
            {
                "Physical Sciences": 60
            }
        ]
    },
    # Rest of your data here
]

# Iterate through the data
for entry in data:
    # Check if "Subject" key exists and it contains a dictionary with the specific key
    if "Subject" in entry and any("Mathematics/Technical Mathematics" in sub_dict for sub_dict in entry["Subject"]):
        new_subjects = []
        # Iterate through each subject in "Subject"
        for sub_dict in entry["Subject"]:
            # Check if the subject contains "Mathematics/Technical Mathematics" key
            if "Mathematics/Technical Mathematics" in sub_dict:
                # Split the key and add them as separate dictionaries
                keys = list(sub_dict.keys())[0].split("/")
                for key in keys:
                    new_subjects.append({key: sub_dict["Mathematics/Technical Mathematics"]})
            else:
                new_subjects.append(sub_dict)
        # Replace the old "Subject" list with the new split subjects
        entry["Subject"] = new_subjects

# Print the modified data
for entry in data:
    print(entry)
