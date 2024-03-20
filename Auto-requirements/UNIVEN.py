import json
import pdfplumber

pdf_path = "C:/Users/Zusakhe Mbebe/Downloads/2024-Undergraduate-Student-Information-Brochure-final-2-003.pdf"
output_json_path = "C:/Users/Zusakhe Mbebe/course-data/Zusakhe/Auto-requirements/Univen.json"

# Open the PDF file
with pdfplumber.open(pdf_path) as pdf:
    page = pdf.pages[12]  # Note: Python is 0-indexed, so page 32 is accessed by index 31
    
    # Extract the table
    table = page.extract_table()

# Write the extracted data into a JSON file
with open(output_json_path, "w") as json_file:
    json.dump(table, json_file, indent=4)

print("Extraction completed. Data saved in:", output_json_path)
