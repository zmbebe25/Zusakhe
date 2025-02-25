import json
from collections import Counter

# ✅ File Paths
input_file_path = r"C:\Users\zusakhe_gradesmatch\Downloads\Zusakhe-1\Review Data(Univen)\User Onboarding Dashboard\3. Onboarding Conversion Rate Dashboard\Re-engagemenetProcessed_Users.json"
output_file_path = r"C:\Users\zusakhe_gradesmatch\Downloads\Zusakhe-1\Review Data(Univen)\User Onboarding Dashboard\3. Onboarding Conversion Rate Dashboard\Re-engagemenetProcessed_Users(State).json"

# ✅ Load JSON Data
try:
    with open(input_file_path, "r", encoding="utf-8") as infile:
        users_data = json.load(infile)
except Exception as e:
    print(f"⚠️ Error reading input file: {e}")
    users_data = []

# ✅ Extract States and Count Occurrences
state_counts = Counter(user.get("State", "Unknown") for user in users_data)

# ✅ Define Re-engagement Success States
reengagement_states = {
    "QA Review", "Staging", "Approved Strategy", "3 Applications",
    "2 Applications", "Potential Sales", "4 Applications", "Feedback",
    "Learner Exists", "1 Application", "Special Feedback"
}

# ✅ Extract Re-engagement Success Rate
reengagement_counts = {state: count for state, count in state_counts.items() if state in reengagement_states}

# ✅ Calculate Total Re-engagement Success
total_reengaged_users = sum(reengagement_counts.values())

# ✅ Prepare Output Data
output_data = {
    "TotalUsers": len(users_data),
    "StateCounts": dict(state_counts),  # Convert Counter to a regular dictionary
    "Re-engagement Success Rate": {
        "Total Re-engaged Users": total_reengaged_users,
        "Breakdown": reengagement_counts
    }
}

# ✅ Save Results to JSON File
try:
    with open(output_file_path, "w", encoding="utf-8") as outfile:
        json.dump(output_data, outfile, indent=4)
    print(f"✅ State occurrences saved to {output_file_path}")
except Exception as e:
    print(f"⚠️ Error saving output file: {e}")

# ✅ Print Summary
print("\n=== State Occurrences ===")
for state, count in state_counts.items():
    print(f"{state}: {count}")

print("\n=== Re-engagement Success Rate ===")
print(f"Total Re-engaged Users: {total_reengaged_users}")
for state, count in reengagement_counts.items():
    print(f"{state}: {count}")
