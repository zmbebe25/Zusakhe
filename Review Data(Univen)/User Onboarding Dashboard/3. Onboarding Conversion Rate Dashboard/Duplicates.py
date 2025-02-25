import json

# ✅ File Paths
input_file_path = r"C:\Users\zusakhe_gradesmatch\Downloads\Zusakhe-1\Review Data(Univen)\User Onboarding Dashboard\3. Onboarding Conversion Rate Dashboard\Re-engagemenetProcessed_Users(New).json"
output_file_path = r"C:\Users\zusakhe_gradesmatch\Downloads\Zusakhe-1\Review Data(Univen)\User Onboarding Dashboard\3. Onboarding Conversion Rate Dashboard\Re-engagemenetProcessed_Users.json"

# ✅ Load JSON Data
try:
    with open(input_file_path, "r", encoding="utf-8") as infile:
        users_data = json.load(infile)
except Exception as e:
    print(f"⚠️ Error reading input file: {e}")
    users_data = []

# ✅ Remove Duplicates Based on UserID
unique_users = {}
for user in users_data:
    user_id = user.get("Phone")
    if user_id and user_id not in unique_users:
        unique_users[user_id] = user  # Store unique users by UserID

# ✅ Convert Dictionary to List
cleaned_users = list(unique_users.values())

# ✅ Save Cleaned Data to JSON File
try:
    with open(output_file_path, "w", encoding="utf-8") as outfile:
        json.dump(cleaned_users, outfile, indent=4)
    print(f"✅ Duplicates removed and saved to {output_file_path}")
except Exception as e:
    print(f"⚠️ Error saving output file: {e}")

# ✅ Print Summary
print(f"\nTotal Users Before: {len(users_data)}")
print(f"Total Users After Removing Duplicates: {len(cleaned_users)}")
