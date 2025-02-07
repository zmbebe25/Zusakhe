import json
from itertools import combinations

# Define input and output file paths
json_path = "C:/Users/zusakhe_gradesmatch/Downloads/MatchedQualificationGroup_WithCounts(2024).json"  # Replace with your file path
output_path = "C:/Users/zusakhe_gradesmatch/Downloads/MatchedQualificationGroup_WithCounts_UniqueAndDuplicates(2024).json"  # Replace with your output file path

# Load the JSON data
with open(json_path, "r", encoding="utf-8") as file:
    data = json.load(file)

# Initialize variables
category_schools = {}
duplicate_school_counts = {}
unique_school_counts = {}

# Collect schools for each category
for category, category_data in data.items():
    if isinstance(category_data, dict) and "Schools" in category_data:
        category_schools[category] = set(
            school["School"] for school in category_data["Schools"] if isinstance(school, dict) and "School" in school
        )

# Flatten the list of all schools and count occurrences across all categories
all_schools_flat = [school for schools in category_schools.values() for school in schools]
school_occurrences = {school: all_schools_flat.count(school) for school in set(all_schools_flat)}

# Process each category for unique and duplicate schools
for category, schools in category_schools.items():
    # Unique schools are those that appear only in this category
    unique_schools = {school for school in schools if school_occurrences[school] == 1}
    # Duplicate schools are those shared with other categories
    duplicate_schools = {school for school in schools if school_occurrences[school] > 1}

    # Add counts to the respective dictionaries
    unique_school_counts[category] = len(unique_schools)
    duplicate_school_counts[category] = len(duplicate_schools)

    # Update the original data structure with the counts
    if isinstance(data[category], dict):
        data[category]["UniqueSchoolCount"] = len(unique_schools)
        data[category]["DuplicateSchoolCount"] = len(duplicate_schools)

# Add pairwise duplicate counts for combinations of categories
pairwise_duplicate_counts = {}
categories = list(category_schools.keys())
for comb in combinations(categories, 2):  # All 2-category combinations
    shared_schools = category_schools[comb[0]].intersection(category_schools[comb[1]])
    pairwise_duplicate_counts[", ".join(comb)] = {
        "Categories": comb,
        "DuplicateSchoolCount": len(shared_schools),
        "SharedSchools": list(shared_schools)  # Add shared school names for reference
    }

# Add the pairwise duplicates to the main dataset
data["PairwiseDuplicateSchoolCounts"] = pairwise_duplicate_counts

# Calculate the total number of unique and duplicate schools
total_unique_school_count = sum(unique_school_counts.values())
total_duplicate_school_count = sum(duplicate_school_counts.values())

# Add total counts to the JSON
data["TotalUniqueSchoolCount"] = total_unique_school_count
data["TotalDuplicateSchoolCount"] = total_duplicate_school_count

# Save the updated data with counts back to a new JSON file
with open(output_path, "w", encoding="utf-8") as file:
    json.dump(data, file, indent=4)

print(f"Updated data with unique and duplicate school counts saved to {output_path}")
