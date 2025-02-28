import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from pymongo import MongoClient

dash.register_page(__name__, path="/onboarding-funnel")

# ✅ MongoDB Connection
mongo_uri = "mongodb+srv://zusakhe:KN3VcfCsVuyafM9l@mailserver.seham.mongodb.net/test?"
client = MongoClient(mongo_uri)
db = client["gradesmatch_core"]
collection = db["user"]

# ✅ Fetch counts from MongoDB
total_signups = collection.count_documents({"ApplicationYear": 2025, "BridgeApplicant": True})

started_onboarding = collection.count_documents({
    "ApplicationYear": 2025,
    "School": {"$ne": None},
    "PreferredQualifications": {"$ne": None},
    "AdditionalDetails": {"$ne": None}
})

completed_onboarding = collection.count_documents({
    "ApplicationYear": 2025,
    "School": {"$ne": None},
    "PreferredQualifications": {"$ne": None},
    "AdditionalDetails": {"$ne": None},
    "TotalDocs": {"$ne": None},
    "State": {"$in": ["Staging", "Approved Strategy"]}
})

approved_users = collection.count_documents({
    "ApplicationYear": 2025,
    "State": "Approved Strategy"
})

application_submitted = collection.count_documents({
    "ApplicationYear": 2025,
    "State": {
        "$in": [
            "1 Application", "1 application", "12 Applications",
            "2 Applications", "2+ Applications", "2+ applications", "3 Applications",
            "4 Applications", "5 Applications", "6 Applications", "7 Applications",
            "8 Applications", "9 Applications"
        ]
    }
})

completion = collection.count_documents({
    "ApplicationYear": 2025,
    "State": {"$in": ["Feedback", "Special Feedback"]}
})

# ✅ Create a DataFrame for the Funnel Chart
funnel_data = pd.DataFrame({
    "Stage": [
        "Total Sign-Ups",
        "Started Onboarding",
        "Completed Onboarding",
        "Approved",
        "Application Submitted",
        "Completion"
    ],
    "Users": [
        total_signups,
        started_onboarding,
        completed_onboarding,
        approved_users,
        application_submitted,
        completion
    ]
})

# ✅ Calculate Drop-Off Rates
funnel_data["Drop-Off"] = funnel_data["Users"].diff(-1)  # Difference between stages
funnel_data["Conversion Rate (%)"] = (
    funnel_data["Users"].pct_change(-1) * -100
).fillna(0).round(2)  # Percentage conversion

# ✅ Funnel Chart (Main Visualization)
funnel_fig = px.funnel(
    funnel_data,
    x="Users",
    y="Stage",
    title="📊 Onboarding Funnel",
)


# ✅ Layout for Dashboard
layout = html.Div([
    html.H1("Onboarding Funnel Dashboard", style={'textAlign': 'center', 'marginBottom': '20px'}),

    # ✅ Onboarding Funnel Definition
    html.Div([
        html.H3("📌 Onboarding Funnel Definition", style={'textAlign': 'center', 'color': '#2c3e50', 'fontWeight': 'bold'}),
        html.P(
            "The Onboarding Funnel represents the step-by-step journey of users from initial registration to full completion of the process. "
            "It tracks user engagement across key milestones—Sign-Ups, Onboarding, Profile Approval, and Application Submission—highlighting "
            "conversion rates and identifying drop-off points. This helps in visualizing where users disengage, optimizing the onboarding "
            "experience, and improving overall conversion rates.",
            style={'textAlign': 'center', 'color': '#34495e', 'fontSize': '16px'}
        ),
    ], style={'marginBottom': '30px', 'padding': '20px', 'backgroundColor': '#f8f9fa', 'borderRadius': '10px'}),

    # ✅ Funnel Chart
    html.Div([
        html.H3("📊 User Journey Drop-Off", style={'textAlign': 'center'}),
        dcc.Graph(figure=funnel_fig)
    ], style={'marginBottom': '30px'}),

])
