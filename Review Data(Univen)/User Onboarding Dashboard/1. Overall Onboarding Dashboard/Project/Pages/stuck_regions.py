import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
from app_utils import *

dash.register_page(__name__, path="/stuck-regions")

# Data for stuck users
stuck_users_df = pd.DataFrame(list(stuck_users_counts.items()), columns=["State", "User Count"]).sort_values(by="User Count", ascending=False)

# Data for regional split
regional_df, total_learners = regional_split_learners()

layout = html.Div([
    html.H1("Users Stuck & Regional Split", style={'textAlign': 'center'}),

    # Users Stuck in Specific States (Bar Graph)
    html.Div([
        html.H3("Users Stuck in Specific States", style={'textAlign': 'center'}),
        dcc.Graph(
            figure=px.bar(
                stuck_users_df, x="State", y="User Count",
                title="Users Stuck in Various States",
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
                regional_df, x='Province', y='Count',
                title="Regional Split", labels={'Province': 'Province', 'Count': 'Learners'},
                template='plotly_white'
            )
        ),
        html.H4(f"Total Learners Across All Provinces: {total_learners}", style={'textAlign': 'center'})
    ])
])
