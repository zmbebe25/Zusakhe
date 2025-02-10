import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
from pymongo import MongoClient

# MongoDB Connection
MONGO_URI = "mongodb://0.0.0.0:27017/"  # Updated for universal accessibility
app = dash.Dash(__name__, external_stylesheets=['https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css'])

def total_users_with_full_docs():
    return collection.count_documents({"FullDocs": True})

def regional_split_learners():
    return []
