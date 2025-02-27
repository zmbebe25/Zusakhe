import dash
from dash import dcc, html
import plotly.express as px
from pymongo import MongoClient
from datetime import datetime, timezone
import json

# ✅ Register this Page in the Multi-Page App
dash.register_page(__name__, path="/onboarding-conversion")

# ✅ MongoDB Connection
mongo_uri = "mongodb+srv://zusakhe:KN3VcfCsVuyafM9l@mailserver.seham.mongodb.net/test?"
client = MongoClient(mongo_uri)

# ✅ Define DB Collections
db_core = client["gradesmatch_core"]
db_analytics = client["gradesmatch_analytics"]
users_collection = db_core["user"]
state_change_collection = db_analytics["state_change"]

# ✅ Define start of 2025
start_of_2025 = datetime(2025, 1, 1, tzinfo=timezone.utc)

# ✅ Fetch Counts from MongoDB
total_signups = users_collection.count_documents({"ApplicationYear": 2025, "BridgeApplicant": True})

onboarding_start = users_collection.count_documents({
    "ApplicationYear": 2025,
    "School": {"$ne": None},
    "PreferredQualifications": {"$ne": None},
    "AdditionalDetails": {"$ne": None}
})

approved_learners = state_change_collection.count_documents({
    "Action": "Review",
    "CreatedTime": {"$gte": start_of_2025}
})

# ✅ Calculate conversion rates
signup_to_onboarding_rate = (onboarding_start / total_signups) * 100 if total_signups > 0 else 0
onboarding_to_approval_rate = (approved_learners / onboarding_start) * 100 if onboarding_start > 0 else 0

# ✅ Conversion Data for Funnel Chart
conversion_data = {
    "Stage": ["Sign-ups", "Onboarding Start", "Approved"],
    "Users": [total_signups, onboarding_start, approved_learners]
}

# ✅ Load WhatsApp Reminder Data
whatsapp_reminder_path = r"C:\Users\zusakhe_gradesmatch\Downloads\Zusakhe-1\Review Data(Univen)\User Onboarding Dashboard\3. Onboarding Conversion Rate Dashboard\WhatsappReminderOutput.json"

try:
    with open(whatsapp_reminder_path, "r", encoding="utf-8") as file:
        reminder_data = json.load(file)
        total_reminded_learners = reminder_data.get("UniqueToCount", 0)
except Exception as e:
    print(f"⚠️ Error loading WhatsApp reminder data: {e}")
    total_reminded_learners = 0  

# ✅ Load Re-engagement Processed Users Data
reengagement_file = r"C:\Users\zusakhe_gradesmatch\Downloads\Zusakhe-1\Review Data(Univen)\User Onboarding Dashboard\3. Onboarding Conversion Rate Dashboard\Re-engagemenetProcessed_Users(State).json"

try:
    with open(reengagement_file, "r", encoding="utf-8") as file:
        reengagement_data = json.load(file)
        
        # ✅ Ensure "Re-engagement Success Rate" exists and contains only numbers
        success_rate_data = reengagement_data.get("Re-engagement Success Rate", {})
        total_reengaged_users = sum(value for value in success_rate_data.values() if isinstance(value, int))

except Exception as e:
    print(f"⚠️ Error loading Re-engagement data: {e}")
    total_reengaged_users = 0  

# ✅ Calculate New Re-engagement Success Rates
re_engagement_success_rate = (total_reengaged_users / total_reminded_learners) * 100 if total_reminded_learners > 0 else 0
reminded_to_signup_rate = (total_reminded_learners / total_signups) * 100 if total_signups > 0 else 0

# ✅ Load JSON Data for Onboarding Time
onboarding_file = r"C:/Users/zusakhe_gradesmatch/Downloads/Zusakhe-1/Review Data(Univen)/User Onboarding Dashboard/3. Onboarding Conversion Rate Dashboard/SignUP_OnboardStart.json"
with open(onboarding_file, "r", encoding="utf-8") as file:
    onboarding_data = json.load(file)

# ✅ Extract Key Metrics
avg_onboarding_time = onboarding_data["AverageOnboardingTime"]

# ✅ Load JSON Data for QA Time
qa_time_file = r"C:\Users\zusakhe_gradesmatch\Downloads\Zusakhe-1\Review Data(Univen)\User Onboarding Dashboard\3. Onboarding Conversion Rate Dashboard\OnboardEndToApproval(DaysGrouped).json"
with open(qa_time_file, "r", encoding="utf-8") as file:
    qa_time_data = json.load(file)

