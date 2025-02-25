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
db_analytics = client[database_name_analytics]
users_collection = db_core[collection_name_core]
action_logs_collection = db_analytics[collection_name_analytics]

# ✅ Define MongoDB Query
filter_query = {
    "ApplicationYear": 2024,
    "State": {"$in": ["Feedback", "Special Feedback"]}
}

# ✅ Fetch Users Matching the Query
users_data = list(users_collection.find(filter_query, {"_id": 1}))

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
utc = pytz.UTC  # Use pytz to handle UTC timezone

for user in users_data:
    user_id = str(user["_id"])  # Convert ObjectId to String

    # Filter logs for this application
    user_logs = [log for log in action_logs if log.get("onBehalfOf") == user_id]

    # Find last occurrence of "Done by learner"
    last_done_by_learner = next(
        (log for log in reversed(user_logs) if "Done by learner" in log.get("action", "")),
        None
    )

    # Find latest QA-related action (Matching "Updated state to Feedback")
    latest_qa_action = next(
        (log for log in reversed(user_logs) if "Updated state to Feedback" in log.get("action", "")),
        None
    )

    if last_done_by_learner and latest_qa_action:
        try:
            # Convert timestamps to datetime
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
                raise ValueError("Invalid FeedbackActionTime format")

            # ✅ Calculate QA Time
            qa_time_hours = (qa_time - done_time).total_seconds() / 3600  # Convert to hours
            qa_time_days = qa_time_hours / 24  # Convert hours to days

            # ✅ **Skip Negative Values**
            if qa_time_days < 0:
                print(f"Skipping negative value for {user_id}: {round(qa_time_days, 2)} days")
                continue

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
                "FeedbackActionTime": qa_time.isoformat(),
                "FeedbackAction": latest_qa_action.get("action"),
                "FeedbackTimeHours": round(qa_time_hours, 2),
                "FeedbackTimeDays": round(qa_time_days, 2),
            })

        except Exception as e:
            print(f"Error processing user {user_id}: {e}")

# ✅ Calculate Average Feedback Time (Only from valid positive values)
if qa_time_days_list:
    avg_qa_days = statistics.mean(qa_time_days_list)
    avg_qa_hours = avg_qa_days * 24
else:
    avg_qa_days = avg_qa_hours = 0

# ✅ Final JSON Output Structure
output_data = {
    "FeedbackTimeDetails": qa_times,
    "Summary": {
        "AverageQATime": {
            "Days": round(avg_qa_days, 2),
            "Hours": round(avg_qa_hours, 2),
        },
        "BenchmarkCount": {
            "MetBenchmark (<=5 days)": benchmark_met,
            "DidNotMeetBenchmark (>5 days)": benchmark_not_met
        }
    }
}

# ✅ Print Summary
print("\n=== Summary ===")
print(f"Average Feedback Time: {round(avg_qa_days, 2)} days, {round(avg_qa_hours, 2)} hours")
print(f"Met Benchmark (<=5 days): {benchmark_met}")
print(f"Did Not Meet Benchmark (>5 days): {benchmark_not_met}\n")

# ✅ Save Results to a JSON File
output_file = r"C:\Users\zusakhe_gradesmatch\Downloads\Zusakhe-1\Review Data(Univen)\User Onboarding Dashboard\1. Overall Onboarding Dashboard\Project\Feedback_times.json"
with open(output_file, "w", encoding="utf-8") as outfile:
    json.dump(output_data, outfile, indent=4)

print(f"✅ Feedback times and summary have been calculated and saved to {output_file}")
