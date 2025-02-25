import os
import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
import json
from pymongo import MongoClient

# MongoDB Connection
MONGO_URI = "mongodb+srv://zusakhe:KN3VcfCsVuyafM9l@mailserver.seham.mongodb.net/test?"
DB_NAME = "gradesmatch_core"
COLLECTION_NAME = "user"

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# Paths to additional data
DATA_DIR = r"C:\Users\zusakhe_gradesmatch\Downloads\Zusakhe-1\Review Data(Univen)\1. Overall Onboarding Dashboard"
dropoff_rate_file = os.path.join(DATA_DIR, "drop_off_rates.json")
onboarding_time_file = os.path.join(DATA_DIR, "latest_onboarding_times.json")
qa_time_file = os.path.join(DATA_DIR, "qa_times.json")

# Load JSON Data
def load_json(file_path):
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return {}

dropoff_data = load_json(dropoff_rate_file)
onboarding_data = load_json(onboarding_time_file)
qa_data = load_json(qa_time_file)

# Helper functions for MongoDB counts
def total_users_with_full_docs():
    return collection.count_documents({"ApplicationYear": 2025, "FullDocs": True, "AverageMarks": {"$gte": 55}})

def total_users_awaiting_learner():
    return collection.count_documents({"State": "Awaiting Learner", "ApplicationYear": 2025})

def total_users_disapproved():
    return collection.count_documents({"State": "Disapproved", "ApplicationYear": 2025})

def total_users_closed():
    return collection.count_documents({"State": "Closed", "ApplicationYear": 2025})

def total_learners_sponsored():
    return collection.count_documents({"Packages": "Sponsored", "ApplicationYear": 2025})

def regional_split_learners():
    provinces = ['EC', 'FS', 'GT', 'KZ', 'KZN', 'LP', 'MP', 'NC', 'NW', 'WC']
    results = []
    total_count = 0
    for province in provinces:
        count = collection.count_documents({"State": {"$in": ["Staging", "Approved Strategy", "Awaiting Learner", "Draft Strategy", "Learner Approval"]}, "Province": province, "ApplicationYear": 2025})
        results.append({"Province": province, "Count": count})
        total_count += count
    df = pd.DataFrame(results).sort_values(by="Count", ascending=False)  # Sorted in descending order
    return df, total_count

# Query for users stuck in different states
stuck_states = [
    "QA", "Awaiting Learner", "Feedback", "Disapproved", "Missing Docs", "QA Failed", 
    "Onboarding", "Staging", "Closed", "Approved Strategy"
]
stuck_users_counts = {state: collection.count_documents({"ApplicationYear": 2025, "State": state}) for state in stuck_states}

# Convert stuck states data to DataFrame and sort in descending order
stuck_users_df = pd.DataFrame(list(stuck_users_counts.items()), columns=["State", "User Count"])
stuck_users_df = stuck_users_df.sort_values(by="User Count", ascending=False)  # Sorted in descending order

# Prepare Drop-Off Funnel Data
stage_counts = dropoff_data.get("StageCounts", {})
funnel_df = pd.DataFrame({
    "Stage": list(stage_counts.keys()),
    "Users": list(stage_counts.values())
})

# Prepare Onboarding Time Summary Data
onboarding_summary = onboarding_data.get("AverageOnboardingTime", {})
onboarding_df = pd.DataFrame({
    "Time Unit": ["Hours", "Minutes"],
    "Duration": [onboarding_summary.get("Hours", 0), onboarding_summary.get("Minutes", 0)]
})

# Prepare QA Time Summary Data
qa_summary = qa_data.get("Summary", {}).get("AverageQATime", {})
qa_df = pd.DataFrame({
    "Time Unit": ["Hours", "Minutes"],
    "Duration": [qa_summary.get("Hours", 0), qa_summary.get("Minutes", 0)]
})

# Initialize Dash app
app = dash.Dash(__name__)

# App Layout
app.layout = html.Div([
    html.H1("Onboarding Dashboard", style={'textAlign': 'center'}),

    # Main Statistics
    html.Div([
        html.Div([html.H3("Total Users with Full Docs"), html.P(total_users_with_full_docs(), className='stat-value')], className='stat-box'),
        html.Div([html.H3("Awaiting Learner State"), html.P(total_users_awaiting_learner(), className='stat-value')], className='stat-box'),
        html.Div([html.H3("Disapproved State"), html.P(total_users_disapproved(), className='stat-value')], className='stat-box'),
        html.Div([html.H3("Closed State"), html.P(total_users_closed(), className='stat-value')], className='stat-box'),
        html.Div([html.H3("Learners Approved for Sponsorship"), html.P(total_learners_sponsored(), className='stat-value')], className='stat-box'),
    ], style={'display': 'flex', 'justifyContent': 'space-around', 'marginBottom': '50px'}),

    # Drop-Off Funnel Chart
    html.Div([
        html.H3("Drop-Off Funnel Chart", style={'textAlign': 'center'}),
        dcc.Graph(
            figure=px.funnel(
                funnel_df, x="Users", y="Stage",
                title="Drop-Off Rate Funnel",
                labels={'Users': 'Users Remaining', 'Stage': 'Process Stage'}
            )
        )
    ]),

    # Onboarding Time Summary
    html.Div([
        html.H3("Onboarding Time Summary", style={'textAlign': 'center'}),
        html.P(f"Days: {onboarding_summary.get('Days', 0)}", style={'fontSize': '18px', 'fontWeight': 'bold', 'textAlign': 'center'}),
        html.P(f"Met Benchmark (<=3 days): {onboarding_data.get('BenchmarkCount', {}).get('MetBenchmark (<=3 days)', 0)}"),
        html.P(f"Did Not Meet Benchmark (>3 days): {onboarding_data.get('BenchmarkCount', {}).get('DidNotMeetBenchmark (>3 days)', 0)}")
    ]),

    # QA Time Summary
    html.Div([
        html.H3("QA Time Summary", style={'textAlign': 'center'}),
        html.P(f"Days: {qa_summary.get('Days', 0)}", style={'fontSize': '18px', 'fontWeight': 'bold', 'textAlign': 'center'}),
        html.P(f"Met Benchmark (<=3 days): {qa_data.get('Summary', {}).get('BenchmarkCount', {}).get('MetBenchmark (<=3 days)', 0)}"),
        html.P(f"Did Not Meet Benchmark (>3 days): {qa_data.get('Summary', {}).get('BenchmarkCount', {}).get('DidNotMeetBenchmark (>3 days)', 0)}")
    ]),

    # Users Stuck in Specific States (Bar Graph)
    html.Div([
        html.H3("Users Stuck in Specific States", style={'textAlign': 'center'}),
        dcc.Graph(
            figure=px.bar(
                stuck_users_df, x="State", y="User Count",
                title="Users Stuck in Various States (Sorted Descending)",
                labels={"State": "State", "User Count": "Number of Users"},
                template="plotly_white"
            )
        )
    ]),

    # Regional Split Chart
    html.Div([
        html.H3("Regional Split of Learners with Complete Onboarding", style={'textAlign': 'center'}),
        dcc.Graph(
            figure=px.bar(
                regional_split_learners()[0], x='Province', y='Count',
                title="Regional Split (Sorted Descending)", labels={'Province': 'Province', 'Count': 'Learners'},
                template='plotly_white'
            )
        ),
        html.H4(f"Total Learners Across All Provinces: {regional_split_learners()[1]}", style={'textAlign': 'center'})
    ])
], style={'padding': '20px'})

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, host="0.0.0.0")
