import dash
from dash import dcc, html
from app_utils import *

dash.register_page(__name__, path="/onboarding-qa")

layout = html.Div([
    html.H1("Overall Onboarding Dashboard: Onboarding & QA Average Time", style={'textAlign': 'center'}),

    # Onboarding Time Summary
    html.Div([
        html.H3("Average time to complete for learners onboarding", style={'textAlign': 'center'}),
        html.P(f"Days: {onboarding_summary.get('Days', 0)}"),
        html.P(f"Met Benchmark (<=3 days): {onboarding_data.get('BenchmarkCount', {}).get('MetBenchmark (<=3 days)', 0)}"),
        html.P(f"Did Not Meet Benchmark (>3 days): {onboarding_data.get('BenchmarkCount', {}).get('DidNotMeetBenchmark (>3 days)', 0)}")
    ]),

    # QA Time Summary
    html.Div([
        html.H3("Average time to complete QA for onboarding team", style={'textAlign': 'center'}),
        html.P(f"Days: {qa_summary.get('Days', 0)}"),
        html.P(f"Met Benchmark (<=3 days): {qa_data.get('Summary', {}).get('BenchmarkCount', {}).get('MetBenchmark (<=3 days)', 0)}"),
        html.P(f"Did Not Meet Benchmark (>3 days): {qa_data.get('Summary', {}).get('BenchmarkCount', {}).get('DidNotMeetBenchmark (>3 days)', 0)}")
    ])
])
