import json

# Define the input and output file paths
json_path = "C:/Users/zusakhe_gradesmatch/Downloads/QualificationGroup(2024).json"
output_path = "C:/Users/zusakhe_gradesmatch/Downloads/MatchedQualificationGroup_WithCounts(2024).json"

# Load JSON data
with open(json_path, "r", encoding="utf-8") as file:
    data = json.load(file)

# Process data to find matched qualifications and add counts
for entry in data:
    try:
        # Extract QualificationGroups from Preferred and Chosen Qualifications
        preferred_groups = {
            qual.get("QualificationGroup", "").strip() 
            for qual in entry.get("PreferredQualifications", []) 
            if qual.get("QualificationGroup")
        }
        chosen_groups = {
            qual.get("QualificationGroup", "").strip() 
            for qual in entry.get("ChosenQualifications", []) 
            if qual.get("QualificationGroup")
        }
        
        # Find matching QualificationGroups
        matched_qualifications = list(preferred_groups & chosen_groups)
        
        # Add counts for PreferredQualifications and MatchedQualifications
        preferred_count = len(preferred_groups)
        matched_count = len(matched_qualifications)
        match_percentage = (matched_count / preferred_count * 100) if preferred_count > 0 else 0
        
        entry["PreferredCount"] = preferred_count
        entry["MatchedQualifications"] = matched_qualifications
        entry["MatchedCount"] = matched_count
        entry["MatchPercentage"] = round(match_percentage, 2)  # Rounded to 2 decimal places

    except Exception as e:
        print(f"Error processing entry with _id {entry['_id']['$oid']}: {e}")

# Save the updated data to a new JSON file
with open(output_path, "w", encoding="utf-8") as file:
    json.dump(data, file, indent=4)

print(f"Matched qualifications, counts, and percentages have been saved to {output_path}.")
