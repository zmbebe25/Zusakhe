import dash
from dash import dcc, html
import dash_bootstrap_components as dbc

# ✅ Initialize Dash App with Multi-Page Support
app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

# ✅ Layout for Navigation
app.layout = dbc.Container([
    dbc.NavbarSimple(
        brand="User Onboarding Dashboard",
        brand_href="/",
        color="primary",
        dark=True,
    ),
    html.Div([
        dcc.Link("Home | ", href="/"),
        dcc.Link("Onboarding Funnel | ", href="/onboarding-funnel"),
        dcc.Link("Conversion Rates | ", href="/onboarding-conversion"),
        dcc.Link("Onboarding & QA | ", href="/onboarding-qa"),
        dcc.Link("Approval Process | ", href="/approval-process"),  
        dcc.Link("Application Progress | ", href="/application-progress"),  # ✅ NEW PAGE
        dcc.Link("Stuck Users & Regions", href="/stuck-regions"),
    ], style={'textAlign': 'center', 'padding': '10px'}),

    dash.page_container  # ✅ This renders the correct page dynamically
])

if __name__ == '__main__':
    app.run_server(debug=True, host="0.0.0.0")
