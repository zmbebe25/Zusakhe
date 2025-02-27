import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from app_utils import *

dash.register_page(__name__, path="/onboarding-qa")

# ✅ Layout for Onboarding & QA Time Analysis
layout = dbc.Container([
    html.H1("Overall Onboarding Dashboard: Onboarding & QA Average Time",
            className="text-center mb-4"),  # Centered Header with spacing

    # ✅ Two-Column Layout
    dbc.Row([
        # ✅ Onboarding Time Summary
        dbc.Col(
            dbc.Card([
                dbc.CardHeader(html.H3("Average time to complete for learners onboarding", className="text-center")),
                dbc.CardBody([
                    html.H4(f"⏳ {onboarding_summary.get('Days', 0)} Days", className="text-center text-primary"),
                    html.P(f"✅ Met Benchmark (<=3 days): {onboarding_data.get('BenchmarkCount', {}).get('MetBenchmark (<=3 days)', 0)}",
                           className="text-success text-center"),
                    html.P(f"❌ Did Not Meet Benchmark (>3 days): {onboarding_data.get('BenchmarkCount', {}).get('DidNotMeetBenchmark (>3 days)', 0)}",
                           className="text-danger text-center"),
                ])
            ], className="shadow-lg p-3 mb-5 bg-white rounded"), width=6
        ),

        # ✅ QA Time Summary
        dbc.Col(
            dbc.Card([
                dbc.CardHeader(html.H3("Average time to complete QA for onboarding team", className="text-center")),
                dbc.CardBody([
                    html.H4(f"⏳ {qa_summary.get('Days', 0)} Days", className="text-center text-primary"),
                    html.P(f"✅ Met Benchmark (<=3 days): {qa_data.get('Summary', {}).get('BenchmarkCount', {}).get('MetBenchmark (<=3 days)', 0)}",
                           className="text-success text-center"),
                    html.P(f"❌ Did Not Meet Benchmark (>3 days): {qa_data.get('Summary', {}).get('BenchmarkCount', {}).get('DidNotMeetBenchmark (>3 days)', 0)}",
                           className="text-danger text-center"),
                ])
            ], className="shadow-lg p-3 mb-5 bg-white rounded"), width=6
        )
    ], className="mb-4"),  # Row for Layout Structure

], fluid=True)  # Full width layout

