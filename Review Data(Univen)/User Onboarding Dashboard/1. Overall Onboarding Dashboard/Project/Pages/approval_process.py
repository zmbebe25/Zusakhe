import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
from pymongo import MongoClient
from dash.dependencies import Input, Output
import io

# ✅ Register Page in Dash Multi-Page App
dash.register_page(__name__, path="/approval-process")

# ✅ MongoDB Connection
mongo_uri = "mongodb+srv://zusakhe:KN3VcfCsVuyafM9l@mailserver.seham.mongodb.net/test?"
client = MongoClient(mongo_uri)
db = client["gradesmatch_core"]
users_collection = db["user"]

# ✅ Query Users Awaiting Approval (State: Staging)
awaiting_approval = users_collection.count_documents({
    "ApplicationYear": 2025,
    "School": {"$ne": None},
    "PreferredQualifications": {"$ne": None},
    "AdditionalDetails": {"$ne": None},
    "TotalDocs": {"$ne": None},
    "State": "Staging"
})

# ✅ Query Approved & Rejected Users
approved_users = users_collection.count_documents({"ApplicationYear": 2025, "State": "Approved Strategy"})
rejected_users = users_collection.count_documents({"ApplicationYear": 2025, "State": {"$in": ["Disapproved", "closed"]}})

# ✅ Query Rejection Reasons
low_maths_rejections = users_collection.count_documents({"ApplicationYear": 2025, "State": "Low Maths"})
low_average_rejections = users_collection.count_documents({"ApplicationYear": 2025, "State": "Low Average"})

# ✅ Fetch Learner Marks & Subject Data for Export
low_maths_marks_data = list(users_collection.find({
    "ApplicationYear": 2025,
    "State": "Low Maths",
    "Marks": {"$exists": True},
    "AverageMarks": {"$exists": True}
}, {"_id": 0, "Marks": 1, "AverageMarks": 1}))

low_average_marks_data = list(users_collection.find({
    "ApplicationYear": 2025,
    "State": "Low Average",
    "Marks": {"$exists": True},
    "AverageMarks": {"$exists": True}
}, {"_id": 0, "Marks": 1, "AverageMarks": 1}))

# ✅ Process Subject Marks (Fix for 'NoneType' error)
processed_marks = []
for learner in low_maths_marks_data + low_average_marks_data:  # Combine both datasets
    marks = learner.get("Marks", [])  # Ensure Marks is a list
    avg_mark = learner.get("AverageMarks", None)

    # Ensure marks exist and filter for Mathematics & Mathematical Literacy (SubjectID: 2 & 21)
    if isinstance(marks, list):
        math_subject = next((subject for subject in marks if subject.get("SubjectID") in [2, 21]), None)
        math_mark = math_subject.get("Mark") if math_subject else None
        subject_name = math_subject.get("SubjectName") if math_subject else "Unknown"
    else:
        math_mark = None
        subject_name = "Unknown"

    processed_marks.append({
        "AverageMarks": avg_mark,
        "MathsMark": math_mark,
        "Subject": subject_name
    })

marks_df = pd.DataFrame(processed_marks)

# ✅ Create Pie Chart (Approval vs. Rejection)
approval_pie_chart = px.pie(
    names=["Approved", "Rejected"],
    values=[approved_users, rejected_users],
    title="Approval vs. Rejection Rate",
    hole=0.4
)

# ✅ Create Bar Chart (Rejection Reasons)
rejection_bar_chart = px.bar(
    x=["Low Maths", "Low Average"],
    y=[low_maths_rejections, low_average_rejections],
    title="Rejection Reasons Breakdown",
    labels={"x": "Rejection Reason", "y": "Users"},
    text_auto=True
)

# ✅ Create Histogram for Average Marks Distribution (Now Matches Rejected Count)
marks_histogram = px.histogram(
    marks_df, x="AverageMarks",
    title=f"Distribution of Average Marks (Count: {len(marks_df)})",
    labels={"AverageMarks": "Average Marks"},
    nbins=10
)

# ✅ Create Maths Mark Range Bar Chart (Separate for Mathematics & Math Literacy)
maths_bar_chart = px.histogram(
    marks_df, x="MathsMark", color="Subject",
    title=f"Mathematics & Mathematical Literacy Mark Distribution (Count: {len(marks_df)})",
    labels={"MathsMark": "Marks", "Subject": "Subject"},
    nbins=10,
    barmode="group"
)

# ✅ Layout for Dashboard
layout = html.Div([
    html.H1("Approval Process Dashboard", style={'textAlign': 'center'}),

    # ✅ Key Metrics Display
    html.Div([
        html.Div([
            html.H4("Total Users Awaiting Approval"),
            html.P(f"{awaiting_approval}", style={"fontSize": "22px", "fontWeight": "bold"})
        ], className="four columns"),

        html.Div([
            html.H4("Total Approved"),
            html.P(f"{approved_users}", style={"fontSize": "22px", "fontWeight": "bold"})
        ], className="four columns"),

        html.Div([
            html.H4("Total Rejected"),
            html.P(f"{rejected_users}", style={"fontSize": "22px", "fontWeight": "bold", "color": "red"})
        ], className="four columns"),
    ], className="row", style={"marginBottom": "30px"}),

    # ✅ Approval Pie Chart
    html.Div([
        dcc.Graph(figure=approval_pie_chart)
    ], style={"marginBottom": "30px"}),

    # ✅ Rejection Reasons Bar Chart
    html.Div([
        dcc.Graph(figure=rejection_bar_chart)
    ], style={"marginBottom": "30px"}),

    # ✅ Average Marks Histogram
    html.Div([
        dcc.Graph(figure=marks_histogram)
    ], style={"marginBottom": "30px"}),

    # ✅ Maths Marks Distribution Chart (for Mathematics & Math Lit)
    html.Div([
        dcc.Graph(figure=maths_bar_chart)
    ], style={"marginBottom": "30px"}),

    # ✅ Exportable Learner Marks Table
    html.Div([
        html.H3("Learner Marks & Mathematics Performance", style={'textAlign': 'center'}),
        dcc.Download(id="download-dataframe-csv"),
        html.Button("Download Data", id="btn-download-csv", n_clicks=0),
        dcc.Graph(
            figure=px.scatter(marks_df, x="AverageMarks", y="MathsMark",
                              color="Subject",
                              title="Maths & Math Lit Marks vs Average Marks",
                              labels={"AverageMarks": "Average Marks", "MathsMark": "Marks", "Subject": "Subject"}))
    ], style={"marginBottom": "30px"})
])

# ✅ CSV Export Callback (Inline Fix)
@dash.callback(
    Output("download-dataframe-csv", "data"),
    Input("btn-download-csv", "n_clicks"),
    prevent_initial_call=True,
)
def download_csv(n_clicks):
    output = io.StringIO()
    marks_df.to_csv(output, index=False)
    return dict(content=output.getvalue(), filename="learner_marks.csv")
