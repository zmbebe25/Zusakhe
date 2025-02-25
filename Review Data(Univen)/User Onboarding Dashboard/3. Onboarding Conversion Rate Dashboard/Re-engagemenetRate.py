import json
from pymongo import MongoClient
from datetime import datetime

# ✅ MongoDB Connection Details
mongo_uri = "mongodb+srv://zusakhe:KN3VcfCsVuyafM9l@mailserver.seham.mongodb.net/test?"
database_name_social = "gradesmatch_social"
collection_name_social = "whatsapp_queue"
database_name_core = "gradesmatch_core"
collection_name_core = "user"

# ✅ MongoDB Connection
client = MongoClient(mongo_uri)
db_social = client[database_name_social]
whatsapp_collection = db_social[collection_name_social]
db_core = client[database_name_core]
users_collection = db_core[collection_name_core]

# ✅ Define the Query (Filter for relevant messages)
filter_query = {
    "Message": {"$regex": "You have started the Onboarding Process", "$options": "i"},
    "CreatedTime": {"$gte": datetime(2025, 1, 1)}
}

# ✅ Fetch relevant messages from WhatsApp queue
whatsapp_data = list(whatsapp_collection.find(filter_query, {"To": 1, "_id": 0}))

# ✅ Function to Convert Phone Numbers
def format_phone_number(to_number):
    """Convert international phone format to local format."""
    if to_number.startswith("27") and len(to_number) == 11:
        return f"0{to_number[2:]}"  # Convert 27xxxxxxxxx → 0xxxxxxxxx
    return to_number  # Return as-is if it doesn't match expected pattern

# ✅ Convert To → Phone format and search for users
processed_users = []
unmatched_users = []  # Track users that fail to match

for entry in whatsapp_data:
    if "To" in entry:
        phone_number = format_phone_number(entry["To"])
        
        # ✅ Search for user by Phone or Whatsapp field
        user = users_collection.find_one(
            {"$or": [{"Phone": phone_number}, {"Whatsapp": phone_number}]},
            {"_id": 1, "State": 1, "Phone": 1, "Whatsapp": 1}
        )

        if user:
            processed_users.append({
                "UserID": str(user["_id"]),
                "State": user.get("State", "Unknown"),
                "Phone": user.get("Phone", "N/A"),
                "Whatsapp": user.get("Whatsapp", "N/A")
            })
        else:
            unmatched_users.append({"Phone": phone_number})  # Track unmatched users

# ✅ Save processed results to JSON file
output_file_path = r"C:\Users\zusakhe_gradesmatch\Downloads\Zusakhe-1\Review Data(Univen)\User Onboarding Dashboard\3. Onboarding Conversion Rate Dashboard\Re-engagemenetProcessed_Users(New).json"
with open(output_file_path, "w", encoding="utf-8") as outfile:
    json.dump(processed_users, outfile, indent=4)

# ✅ Save unmatched users to separate JSON file
unmatched_output_file = r"C:\Users\zusakhe_gradesmatch\Downloads\Zusakhe-1\Review Data(Univen)\User Onboarding Dashboard\3. Onboarding Conversion Rate Dashboard\Unmatched_Users.json"
with open(unmatched_output_file, "w", encoding="utf-8") as unmatched_file:
    json.dump(unmatched_users, unmatched_file, indent=4)

# ✅ Print output summary
print(f"✅ Processed {len(processed_users)} users. Results saved to {output_file_path}")
print(f"⚠️ Unmatched users: {len(unmatched_users)}. Saved to {unmatched_output_file}")

# ✅ Print unmatched users for debugging
if unmatched_users:
    print("\n🚨 Users that failed to match:")
    print(json.dumps(unmatched_users, indent=4))
