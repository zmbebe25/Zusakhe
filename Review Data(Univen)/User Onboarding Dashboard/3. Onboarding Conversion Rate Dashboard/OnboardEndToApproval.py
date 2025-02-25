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
    "State": "Approved Strategy"
}

# ✅ Fetch Users Matching Query
users_data = list(users_collection.find(filter_query, {"_id": 1}))

# ✅ Extract all onBehalfOf values from application data
on_behalf_of_ids = [str(app["_id"]) for app in users_data]

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

# ✅ Group counts initialization
qa_time_groups = {
    "1-3 days": 0,
    "4-7 days": 0,
    "7-14 days": 0,
    "14-21 days": 0,
    "More than 21 days": 0
}

for app in users_data:
    app_id = str(app["_id"])

    # ✅ Filter logs for this application
    app_logs = [log for log in action_logs if log.get("onBehalfOf") == app_id]

    # ✅ Find last occurrence of "Updated state to Staging from QA" or "Updated state to Staging from QA Failed"
    staging_from_qa_action = next(
        (log for log in reversed(app_logs) if 
         "Updated state to Staging from QA" in log.get("action", "") or 
         "Updated state to Staging from QA Failed" in log.get("action", "")),
        None
    )

    # ✅ Find first occurrence of "get draft strategy"
    draft_strategy_action = next(
        (log for log in app_logs if "get draft strategy" in log.get("action", "")),
        None
    )

    if staging_from_qa_action and draft_strategy_action:
        try:
            # ✅ Convert timestamps to datetime
            staging_time = staging_from_qa_action["actionTime"]
            draft_strategy_time = draft_strategy_action["actionTime"]

            if isinstance(staging_time, dict) and "$date" in staging_time:
                staging_time = datetime.fromisoformat(staging_time["$date"].replace("Z", "+00:00")).replace(tzinfo=utc)
            elif isinstance(staging_time, datetime):
                staging_time = staging_time.replace(tzinfo=utc)
            else:
                raise ValueError("Invalid StagingFromQA time format")

            if isinstance(draft_strategy_time, dict) and "$date" in draft_strategy_time:
                draft_strategy_time = datetime.fromisoformat(draft_strategy_time["$date"].replace("Z", "+00:00")).replace(tzinfo=utc)
            elif isinstance(draft_strategy_time, datetime):
                draft_strategy_time = draft_strategy_time.replace(tzinfo=utc)
            else:
                raise ValueError("Invalid DraftStrategyTime format")

            # ✅ Calculate QA Time
            qa_time_hours = (draft_strategy_time - staging_time).total_seconds() / 3600  # Convert to hours
            qa_time_days = qa_time_hours / 24  # Convert hours to days

            # ✅ **Skip Negative Values**
            if qa_time_days < 0:
                print(f"Skipping negative value for {app_id}: {round(qa_time_days, 2)} days")
                continue

            # ✅ Track QA Time Days
            qa_time_days_list.append(qa_time_days)

            # ✅ Benchmark Evaluation (<=3 days)
            if qa_time_days <= 3:
                benchmark_met += 1
            else:
                benchmark_not_met += 1

            # ✅ Categorize into Groups
            if 1 <= qa_time_days <= 3:
                qa_time_groups["1-3 days"] += 1
            elif 4 <= qa_time_days <= 7:
                qa_time_groups["4-7 days"] += 1
            elif 7 < qa_time_days <= 14:
                qa_time_groups["7-14 days"] += 1
            elif 14 < qa_time_days <= 21:
                qa_time_groups["14-21 days"] += 1
            else:
                qa_time_groups["More than 21 days"] += 1

            # ✅ Print each QA time calculated
            print(f"UserID: {app_id} | QATimeDays: {round(qa_time_days, 2)} days")

            qa_times.append({
                "onBehalfOf": app_id,
                "StagingFromQATime": staging_time.isoformat(),
                "DraftStrategyTime": draft_strategy_time.isoformat(),
                "TimeHours": round(qa_time_hours, 2),
                "TimeDays": round(qa_time_days, 2),
            })

        except Exception as e:
            print(f"Error processing user {app_id}: {e}")

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
        "QATimeGroups": qa_time_groups
    }
}

# ✅ Print summary
print("\n=== Summary ===")
print(f"Average QA Time: {round(avg_qa_days, 2)} days, {round(avg_qa_hours, 2)} hours")
print(f"Met Benchmark (<=3 days): {benchmark_met}")
print(f"Did Not Meet Benchmark (>3 days): {benchmark_not_met}\n")
print("\n=== QA Time Groups ===")
for group, count in qa_time_groups.items():
    print(f"{group}: {count}")

# ✅ Save the results to a JSON file
output_file = r"C:\Users\zusakhe_gradesmatch\Downloads\Zusakhe-1\Review Data(Univen)\User Onboarding Dashboard\3. Onboarding Conversion Rate Dashboard\OnboardEndToApproval(DaysGrouped).json"
with open(output_file, "w", encoding="utf-8") as outfile:
    json.dump(output_data, outfile, indent=4)

print(f"QA times and summary have been calculated and saved to {output_file}")