# ✅ Extract QA Time Metrics
avg_qa_time = qa_time_data["Summary"]["AverageQATime"]

# ✅ Create Bar Charts
onboarding_chart = px.bar(
    x=list(onboarding_data["TimeGroups"].keys()),
    y=list(onboarding_data["TimeGroups"].values()),
    title="Onboarding Time Distribution",
    labels={"x": "Time Groups", "y": "Users"}
)

qa_time_chart = px.bar(
    x=list(qa_time_data["Summary"]["QATimeGroups"].keys()),
    y=list(qa_time_data["Summary"]["QATimeGroups"].values()),
    title="QA Time Distribution",
    labels={"x": "Time Groups", "y": "Users"},
    text_auto=True
)

# ✅ Layout for Onboarding Conversion Page
layout = html.Div([

    html.H1("Onboarding Conversion Rate Dashboard", style={'textAlign': 'center'}),

    # ✅ Conversion Rate Section
    html.Div([
        html.H3("Conversion Rates"),
        dcc.Graph(
            figure=px.funnel(conversion_data, y="Stage", x="Users", title="Onboarding Conversion Funnel")
        ),
        html.P(f"📊 Sign-ups to Onboarding Start: {round(signup_to_onboarding_rate, 2)}%", 
               style={'textAlign': 'center', 'fontSize': '18px', 'fontWeight': 'bold'}),
        html.P(f"📊 Onboarding to Approval: {round(onboarding_to_approval_rate, 2)}%", 
               style={'textAlign': 'center', 'fontSize': '18px', 'fontWeight': 'bold'})
    ], style={'marginBottom': '30px'}),

    # ✅ Re-engagement Success Rate (Total Sign-ups → Reminded Learners)
    html.Div([
        html.H3("Re-engagement Rate (Sign-ups → Reminded Learners)"),
        html.P(f"📌 Total Sign-ups: {total_signups}"),
        html.P(f"📌 Total Learners Who Got Reminder: {total_reminded_learners}"),
        html.P(f"✅ Reminder-to-Signup Rate: {round(reminded_to_signup_rate, 2)}%", 
               style={'fontSize': '24px', 'fontWeight': 'bold', 'color': 'blue'})
    ], style={'marginBottom': '30px'}),

    # ✅ Re-engagement Success Rate (Reminded Learners → Re-engaged Users)
    html.Div([
        html.H3("Re-engagement Rate (Reminded → Re-engaged Users)"),
        html.P(f"📌 Total Learners Who Got Reminder: {total_reminded_learners}"),
        html.P(f"📌 Total Re-engaged Users: {total_reengaged_users}"),
        html.P(f"✅ Re-engagement Success Rate: {round(re_engagement_success_rate, 2)}%", 
               style={'fontSize': '24px', 'fontWeight': 'bold', 'color': 'green'})
    ], style={'marginBottom': '30px'}),

    # ✅ Onboarding Time Analysis
    html.Div([
        html.H3("Sign-up → Onboarding Start Average Time"),
        
        # Display Key Metrics
        html.P(f"📌 Total Users: {onboarding_data.get('TotalUsers', 0)}"),
        html.P(f"📌 Processed Users: {onboarding_data.get('ProcessedUsers', 0)}"),
        html.P(f"📌 Skipped Users: {onboarding_data.get('SkippedUsers', 0)}",
            style={'color': 'red', 'fontWeight': 'bold'}),  # Highlight Skipped Users

        html.P(f"⏳ Average Time: {avg_onboarding_time['Days']} Days",
            style={'fontSize': '18px', 'fontWeight': 'bold'}),

        dcc.Graph(figure=onboarding_chart)
    ], style={'marginBottom': '30px'}),


    # ✅ QA Time Analysis
    html.Div([
        html.H3("Onboarding → Approval Average Time"),
        
        # Display Key Metrics
        html.P(f"📌 Total Users: {qa_time_data.get('TotalUsers', 0)}"),
        html.P(f"📌 Processed Users: {qa_time_data.get('ProcessedUsers', 0)}"),
        html.P(f"📌 Unused Users: {qa_time_data.get('UnusedUsers', 0)}",
            style={'color': 'red', 'fontWeight': 'bold'}),  # Highlight Unused Users
        
        html.P(f"⏳ Average Time: {avg_qa_time['Days']} Days",
            style={'fontSize': '18px', 'fontWeight': 'bold'}),
        
        dcc.Graph(figure=qa_time_chart)
    ], style={'marginBottom': '30px'}),

])
