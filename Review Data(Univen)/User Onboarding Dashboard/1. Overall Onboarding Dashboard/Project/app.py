import dash
from dash import dcc, html
import dash_bootstrap_components as dbc

# ✅ Initialize Dash App with Multi-Page Support
app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

# ✅ Sidebar Layout (Fixed & Well-Fitted)
sidebar = html.Div(
    [
        html.H2("User Onboarding Dashboard", className="display-6", style={'marginBottom': '20px', 'textAlign': 'center'}),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("🏠 Home", href="/", active="exact"),
                dbc.NavLink("📊 Onboarding Funnel", href="/onboarding-funnel", active="exact"),
                dbc.NavLink("📈 Conversion Rates", href="/onboarding-conversion", active="exact"),
                dbc.NavLink("🔍 Onboarding & QA", href="/onboarding-qa", active="exact"),
                dbc.NavLink("✅ Approval Process", href="/approval-process", active="exact"),
                dbc.NavLink("📂 Application Progress", href="/application-progress", active="exact"),
                dbc.NavLink("⚠️ Stuck Users & Regions", href="/stuck-regions", active="exact"),
                dbc.NavLink("📅 Weekly Updates", href="/weekly-updates", active="exact"),  # ✅ Add this line

            ],
            vertical=True,
            pills=True,
        ),
    ],
    style={
        "position": "fixed",
        "top": 0,
        "left": 0,
        "bottom": 0,
        "width": "250px",  # ✅ Adjusted width
        "padding": "20px",
        "backgroundColor": "#f8f9fa",  # ✅ Light Grey for a clean look
        "borderRight": "2px solid #ddd"  # ✅ Adds a nice separation
    }
)

# ✅ Main Content Layout (White Background)
content = html.Div(
    [
        dbc.Container(
            [
                html.Br(),
                dash.page_container  # ✅ Dynamically renders the current page
            ],
            fluid=True,
            style={"marginLeft": "270px", "padding": "20px", "backgroundColor": "white"}  # ✅ White Background
        )
    ]
)

# ✅ Define App Layout
app.layout = html.Div([sidebar, content])

# ✅ Run the App
if __name__ == '__main__':
    app.run_server(debug=True, host="0.0.0.0")
