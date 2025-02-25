import json
from collections import Counter

# Path to your JSON file
json_file_path = r"C:\Users\zusakhe_gradesmatch\Downloads\gradesmatch_social.whatsapp_queue.json"  # ✅ Update file path

# Load the JSON data
with open(json_file_path, "r", encoding="utf-8") as file:
    data = json.load(file)

# Extract "To" values
to_list = [entry["To"] for entry in data if "To" in entry]

# Count occurrences of each "To" value
to_counts = Counter(to_list)

# Find duplicates
duplicates = {key: count for key, count in to_counts.items() if count > 1}

# Print results
if duplicates:
    print(f"🔴 Found {len(duplicates)} duplicate 'To' values:")
    for duplicate_to, count in duplicates.items():
        print(f"- {duplicate_to}: {count} times")
else:
    print("✅ No duplicate 'To' values found.")

# Print total records & unique "To" count
print(f"\nTotal Records: {len(to_list)}")
print(f"Unique 'To' Count: {len(set(to_list))}")
