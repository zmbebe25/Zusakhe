import json
import pandas as pd

# Define input and output paths
input_path = "C:/Users/zusakhe_gradesmatch/Downloads/User_Review(Outliers)(2024).json"  # Input JSON file path
output_path = "C:/Users/zusakhe_gradesmatch/Downloads/output(2024).xlsx"  # Output Excel file path

# Load JSON data
with open(input_path, "r", encoding="utf-8") as file:
    data = json.load(file)

# Process data into a flat structure
rows = []
for entry in data:
    try:
        row = {
            "ID": entry["_id"]["$oid"],
            "Province": entry.get("Province", "Unknown"),
            "Average Marks": entry.get("AverageMarks", "N/A"),
            "Application Year": entry.get("ApplicationYear", "N/A"),
            "Matric Year": entry.get("MatricYear", "N/A"),
            "Total Review Time (Minutes)": entry["TotalReviewTime"]["CombinedTimeMinutes"],
        }

        # Safely process Preferred Institutions if available
        row["Preferred Institutions"] = ", ".join(
            [inst["Name"] for inst in entry.get("PreferredInsitutions", []) if "Name" in inst and inst["Name"]]
        )

        # Safely process Preferred Qualifications if available
        row["Preferred Qualifications"] = ", ".join(
            [qual["Name"] for qual in entry.get("PreferredQualifications", []) if "Name" in qual and qual["Name"]]
        )

        # Safely process Chosen Industries
        chosen_industries = entry.get("ChosenIndustries", [])
        if isinstance(chosen_industries, list):  # Check if it's a list
            row["Chosen Industries"] = ", ".join(chosen_industries)
        else:
            row["Chosen Industries"] = "N/A"

        # Safely process Chosen Qualifications
        row["Chosen Qualifications"] = ", ".join(
            [
                f'{qual.get("Institution", "Unknown")} ({qual.get("Qualification", "Unknown")})'
                for qual in entry.get("ChosenQualifications", [])
                if "Qualification" in qual and qual["Qualification"]
            ]
        )

        # Safely process Review Times
        review_times = entry.get("ReviewTimes", {})
        if isinstance(review_times, dict):  # Check if it's a dictionary
            row["Review Times"] = ", ".join([f"{k}: {v}" for k, v in review_times.items()])
        else:
            row["Review Times"] = "N/A"
        
        # Add the row to the output list
        rows.append(row)

    except KeyError as e:
        print(f"Skipping entry due to missing key: {e}")
    except TypeError as e:
        print(f"Skipping entry due to type error: {e}")

# Convert to a pandas DataFrame
df = pd.DataFrame(rows)

# Sort DataFrame by "Total Review Time (Minutes)" in descending order
df = df.sort_values(by="Total Review Time (Minutes)", ascending=False)

# Save to an Excel file
df.to_excel(output_path, index=False, sheet_name="Review Data")

print(f"Data has been saved to {output_path}")
