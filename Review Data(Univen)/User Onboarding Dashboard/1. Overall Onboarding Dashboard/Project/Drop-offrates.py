import json
from pymongo import MongoClient

# MongoDB connection details
mongo_uri = "mongodb+srv://zusakhe:KN3VcfCsVuyafM9l@mailserver.seham.mongodb.net/test?"
database_name = "gradesmatch_core"
collection_name = "user"

# MongoDB connection
client = MongoClient(mongo_uri)
db = client[database_name]
users_collection = db[collection_name]

# Filters for different stages
filters = {
    "Stage 1(Signups)": {"ApplicationYear": 2025, "BridgeApplicant": True},
    "Stage 2(School,PreferredQualifications)": {
        "ApplicationYear": 2025,
        "School": {"$ne": None},
        "PreferredQualifications": {"$ne": None},
    },
    "Stage 3(School,PreferredQualifications,AdditionalDetails)": {
        "ApplicationYear": 2025,
        "School": {"$ne": None},
        "PreferredQualifications": {"$ne": None},
        "AdditionalDetails": {"$ne": None},
    },
    "Stage 4(School,PreferredQualifications,AdditionalDetails,TotalDocs)": {
        "ApplicationYear": 2025,
        "School": {"$ne": None},
        "PreferredQualifications": {"$ne": None},
        "AdditionalDetails": {"$ne": None},
        "TotalDocs": {"$ne": None},
    },
    "Stage 5(School,PreferredQualifications,AdditionalDetails,TotalDocs,State:Staging& Approved Strategy)": {
        "ApplicationYear": 2025,
        "School": {"$ne": None},
        "PreferredQualifications": {"$ne": None},
        "AdditionalDetails": {"$ne": None},
        "TotalDocs": {"$ne": None},
        "State": {"$in": ["Staging", "Approved Strategy"]},
    },
}

# Calculate counts for each stage
stage_counts = {}
for stage, query in filters.items():
    try:
        count = users_collection.count_documents(query)
        stage_counts[stage] = count
    except Exception as e:
        print(f"Error retrieving data for {stage}: {e}")
        stage_counts[stage] = 0  # Default to 0 if an error occurs

# Calculate drop-off rates relative to Stage 1
drop_off_rates = {}
stage_1_count = stage_counts.get("Stage 1(Signups)", 0)  # Ensure no KeyError

for stage, count in stage_counts.items():
    if stage_1_count > 0:
        drop_rate = ((stage_1_count - count) / stage_1_count) * 100
    else:
        drop_rate = 0  # Prevent division by zero

    drop_off_rates[stage] = round(drop_rate, 2)

# Prepare final JSON output
output_data = {
    "StageCounts": stage_counts,
    "DropOffRates": drop_off_rates,
}

# Save the results to a JSON file
output_file = "C:/Users/zusakhe_gradesmatch/Downloads/Zusakhe-1/Review Data(Univen)/User Onboarding Dashboard/1. Overall Onboarding Dashboard/Project/drop_off_rates.json"
try:
    with open(output_file, "w", encoding="utf-8") as outfile:
        json.dump(output_data, outfile, indent=4)
    print(f"\nDrop-off rates have been calculated and saved to {output_file}")
except Exception as e:
    print(f"Error saving JSON file: {e}")

# Print results
print("\n=== Drop-Off Rate Analysis ===")
print(json.dumps(output_data, indent=4))
