import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
from pymongo import MongoClient

# MongoDB Connection
MONGO_URI = "mongodb://localhost:27017/"  # Update with your MongoDB URI
db_name = "your_database"
collection_name = "your_collection"

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client[db_name]
collection = db[collection_name]

def fetch_data():
    """Fetch data from MongoDB and convert it into a DataFrame"""
    data = list(collection.find({}, {"_id": 0}))  # Exclude MongoDB ObjectId
    return pd.DataFrame(data) if data else pd.DataFrame(columns=["Category", "Value"])

# Initialize Dash app
app = dash.Dash(__name__)

# App Layout
app.layout = html.Div([
    html.H1("MongoDB Dashboard"),
    dcc.Dropdown(
        id='category-filter',
        options=[{'label': cat, 'value': cat} for cat in fetch_data()["Category"].unique()],
        multi=True,
        placeholder="Select Category"
    ),
    dcc.Graph(id='bar-chart')
])

# Callback to update graph
@app.callback(
    Output('bar-chart', 'figure'),
    Input('category-filter', 'value')
)
def update_graph(selected_categories):
    df = fetch_data()
    if selected_categories:
        df = df[df["Category"].isin(selected_categories)]
    
    fig = px.bar(df, x='Category', y='Value', title="Data from MongoDB")
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
