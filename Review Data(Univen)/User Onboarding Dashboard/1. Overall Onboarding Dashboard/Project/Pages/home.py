import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
from app_utils import *

dash.register_page(__name__, path="/")

# Prepare Drop-Off Funnel Data
stage_counts = dropoff_data.get("StageCounts", {})
funnel_df = pd.DataFrame({
    "Stage": list(stage_counts.keys()),
    "Users": list(stage_counts.values())
})

layout = html.Div([
    html.H1("", style={'textAlign': 'center'}),

    # Main Statistics
    html.Div([
        html.Div([html.H3("Total Users with Full Docs"), html.P(total_users_with_full_docs()), html.P(f"Daily: {daily_users_with_full_docs()}")], className='stat-box'),
        html.Div([html.H3("Awaiting Learner State"), html.P(total_users_awaiting_learner()), html.P(f"Daily: {daily_users_awaiting_learner()}")], className='stat-box'),
        html.Div([html.H3("Disapproved State"), html.P(total_users_disapproved()), html.P(f"Daily: {daily_users_disapproved()}")], className='stat-box'),
        html.Div([html.H3("Closed State"), html.P(total_users_closed()), html.P(f"Daily: {daily_users_closed()}")], className='stat-box'),
        html.Div([html.H3("Learners Approved for Sponsorship"), html.P(total_learners_sponsored()), html.P(f"Daily: {daily_learners_sponsored()}")], className='stat-box'),
    ], style={'display': 'flex', 'justifyContent': 'space-around'}),

    # Drop-Off Funnel Chart
    html.Div([
        html.H3("Drop-off rates at each onboarding stage (e.g., personal info, document submission)", style={'textAlign': 'center'}),
        dcc.Graph(figure=px.funnel(funnel_df, x="Users", y="Stage"))
    ])
])
