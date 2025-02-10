import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
from pymongo import MongoClient

# MongoDB Connection
MONGO_URI = "mongodb+srv://zusakhe:KN3VcfCsVuyafM9l@mailserver.seham.mongodb.net/test?"  # Update with your MongoDB URI
db_name = "gradesmatch_core"
collection_name = "user"

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client[db_name]
collection = db[collection_name]

def total_users_with_full_docs():
    """Count users with FullDocs=True, ApplicationYear=2025, and AverageMarks >= 55"""
    return collection.count_documents({
        "ApplicationYear": 2025,
        "FullDocs": True,
        "AverageMarks": {"$gte": 55}
    })

def total_users_awaiting_learner():
    """Count users with State='Awaiting Learner'"""
    return collection.count_documents({"State": "Awaiting Learner","ApplicationYear": 2025})

def total_users_disapproved():
    """Count users with State='Disapproved'"""
    return collection.count_documents({"State": "Disapproved","ApplicationYear": 2025})

def total_users_closed():
    """Count users with State='Closed'"""
    return collection.count_documents({"State": "Closed","ApplicationYear": 2025})

def total_learners_sponsored():
    """Count learners with Packages='Sponsored'"""
    return collection.count_documents({"Packages": "Sponsored","ApplicationYear": 2025})

def regional_split_learners():
    """Regional split of learners with complete onboarding"""
    provinces = [
        'EC', 'FS', 'GT', 'KZ', 'KZN', 'LP', 'MP', 'NC', 'NW', 'WC'
    ]
    results = []
    total_count = 0
    for province in provinces:
        count = collection.count_documents({
            "State": {
                "$in": [
                    "Staging",
                    "Approved Strategy",
                    "Awaiting Learner",
                    "Draft Strategy",
                    "Learner Approval"
                ]
            },
            "Province": province,
            "ApplicationYear": 2025
        })
        results.append({"Province": province, "Count": count})
        total_count += count
    df = pd.DataFrame(results)
    df = df.sort_values(by="Count", ascending=True)
    return df, total_count

# Initialize Dash app
app = dash.Dash(__name__)

# App Layout
app.layout = html.Div([
    html.Meta(name="viewport", content="width=device-width, initial-scale=1.0"),
    html.Div([
        html.H1("Total users onboarded", style={
            'textAlign': 'center', 'color': '#000', 'padding': '20px',
            'background': '#f0f0f0',
            'borderRadius': '15px', 'marginBottom': '30px',
            'fontFamily': 'Trebuchet MS, sans-serif', 'fontSize': '3em',
            'boxShadow': '0px 4px 6px rgba(0, 0, 0, 0.1)'
        }),
    ], style={'padding': '10px'}),

    html.Div([
        html.Div([
            html.H3("Total Users with Full Docs", style={
                'color': '#333', 'marginBottom': '10px',
                'fontFamily': 'Verdana, sans-serif', 'fontSize': '1.5em'
            }),
            html.P(f"{total_users_with_full_docs()}", style={
                'fontSize': '2em', 'fontWeight': 'bold',
                'color': '#333', 'background': '#f9f9f9',
                'padding': '20px', 'borderRadius': '15px',
                'textAlign': 'center', 'boxShadow': '0px 4px 6px rgba(0, 0, 0, 0.1)'
            })
        ], className='stat-box', style={'textAlign': 'center'}),
        html.Div([
            html.H3("Awaiting Learner State", style={
                'color': '#333', 'marginBottom': '10px',
                'fontFamily': 'Verdana, sans-serif', 'fontSize': '1.5em'
            }),
            html.P(f"{total_users_awaiting_learner()}", style={
                'fontSize': '2em', 'fontWeight': 'bold',
                'color': '#333', 'background': '#f9f9f9',
                'padding': '20px', 'borderRadius': '15px',
                'textAlign': 'center', 'boxShadow': '0px 4px 6px rgba(0, 0, 0, 0.1)'
            })
        ], className='stat-box', style={'textAlign': 'center'}),
        html.Div([
            html.H3("Disapproved State", style={
                'color': '#333', 'marginBottom': '10px',
                'fontFamily': 'Verdana, sans-serif', 'fontSize': '1.5em'
            }),
            html.P(f"{total_users_disapproved()}", style={
                'fontSize': '2em', 'fontWeight': 'bold',
                'color': '#333', 'background': '#f9f9f9',
                'padding': '20px', 'borderRadius': '15px',
                'textAlign': 'center', 'boxShadow': '0px 4px 6px rgba(0, 0, 0, 0.1)'
            })
        ], className='stat-box', style={'textAlign': 'center'}),
        html.Div([
            html.H3("Closed State", style={
                'color': '#333', 'marginBottom': '10px',
                'fontFamily': 'Verdana, sans-serif', 'fontSize': '1.5em'
            }),
            html.P(f"{total_users_closed()}", style={
                'fontSize': '2em', 'fontWeight': 'bold',
                'color': '#333', 'background': '#f9f9f9',
                'padding': '20px', 'borderRadius': '15px',
                'textAlign': 'center', 'boxShadow': '0px 4px 6px rgba(0, 0, 0, 0.1)'
            })
        ], className='stat-box', style={'textAlign': 'center'}),
        html.Div([
            html.H3("Learners Approved for Sponsorship", style={
                'color': '#333', 'marginBottom': '10px',
                'fontFamily': 'Verdana, sans-serif', 'fontSize': '1.5em'
            }),
            html.P(f"{total_learners_sponsored()}", style={
                'fontSize': '2em', 'fontWeight': 'bold',
                'color': '#333', 'background': '#f9f9f9',
                'padding': '20px', 'borderRadius': '15px',
                'textAlign': 'center', 'boxShadow': '0px 4px 6px rgba(0, 0, 0, 0.1)'
            })
        ], className='stat-box', style={'textAlign': 'center'}),
    ], style={
        'display': 'grid', 'gridTemplateColumns': 'repeat(auto-fit, minmax(250px, 1fr))',
        'gap': '20px', 'padding': '20px'
    }),

    html.Div([
        html.H3("Regional Split of Learners with Complete Onboarding", style={
            'textAlign': 'center', 'color': '#333', 'marginBottom': '20px',
            'fontFamily': 'Trebuchet MS, sans-serif', 'fontSize': '2em'
        }),
        dcc.Graph(
            id='regional-split-chart',
            figure=px.bar(
                regional_split_learners()[0], x='Province', y='Count',
                title="Regional Split", labels={'Province': 'Province', 'Count': 'Learners'},
                template='plotly_white'
            )
        ),
        html.H4(f"Total Learners Across All Provinces: {regional_split_learners()[1]}", style={
            'textAlign': 'center', 'color': '#333', 'marginTop': '20px',
            'fontFamily': 'Verdana, sans-serif', 'fontSize': '1.5em',
            'background': '#f9f9f9',
            'padding': '10px', 'borderRadius': '15px',
            'boxShadow': '0px 4px 6px rgba(0, 0, 0, 0.1)'
        })
    ], style={
        'marginTop': '30px', 'padding': '20px', 'background': '#f9f9f9',
        'borderRadius': '15px', 'boxShadow': '0px 4px 6px rgba(0, 0, 0, 0.1)'
    })
], style={
    'fontFamily': 'Arial, sans-serif', 'background': '#fff',
    'color': '#333', 'minHeight': '100vh',
    'padding': '20px', 'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center'
})

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, host="0.0.0.0")
