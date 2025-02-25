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

# ✅ Drop-Off Heatmap
heatmap_data = pd.DataFrame({
    "Stage": funnel_data["Stage"].iloc[:-1],  # Exclude last stage
    "Drop-Off Rate (%)": funnel_data["Conversion Rate (%)"].iloc[:-1]
})

heatmap_fig = px.bar(
    heatmap_data,
    x="Stage",
    y="Drop-Off Rate (%)",
    title="🔥 Drop-Off Heatmap",
    color="Drop-Off Rate (%)",
    color_continuous_scale="Reds"
)

# ✅ Dummy Data for Trend Line (Replace with actual MongoDB aggregation)
trend_data = pd.DataFrame({
    "Date": pd.date_range(start="2025-01-01", periods=10, freq="D"),
    "Conversion Rate (%)": [30, 35, 40, 50, 55, 60, 65, 70, 75, 80]
})

trend_fig = px.line(
    trend_data,
    x="Date",
    y="Conversion Rate (%)",
    title="📈 Conversion Trends Over Time",
    markers=True
)

# ✅ Layout for Dashboard
layout = html.Div([
    html.H1("Onboarding Funnel Dashboard", style={'textAlign': 'center'}),

    # ✅ Funnel Chart
    html.Div([
        html.H3("User Journey Drop-Off"),
        dcc.Graph(figure=funnel_fig)
    ], style={'marginBottom': '30px'})
])
