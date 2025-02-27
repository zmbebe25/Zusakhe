import json
from datetime import datetime
from pymongo import MongoClient
import pytz
import statistics

# ✅ MongoDB Connection Details
mongo_uri = "mongodb+srv://zusakhe:KN3VcfCsVuyafM9l@mailserver.seham.mongodb.net/test?"
database_name_core = "gradesmatch_core"
collection_name_core = "user"
database_name_analytics = "gradesmatch_analytics"
collection_name_analytics = "actionlog"

# ✅ MongoDB Connection
client = MongoClient(mongo_uri)
db_core = client[database_name_core]
users_collection = db_core[collection_name_core]
db_analytics = client[database_name_analytics]
action_logs_collection = db_analytics[collection_name_analytics]

# ✅ Define MongoDB Query
filter_query = {
    "ApplicationYear": 2025,
    "School": {"$ne": None},
    "PreferredQualifications": {"$ne": None},
    "AdditionalDetails": {"$ne": None},
    "TotalDocs": {"$ne": None},
    "State": {"$in": ["Staging", "Approved Strategy"]}
}

# ✅ Fetch Users Matching the Query
users_data = list(users_collection.find(filter_query))

# ✅ Convert ObjectId to String
on_behalf_of_ids = [str(user["_id"]) for user in users_data]

# ✅ Query the action logs from MongoDB using the onBehalfOf values
action_logs = list(action_logs_collection.find(
    {"onBehalfOf": {"$in": on_behalf_of_ids}}
).sort("actionTime", 1))  # Sort by actionTime in ascending order

# ✅ Initialize QA Time Calculation
qa_times = []
qa_time_days_list = []
benchmark_met = 0
benchmark_not_met = 0
skipped_users = 0  # ✅ Count skipped users
users_without_learner_action = 0  # ✅ Users missing "Done by learner"
users_with_negative_time = 0  # ✅ Users with negative QA time
utc = pytz.UTC  # Use pytz to handle UTC timezone

for user in users_data:
    user_id = str(user["_id"])  # Convert ObjectId to String

    # ✅ Filter logs for this application
    user_logs = [log for log in action_logs if log.get("onBehalfOf") == user_id]

    # ✅ Find latest QA-related action
    latest_qa_action = next(
        (log for log in reversed(user_logs) if "Updated state to QA Failed" in log.get("action", "") or 
         "Updated state to Staging" in log.get("action", "")),
        None
    )

    if latest_qa_action:
        # ✅ Find last occurrence of "Done by learner" BEFORE the latest QA-related action
        last_done_by_learner = None
        for log in reversed(user_logs):
            if log.get("action") and "Done by learner" in log["action"]:
                if log["actionTime"] < latest_qa_action["actionTime"]:  # Ensure it's before QA action
                    last_done_by_learner = log
                    break  # Stop once we find the correct one

        if not last_done_by_learner:
            users_without_learner_action += 1  # ✅ Count users missing "Done by learner"
            skipped_users += 1
            continue  # Skip this user

        try:
            # ✅ Convert timestamps to datetime
            done_time = last_done_by_learner["actionTime"]
            qa_time = latest_qa_action["actionTime"]

            if isinstance(done_time, dict) and "$date" in done_time:
                done_time = datetime.fromisoformat(done_time["$date"].replace("Z", "+00:00")).replace(tzinfo=utc)
            elif isinstance(done_time, datetime):
                done_time = done_time.replace(tzinfo=utc)
            else:
                raise ValueError("Invalid DoneByLearnerTime format")

            if isinstance(qa_time, dict) and "$date" in qa_time:
                qa_time = datetime.fromisoformat(qa_time["$date"].replace("Z", "+00:00")).replace(tzinfo=utc)
            elif isinstance(qa_time, datetime):
                qa_time = qa_time.replace(tzinfo=utc)
            else:
                raise ValueError("Invalid QAActionTime format")

            # ✅ Calculate QA Time
            qa_time_hours = (qa_time - done_time).total_seconds() / 3600  # Convert to hours
            qa_time_days = qa_time_hours / 24  # Convert hours to days

            # ✅ **Skip Negative Values**
            if qa_time_days < 0:
                print(f"Skipping negative value for {user_id}: {round(qa_time_days, 2)} days")
                users_with_negative_time += 1  # ✅ Count negative values
                skipped_users += 1
                continue

            # ✅ Print QA Time Days
            print(f"UserID: {user_id} | QATimeDays: {round(qa_time_days, 2)} days")

            # ✅ Track QA Time Days
            qa_time_days_list.append(qa_time_days)

            # ✅ Benchmark Evaluation (<=3 days)
            if qa_time_days <= 3:
                benchmark_met += 1
            else:
                benchmark_not_met += 1

            qa_times.append({
                "onBehalfOf": user_id,
                "DoneByLearnerTime": done_time.isoformat(),
                "QAActionTime": qa_time.isoformat(),
                "QAAction": latest_qa_action.get("action"),
                "QATimeHours": round(qa_time_hours, 2),
                "QATimeDays": round(qa_time_days, 2),
            })

        except Exception as e:
            print(f"Error processing user {user_id}: {e}")

# ✅ Calculate Average QA Time (Only from valid positive values)
if qa_time_days_list:
    avg_qa_days = statistics.mean(qa_time_days_list)
    avg_qa_hours = avg_qa_days * 24
else:
    avg_qa_days = avg_qa_hours = 0

# ✅ Final JSON Output Structure
output_data = {
    "QATimeDetails": qa_times,
    "Summary": {
        "AverageQATime": {
            "Days": round(avg_qa_days, 2),
            "Hours": round(avg_qa_hours, 2),
        },
        "BenchmarkCount": {
            "MetBenchmark (<=3 days)": benchmark_met,
            "DidNotMeetBenchmark (>3 days)": benchmark_not_met
        },
        "SkippedUsers": {
            "TotalSkipped": skipped_users,
            "UsersWithoutLearnerAction": users_without_learner_action,
            "UsersWithNegativeQA": users_with_negative_time
        }
    }
}

# ✅ Print Summary
print("\n=== Summary ===")
print(f"Total Users Processed: {len(users_data)}")
print(f"Users Skipped: {skipped_users}")
print(f" - Users Without Learner Action: {users_without_learner_action}")
print(f" - Users With Negative QA Time: {users_with_negative_time}")
print(f"Met Benchmark (<=3 days): {benchmark_met}")
print(f"Did Not Meet Benchmark (>3 days): {benchmark_not_met}")
print(f"Average QA Time: {round(avg_qa_days, 2)} days, {round(avg_qa_hours, 2)} hours")

# ✅ Save Results to a JSON File
output_file = r"C:\Users\zusakhe_gradesmatch\Downloads\Zusakhe-1\Review Data(Univen)\User Onboarding Dashboard\1. Overall Onboarding Dashboard\Project\qa_times.json"
with open(output_file, "w", encoding="utf-8") as outfile:
    json.dump(output_data, outfile, indent=4)

print(f"\n✅ QA times and summary have been calculated and saved to {output_file}")
