import json

# File paths for input and output
json1_path = "C:/Users/zusakhe_gradesmatch/Downloads/User_Review(Outliers)(2023).json"
json2_path = "C:/Users/zusakhe_gradesmatch/Downloads/School(User2023).json"
output_path = "C:/Users/zusakhe_gradesmatch/Downloads/User_Review(Outliers)(2023).json"

# Load the two JSON files
with open(json1_path, "r") as file1, open(json2_path, "r") as file2:
    json1_data = json.load(file1)
    json2_data = json.load(file2)

# Create a mapping of $oid from json2 for quick lookup
json2_mapping = {entry["_id"]["$oid"]: entry for entry in json2_data}

# Merge data
for record in json1_data:
    record_oid = record["_id"]["$oid"]
    if record_oid in json2_mapping:
        # Add School and SchoolDistrict from json2 to the record
        record["School"] = json2_mapping[record_oid].get("School", None)
        record["SchoolDistrict"] = json2_mapping[record_oid].get("SchoolDistrict", None)

# Save the merged data to a new JSON file
with open(output_path, "w") as output_file:
    json.dump(json1_data, output_file, indent=4)

print(f"Merged data with School and SchoolDistrict has been saved to {output_path}")
