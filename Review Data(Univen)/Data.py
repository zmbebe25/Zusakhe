import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd

# Load data
data = pd.DataFrame({
    'Category': ['A', 'B', 'C', 'D'],
    'Value': [10, 20, 30, 40]
})

# Initialize the app
app = dash.Dash(__name__)

# Create layout
app.layout = html.Div([
    html.H1("Dashboard Example"),
    dcc.Graph(
        figure=px.bar(data, x='Category', y='Value', title="Sample Bar Chart")
    )
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
