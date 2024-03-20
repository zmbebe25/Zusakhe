import pdfplumber
import json

pdf_path = "C:/Users/Zusakhe Mbebe/Downloads/REVISED-2024-ACADEMIC-CALENDAR.pdf"

# Initialize a variable to hold the specific Thursday event
thursday_event = ""

# Open the PDF file
with pdfplumber.open(pdf_path) as pdf:
    # Access the specific page
    page = pdf.pages[9]  # Page 10 in the document
    
    # Extract tables from the page
    tables = page.extract_tables()

    # Assuming the first table is the one of interest and that the event is in the second row of table data
    # Considering the header row as the first row, the event you're interested in is in the second row (index 1)
    # Thursday is the 5th column (index 4)
    if tables and len(tables[0]) > 1:
        thursday_event = tables[0][1][4]  # Row 2, Thursday column

# Prepare the event for JSON output
event_json = json.dumps({"Thursday_Event": thursday_event}, indent=4)

# Print the JSON string
print(event_json)
