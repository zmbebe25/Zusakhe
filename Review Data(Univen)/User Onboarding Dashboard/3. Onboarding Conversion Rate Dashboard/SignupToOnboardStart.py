from pymongo import MongoClient
from datetime import datetime
import pytz
import json

# ✅ MongoDB Connection Details
mongo_uri = "mongodb+srv://zusakhe:KN3VcfCsVuyafM9l@mailserver.seham.mongodb.net/test?"
database_name = "gradesmatch_core"
collection_name = "user"

# ✅ MongoDB Connection
client = MongoClient(mongo_uri)
db = client[database_name]
users_collection = db[collection_name]

# ✅ Query to filter users in "Onboarding" for 2025
filter_query = {
    "ApplicationYear": 2025,
    "State": "Onboarding"
}

# ✅ Fetch users that match the query
users = list(users_collection.find(filter_query))

# ✅ Initialize results list & time group counters
onboarding_times = []
time_groups = {
    "1-3 days": 0,
    "4-7 days": 0,
    "7-14 days": 0,
    "14-21 days": 0,
    "More than 21 days": 0
}

# ✅ Timezone UTC
utc = pytz.UTC

# ✅ Benchmark Counters
benchmark_true_count = 0
benchmark_false_count = 0

# ✅ Counters for Skipped and Used Users
total_users = len(users)
skipped_users = 0
processed_users = 0

for user in users:
    try:
        # Extract CreatedDate and UpdateTime
        created_date = user.get("CreatedDate")
        last_update_state = user.get("UpdateTime")

        # Convert CreatedDate
        if isinstance(created_date, dict) and "$date" in created_date:
            created_date = datetime.fromisoformat(created_date["$date"].replace("Z", "+00:00")).replace(tzinfo=utc)
        elif isinstance(created_date, datetime):
            created_date = created_date.replace(tzinfo=utc)
        else:
            raise ValueError("Invalid CreatedDate format")

        # 🚀 **Skip if CreatedDate is from 2024**
        if created_date.year == 2024:
            print(f"Skipping user {user['_id']} - CreatedDate is in 2024")
            skipped_users += 1
            continue  # Skip this user and move to the next one

        # Convert UpdateTime
        if isinstance(last_update_state, dict) and "$date" in last_update_state:
            last_update_state = datetime.fromisoformat(last_update_state["$date"].replace("Z", "+00:00")).replace(tzinfo=utc)
        elif isinstance(last_update_state, datetime):
            last_update_state = last_update_state.replace(tzinfo=utc)
        else:
            raise ValueError("Invalid UpdateTime format")

        # ✅ Calculate onboarding time
        onboarding_time_days = (last_update_state - created_date).days
        onboarding_time_hours = (last_update_state - created_date).total_seconds() / 3600
        onboarding_time_minutes = onboarding_time_hours * 60

        # ✅ Check if onboarding was completed within the 3-day benchmark
        benchmark_met = onboarding_time_days <= 3  

        if benchmark_met:
            benchmark_true_count += 1
        else:
            benchmark_false_count += 1

        # ✅ Categorize into Groups
        if 1 <= onboarding_time_days <= 3:
            time_groups["1-3 days"] += 1
        elif 4 <= onboarding_time_days <= 7:
            time_groups["4-7 days"] += 1
        elif 7 < onboarding_time_days <= 14:
            time_groups["7-14 days"] += 1
        elif 14 < onboarding_time_days <= 21:
            time_groups["14-21 days"] += 1
        else:
            time_groups["More than 21 days"] += 1

        onboarding_times.append({
            "UserID": str(user["_id"]),
            "CreatedDate": created_date.isoformat(),
            "UpdateTime": last_update_state.isoformat(),
            "OnboardingTimeDays": onboarding_time_days,
            "OnboardingTimeHours": round(onboarding_time_hours, 2),
            "OnboardingTimeMinutes": round(onboarding_time_minutes, 2),
            "BenchmarkMet": benchmark_met
        })

        processed_users += 1  # ✅ Count Users Used

    except Exception as e:
        print(f"Error processing user {user['_id']}: {e}")

# ✅ Calculate Average Onboarding Time
if onboarding_times:
    avg_days = sum(entry["OnboardingTimeDays"] for entry in onboarding_times) / len(onboarding_times)
    avg_hours = sum(entry["OnboardingTimeHours"] for entry in onboarding_times) / len(onboarding_times)
    avg_minutes = sum(entry["OnboardingTimeMinutes"] for entry in onboarding_times) / len(onboarding_times)
else:
    avg_days, avg_hours, avg_minutes = 0, 0, 0

# ✅ Final Output for Dashboard
final_output = {
    "TotalUsers": total_users,
    "ProcessedUsers": processed_users,
    "SkippedUsers": skipped_users,
    "AverageOnboardingTime": {
        "Days": round(avg_days, 2),
        "Hours": round(avg_hours, 2),
        "Minutes": round(avg_minutes, 2)
    },
    "BenchmarkCount": {
        "MetBenchmark (<=3 days)": benchmark_true_count,
        "DidNotMeetBenchmark (>3 days)": benchmark_false_count
    },
    "TimeGroups": time_groups,  # ✅ Added Time Categories
    "OnboardingDetails": onboarding_times
}

# ✅ Save Results to JSON File
output_file = "C:/Users/zusakhe_gradesmatch/Downloads/Zusakhe-1/Review Data(Univen)/User Onboarding Dashboard/3. Onboarding Conversion Rate Dashboard/SignUP_OnboardStart.json"
with open(output_file, "w", encoding="utf-8") as outfile:
    json.dump(final_output, outfile, indent=4)

# ✅ Print Summary
print(f"✅ Onboarding time calculations saved to {output_file}")
print(f"Total Users: {total_users}")
print(f"Processed Users: {processed_users}")
print(f"Skipped Users: {skipped_users}")
