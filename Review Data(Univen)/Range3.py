import json
from datetime import timedelta

# Define file paths
input_data_path = "C:/Users/zusakhe_gradesmatch/Downloads/merged_data(2023).json"
output_file = "C:/Users/zusakhe_gradesmatch/Downloads/cleaned_review_data(2023).json"

# Function to parse TotalTime
def parse_time(total_time):
    if not total_time:
        return None
    try:
        if "days" in total_time:
            # Extract days, hours, minutes, seconds
            days, time_part = total_time.split(" days, ")
            days = int(days)
            hours, minutes, seconds = map(float, time_part.split(":"))
        else:
            # Only hours, minutes, and seconds
            days = 0
            hours, minutes, seconds = map(float, total_time.split(":"))
        # Convert to timedelta
        return timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
    except ValueError:
        return None

# Load input data
with open(input_data_path, "r") as input_file:
    data = json.load(input_file)

# Process data: Categorize performance and calculate review times
performance_categories = {
    "Inadequate Learner (Average(0-39%))": [],
    "Moderate Learner (Average(40-49%))": [],
    "Adequate Learner (Average(50-59%))": [],
    "Good Learner (Average(60-69%))": [],
    "Proficient Learner (Average: 70-79%)": [],
    "Excellent Learner (Average(80-100%))": [],
}

review_times = []

for institution in data:
    for user in institution.get("Users", []):
        avg_marks = user.get("AverageMarks")
        chosen_qualifications = [
            q["Qualification"] for q in user.get("ChosenQualifications", [])
        ]
        chosen_institutions = user.get("ChosenInstitutions", [])
        preferred_institutions = user.get("PreferredInstitutions", [])
        preferred_qualifications = user.get("PreferredQualifications", [])
        total_time = user.get("TotalTime")
        
        review_time = parse_time(total_time)

        # Append to review_times even if no category is assigned yet
        if review_time and review_time >= timedelta(minutes=1) and avg_marks is not None:
            review_times.append({
                "UserID": user.get("UserID"),
                "ReviewTime": review_time,
                "AverageMarks": avg_marks,
                "ChosenQualifications": chosen_qualifications,
                "ChosenInstitutions": chosen_institutions,
                "PreferredInstitutions": preferred_institutions,
                "PreferredQualifications": preferred_qualifications,
            })

            # Assign category based on review time and average marks
            if avg_marks < 40:
                category = "Inadequate Learner (Average(0-39%))"
            elif 40 <= avg_marks < 50:
                category = "Moderate Learner (Average(40-49%))"
            elif 50 <= avg_marks < 60:
                category = "Adequate Learner (Average(50-59%))"
            elif 60 <= avg_marks < 70:
                category = "Good Learner (Average(60-69%))"
            elif 70 <= avg_marks < 80:
                category = "Proficient Learner (Average: 70-79%)"
            elif avg_marks >= 80:
                category = "Excellent Learner (Average(80-100%))"
            else:
                continue

            performance_categories[category].append({
                "UserID": user.get("UserID"),
                "AverageMarks": avg_marks,
                "ReviewTime": str(review_time),
                "ChosenQualifications": chosen_qualifications,
                "ChosenInstitutions": chosen_institutions,
                "PreferredInstitutions": preferred_institutions,
                "PreferredQualifications": preferred_qualifications
            })

# Calculate average review time for each category
average_review_times = {}
for category, users in performance_categories.items():
    if users:
        total_time = sum([parse_time(user["ReviewTime"]).total_seconds() for user in users], 0)
        avg_time = total_time / len(users)
        average_review_times[category] = str(timedelta(seconds=avg_time))
    else:
        average_review_times[category] = "No Data"

# Ensure review_times is not empty before finding slowest and fastest reviews
if review_times:
    slowest_review = max(review_times, key=lambda x: x["ReviewTime"])
    fastest_review = min(review_times, key=lambda x: x["ReviewTime"])

    summary = {
        "FastestReview": {
            "UserID": fastest_review["UserID"],
            "ReviewTime": str(fastest_review["ReviewTime"]),
            "AverageMarks": fastest_review["AverageMarks"],
            "ChosenQualifications": fastest_review["ChosenQualifications"],
            "ChosenInstitutions": fastest_review["ChosenInstitutions"],
            "PreferredInstitutions": fastest_review["PreferredInstitutions"],
            "PreferredQualifications": fastest_review["PreferredQualifications"],
        },
        "SlowestReview": {
            "UserID": slowest_review["UserID"],
            "ReviewTime": str(slowest_review["ReviewTime"]),
            "AverageMarks": slowest_review["AverageMarks"],
            "ChosenQualifications": slowest_review["ChosenQualifications"],
            "ChosenInstitutions": slowest_review["ChosenInstitutions"],
            "PreferredInstitutions": slowest_review["PreferredInstitutions"],
            "PreferredQualifications": slowest_review["PreferredQualifications"],
        }
    }
else:
    summary = {
        "FastestReview": None,
        "SlowestReview": None
    }

# Save processed data to output file
with open(output_file, "w") as output_file:
    json.dump(
        {
            "PerformanceCategories": performance_categories,
            "AverageReviewTimes": average_review_times,
            "ReviewSummary": summary,
        },
        output_file,
        indent=4,
    )

print(f"Processed data with average, slowest, and fastest reviews has been saved to {output_file}")
