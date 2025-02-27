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

# ✅ Timezone UTC
utc = pytz.UTC

# ✅ Define MongoDB Query (Filter Users)
filter_query = {
    "ApplicationYear": 2025,
    "School": {"$ne": None},
    "PreferredQualifications": {"$ne": None},
    "AdditionalDetails": {"$ne": None},
    "TotalDocs": {"$ne": None},
    "State": "Approved Strategy"
}

# ✅ Fetch Only Relevant User IDs (Instead of Fetching All Data)
users_data = list(users_collection.find(filter_query, {"_id": 1}))

# ✅ Extract all onBehalfOf values
on_behalf_of_ids = [str(app["_id"]) for app in users_data]

# ✅ Fetch Only Required Actions from Action Logs (Instead of Fetching All)
action_logs = list(action_logs_collection.find(
    {
        "onBehalfOf": {"$in": on_behalf_of_ids},
        "action": {"$in": ["Updated state to Staging from QA", 
                           "Updated state to Staging from QA Failed", 
                           "get draft strategy"]}
    },
    {"onBehalfOf": 1, "action": 1, "actionTime": 1}
).sort("actionTime", 1))  # Sort by actionTime in ascending order

# ✅ Initialize Variables
qa_times = []
qa_time_days_list = []
benchmark_met = 0
benchmark_not_met = 0
skipped_users = 0
missing_actions_users = 0
processed_users = 0
total_users = len(users_data)

# ✅ QA Time Groups
qa_time_groups = {
    "1-3 days": 0,
    "4-7 days": 0,
    "7-14 days": 0,
    "14-21 days": 0,
    "More than 21 days": 0
}

# ✅ Group Action Logs by User ID for Faster Lookup
user_logs_map = {}
for log in action_logs:
    user_logs_map.setdefault(log["onBehalfOf"], []).append(log)

# ✅ Process Each User
for app in users_data:
    app_id = str(app["_id"])
    app_logs = user_logs_map.get(app_id, [])

    # ✅ Find last occurrence of "Updated state to Staging from QA" or "Updated state to Staging from QA Failed"
    staging_from_qa_action = next(
        (log for log in reversed(app_logs) if "Updated state to Staging from QA" in log["action"] or 
         "Updated state to Staging from QA Failed" in log["action"]),
        None
    )

    # ✅ Find first occurrence of "get draft strategy"
    draft_strategy_action = next(
        (log for log in app_logs if "get draft strategy" in log["action"]),
        None
    )

    # ✅ Count Users Missing Required Actions
    if not staging_from_qa_action or not draft_strategy_action:
        missing_actions_users += 1
        continue  # Skip Processing

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
            skipped_users += 1
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

        qa_times.append({
            "onBehalfOf": app_id,
            "StagingFromQATime": staging_time.isoformat(),
            "DraftStrategyTime": draft_strategy_time.isoformat(),
            "TimeHours": round(qa_time_hours, 2),
            "TimeDays": round(qa_time_days, 2),
        })

        processed_users += 1  # ✅ Count Successfully Processed Users

    except Exception as e:
        print(f"Error processing user {app_id}: {e}")

# ✅ Calculate Unused Users
unused_users = skipped_users + missing_actions_users

# ✅ Final JSON Output Structure
output_data = {
    "TotalUsers": total_users,
    "ProcessedUsers": processed_users,
    "UnusedUsers": unused_users,
    "SkippedUsers": skipped_users,
    "MissingActionsUsers": missing_actions_users,
    "Summary": {
        "AverageQATime": {
            "Days": round(statistics.mean(qa_time_days_list), 2) if qa_time_days_list else 0,
            "Hours": round(statistics.mean(qa_time_days_list) * 24, 2) if qa_time_days_list else 0,
        },
        "BenchmarkCount": {
            "MetBenchmark (<=3 days)": benchmark_met,
            "DidNotMeetBenchmark (>3 days)": benchmark_not_met
        },
        "QATimeGroups": qa_time_groups
    }
}

# ✅ Save the results to a JSON file
output_file = r"C:\Users\zusakhe_gradesmatch\Downloads\Zusakhe-1\Review Data(Univen)\User Onboarding Dashboard\3. Onboarding Conversion Rate Dashboard\OnboardEndToApproval(DaysGrouped).json"
with open(output_file, "w", encoding="utf-8") as outfile:
    json.dump(output_data, outfile, indent=4)

# ✅ Print Summary
print(f"✅ QA times and summary saved to {output_file}")
print(f"Total Users: {total_users}, Processed Users: {processed_users}, Unused Users: {unused_users}")
