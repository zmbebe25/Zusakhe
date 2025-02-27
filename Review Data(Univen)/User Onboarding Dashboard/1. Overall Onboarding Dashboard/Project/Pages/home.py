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
    
    # Page Title
    html.H1("Overall Onboarding Dashboard", style={'textAlign': 'center', 'fontSize': '32px', 'fontWeight': 'bold'}),

    # Key Statistics
    html.Div([
        html.Div([
            html.H3("📄 Total Users with Full Docs", style={'fontSize': '20px', 'fontWeight': 'bold'}),
            html.P(total_users_with_full_docs(), style={'fontSize': '18px'}),
            html.P(f"📅 Daily: {daily_users_with_full_docs()}", style={'color': 'gray'})
        ], className='stat-box'),

        html.Div([
            html.H3("⏳ Awaiting Learner State", style={'fontSize': '20px', 'fontWeight': 'bold'}),
            html.P(total_users_awaiting_learner(), style={'fontSize': '18px'}),
            html.P(f"📅 Daily: {daily_users_awaiting_learner()}", style={'color': 'gray'})
        ], className='stat-box'),

        html.Div([
            html.H3("❌ Disapproved State", style={'fontSize': '20px', 'fontWeight': 'bold'}),
            html.P(total_users_disapproved(), style={'fontSize': '18px'}),
            html.P(f"📅 Daily: {daily_users_disapproved()}", style={'color': 'gray'})
        ], className='stat-box'),

        html.Div([
            html.H3("🚫 Closed State", style={'fontSize': '20px', 'fontWeight': 'bold'}),
            html.P(total_users_closed(), style={'fontSize': '18px'}),
            html.P(f"📅 Daily: {daily_users_closed()}", style={'color': 'gray'})
        ], className='stat-box'),

        html.Div([
            html.H3("🎓 Learners Approved for Sponsorship", style={'fontSize': '20px', 'fontWeight': 'bold'}),
            html.P(total_learners_sponsored(), style={'fontSize': '18px'}),
            html.P(f"📅 Daily: {daily_learners_sponsored()}", style={'color': 'gray'})
        ], className='stat-box'),

    ], style={'display': 'flex', 'justifyContent': 'space-around', 'flexWrap': 'wrap', 'padding': '20px'}),

    # Definition Section
        html.Div([
            html.H3("📉 Drop-off Rates at Each Onboarding Stage", 
                    style={'textAlign': 'center', 'fontSize': '26px', 'fontWeight': 'bold'}),
            html.P(
                "The drop-off rate represents the number of users who abandon the onboarding process at each stage. "
                "Measured from Sign-ups through State Approval, this metric reflects user engagement across key milestones: "
                "personal info, education details, additional details, document submission, and final state transition.",
                style={'textAlign': 'center', 'fontSize': '18px', 'maxWidth': '80%', 'margin': 'auto'}
            )
        ], style={'padding': '20px'}),
    # Drop-Off Funnel Chart
    html.Div([
        html.H3("🔻 Onboarding Drop-Off Funnel", style={'textAlign': 'center', 'fontSize': '24px', 'fontWeight': 'bold'}),
        dcc.Graph(figure=px.funnel(funnel_df, x="Users", y="Stage"))
    ], style={'padding': '20px'})
])

