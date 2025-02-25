import json
from collections import Counter
from pymongo import MongoClient
from datetime import datetime

# ✅ MongoDB Connection Details
mongo_uri = "mongodb+srv://zusakhe:KN3VcfCsVuyafM9l@mailserver.seham.mongodb.net/test?"
database_name = "gradesmatch_social"
collection_name = "whatsapp_queue"

# ✅ MongoDB Connection
client = MongoClient(mongo_uri)
db = client[database_name]
whatsapp_collection = db[collection_name]

# ✅ Define the Query (Filter for relevant messages)
filter_query = {
    "Message": {"$regex": "You have started the Onboarding Process", "$options": "i"},
    "CreatedTime": {"$gte": datetime(2025, 1, 1)}
}

# ✅ Fetch Data from MongoDB
data = list(whatsapp_collection.find(filter_query, {"To": 1, "_id": 0}))

# ✅ Extract "To" values
to_list = [entry["To"] for entry in data if "To" in entry]

# ✅ Count occurrences of each "To" value
to_counts = Counter(to_list)

# ✅ Find duplicates
duplicates = {key: count for key, count in to_counts.items() if count > 1}

# ✅ Prepare output data
output_data = {
    "TotalRecords": len(to_list),
    "UniqueToCount": len(set(to_list)),
    "DuplicateToNumbers": duplicates
}

# ✅ Output File Path
output_file_path = r"C:\Users\zusakhe_gradesmatch\Downloads\Zusakhe-1\Review Data(Univen)\User Onboarding Dashboard\3. Onboarding Conversion Rate Dashboard\WhatsappReminderOutput.json"

# ✅ Save results to JSON file
with open(output_file_path, "w", encoding="utf-8") as outfile:
    json.dump(output_data, outfile, indent=4)

# ✅ Print confirmation message
print(f"✅ Results saved to {output_file_path}")
print(json.dumps(output_data, indent=4))  # Print output for debugging
