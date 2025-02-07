import json

# Define input and output paths
input_data_path = "C:/Users/zusakhe_gradesmatch/Downloads/exported_data2(2023).json"  # Replace with your input file path
output_file = "C:/Users/zusakhe_gradesmatch/Downloads/exported_data(2023).json"    # Replace with your desired output file path

# Define the list of valid institutions
valid_institutions = [
    "Nelson Mandela Metropolitan University",
    "Rhodes University",
    "University of Fort Hare",
    "Walter Sisulu University",
    "University of Free State",
    "Central University of Technology",
    "University of Johannesburg",
    "University of Pretoria",
    "University of South Africa",
    "University of the Witwatersrand",
    "Tshwane University of Technology",
    "Sefako Makgatho Health Sciences University",
    "Vaal University of Technology",
    "University of KwaZulu-Natal",
    "University of Zululand",
    "Durban University of Technology",
    "Mangosuthu University of Technology",
    "University of Limpopo",
    "University of Venda",
    "University of Mpumalanga",
    "Sol Plaatje University",
    "North West University",
    "University of Cape Town",
    "Stellenbosch University",
    "University of Western Cape",
    "Cape Peninsula University of Technology"
]

# Load input data
with open(input_data_path, "r") as file:
    input_data = json.load(file)

# Initialize a dictionary to group data by UserID and Institution
grouped_data = {}

# Process each user's data
for user_id, changes in input_data.items():
    if user_id not in grouped_data:
        grouped_data[user_id] = {}

    # Group changes by institution for the current user
    for change in changes:
        for institution in valid_institutions:
            if institution in change["changes"]:
                if institution not in grouped_data[user_id]:
                    grouped_data[user_id][institution] = []

                # Add the change to the institution under the current UserID
                grouped_data[user_id][institution].append({
                    "ChangeID": change["_id"],
                    "CreatedTime": change["CreatedTime"],
                    "CreatedBy": change["CreatedBy"],
                    "ChangeDescription": change["changes"]
                })

# Convert the grouped data to a list for JSON serialization
output_data = []
for user_id, institutions in grouped_data.items():
    user_entry = {"UserID": user_id, "Institutions": []}
    for institution, changes in institutions.items():
        user_entry["Institutions"].append({
            "Institution": institution,
            "Changes": changes
        })
    output_data.append(user_entry)

# Write the result to the output file
with open(output_file, "w") as file:
    json.dump(output_data, file, indent=2)

print(f"Data has been successfully grouped and saved to {output_file}")
