import json
import pdfplumber

pdf_path = "C:/Users/Zusakhe Mbebe/Downloads/2024-Undergraduate-Student-Information-Brochure-final-2-003.pdf"
output_json_path = "C:/Users/Zusakhe Mbebe/Downloads/Zusakhe/Auto-requirements/Univen_page31.json"

# Open the PDF file
with pdfplumber.open(pdf_path) as pdf:
    page = pdf.pages[30]  # Note: Python is 0-indexed, so page 32 is accessed by index 31
    
    # Extract the table
    table = page.extract_table()

# Convert the table data into a list of dictionaries with keys
data = []
for row in table[1:]:  # Skipping the header row
    data.append({
        "Qualification": row[0],
        "Qualification Code": row[1],
        "Description": row[2],
        "Duration": row[3]
    })

# Write the extracted data into a JSON file
with open(output_json_path, "w") as json_file:
    json.dump(data, json_file, indent=4)

print("Extraction completed. Data saved in:", output_json_path)
