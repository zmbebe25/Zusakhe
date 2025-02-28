import os
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import json
from pymongo import MongoClient
from datetime import datetime, timedelta, timezone

# ✅ Register Page
dash.register_page(__name__, path="/weekly-updates")

# MongoDB Connection
MONGO_URI = "mongodb+srv://zusakhe:KN3VcfCsVuyafM9l@mailserver.seham.mongodb.net/test?"
DB_NAME = "gradesmatch_core"
COLLECTION_NAME = "user"

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# Define the last five days for filtering data
last_five_days = [(datetime.now(timezone.utc) - timedelta(days=i)).replace(hour=0, minute=0, second=0, microsecond=0) for i in range(5)]

# Fetch data functions
def fetch_data(query):
    return {day.strftime('%Y-%m-%d'): collection.count_documents({
        **query,
        "ApplicationYear": 2025,
        "UpdateTime": {"$gte": day, "$lt": day + timedelta(days=1)}
    }) for day in last_five_days}

weekly_full_docs = fetch_data({"FullDocs": True, "AverageMarks": {"$gte": 55}})
weekly_awaiting_learner = fetch_data({"State": "Awaiting Learner"})
weekly_disapproved = fetch_data({"State": "Disapproved"})
weekly_closed = fetch_data({"State": "Closed"})
weekly_sponsored = fetch_data({"Packages": "Sponsored"})

# Style dictionary
CARD_STYLES = {
    "padding": "20px",
    "borderRadius": "10px",
    "textAlign": "center",
    "boxShadow": "0 4px 8px rgba(0, 0, 0, 0.1)",
    "margin": "10px",
    "color": "white"
}

COLOR_MAP = {
    "Users with Full Docs": "#28a745",
    "Awaiting Learner State": "#ffc107",
    "Disapproved State": "#dc3545",
    "Closed State": "#6c757d",
    "Learners Approved for Sponsorship": "#17a2b8"
}

# Function to create cards
def create_stat_card(title, data):
    return dbc.Card(
        dbc.CardBody([
            html.H4(title, className="card-title"),
            html.Div([html.P(f"{day}: {count}", className="card-text") for day, count in data.items()])
        ]),
        style={**CARD_STYLES, "backgroundColor": COLOR_MAP[title]}
    )

# ✅ Define layout
layout = dbc.Container([
    html.H1("Weekly updates", className="text-center my-4"),

    dbc.Row([
        dbc.Col(create_stat_card("Users with Full Docs", weekly_full_docs), width=4),
        dbc.Col(create_stat_card("Awaiting Learner State", weekly_awaiting_learner), width=4),
        dbc.Col(create_stat_card("Disapproved State", weekly_disapproved), width=4),
    ], className="mb-4"),

    dbc.Row([
        dbc.Col(create_stat_card("Closed State", weekly_closed), width=6),
        dbc.Col(create_stat_card("Learners Approved for Sponsorship", weekly_sponsored), width=6),
    ])
], fluid=True)
