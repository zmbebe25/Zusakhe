from pymongo import MongoClient
from datetime import datetime
import dash
from dash import dcc, html
import plotly.express as px

# ✅ Register Dash Page
dash.register_page(__name__, path="/application-progress")

# ✅ MongoDB Connection
mongo_uri = "mongodb+srv://zusakhe:KN3VcfCsVuyafM9l@mailserver.seham.mongodb.net/test?"
client = MongoClient(mongo_uri)
db = client["gradesmatch_core"]
users_collection = db["user"]

# ✅ Define Filters for Metrics
application_ready_query = {
    "ApplicationYear": 2025,
    "State": "Approved Strategy",
    "LastUpdateState": {"$gte": datetime(2025, 1, 1)}
}

application_processing_query = {
    "ApplicationYear": 2025,
    "State": {"$in": [
        "1 Application", "1 application", "12 Applications",
        "2 Applications", "2+ Applications", "2+ applications", "3 Applications",
        "4 Applications", "5 Applications", "6 Applications", "7 Applications",
        "8 Applications", "9 Applications"
    ]}
}

learner_exist_query = {
    "ApplicationYear": 2025,
    "State": "Learner Exists"
}

missing_docs_query = {
    "ApplicationYear": 2025,
    "TotalDocs": None
}

# ✅ Fetch Data from MongoDB
application_ready_count = users_collection.count_documents(application_ready_query)
application_processing_count = users_collection.count_documents(application_processing_query)
learner_exist_count = users_collection.count_documents(learner_exist_query)
missing_docs_count = users_collection.count_documents(missing_docs_query)
total_approved_users = users_collection.count_documents({"ApplicationYear": 2025, "State": "Approved Strategy"})

# ✅ Create a Flow Diagram (User movement from approval to application submission)
flow_data = {
    "Stage": ["Approved", "Application Ready", "Application Processing", "Learner Exists", "Missing Documents"],
    "Users": [total_approved_users, application_ready_count, application_processing_count, learner_exist_count, missing_docs_count]
}

flow_chart = px.funnel(
    flow_data, x="Users", y="Stage",
    title="User Flow from Approval to Application Submission"
)

# ✅ Layout for Dashboard
layout = html.Div([
    html.H1("Application Progress Dashboard", style={'textAlign': 'center'}),

    # ✅ Key Metrics Display
    html.Div([
        html.Div([
            html.H4("Application Ready"),
            html.P(f"{application_ready_count}", style={"fontSize": "22px", "fontWeight": "bold"})
        ], className="three columns"),

        html.Div([
            html.H4("Application Processing"),
            html.P(f"{application_processing_count}", style={"fontSize": "22px", "fontWeight": "bold"})
        ], className="three columns"),

        html.Div([
            html.H4("Learner Exists"),
            html.P(f"{learner_exist_count}", style={"fontSize": "22px", "fontWeight": "bold", "color": "red"})
        ], className="three columns"),

        html.Div([
            html.H4("Missing Documents"),
            html.P(f"{missing_docs_count}", style={"fontSize": "22px", "fontWeight": "bold", "color": "orange"})
        ], className="three columns"),
    ], className="row", style={"marginBottom": "30px"}),
])
