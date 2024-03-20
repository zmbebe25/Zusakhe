import pdfplumber
import csv

# Function to extract table data from the specified page
def extract_table_data(pdf_path, page_number, target_headers):
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[page_number]
        text = page.extract_text()

        # Find the start line of the table
        start_line_index = text.find("2024 UNDERGRADUATE PROSPECTUS") + len("2024 UNDERGRADUATE PROSPECTUS")
        lines = text[start_line_index:].split('\n')

        # Find the index of the first non-empty line
        for index, line in enumerate(lines):
            if line.strip():
                start_line_index += index
                break

        # Crop the page to start from the line after the specified text
        cropped_page = page.crop((0, page.bbox[3] - start_line_index, page.width, page.height))

        # Extract tables from the cropped page
        tables = cropped_page.extract_tables()

    # Check if tables were extracted
    if not tables:
        print("No tables found on the page.")
        return [], []

    # Assuming the first table is the desired one
    table = tables[0]

    # Extracting headers and data from the table
    headers = table[0]
    data = table[1:]

    # Find the indices of target headers in the actual headers
    indices = [headers.index(header) for header in target_headers]

    # Extracting only the columns with target headers
    filtered_data = [[row[index] for index in indices] for row in data]

    return target_headers, filtered_data

# Path to the PDF and the destination CSV
pdf_path = "C:/Users/Zusakhe Mbebe/Downloads/uj-undergraduate-prospectus-2024.pdf"
csv_path = "C:/Users/Zusakhe Mbebe/course-data/Zusakhe/Auto-requirements/table_data.csv"

# Headers to extract
target_headers = ['PROGRAMME', 'Qualification Code', 'Minimum APS', 'English', 'Additional Recognised Language',
                  'Mathematics', 'Mathematical Literacy', 'Technical Mathematics', 'CAREER', 'CAMPUS']

# Extracting table data from page 32
page_number = 31  # Since page numbering starts from 0
headers, data = extract_table_data(pdf_path, page_number, target_headers)

# Writing the extracted data to a CSV file
with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(headers)  # Writing headers
    writer.writerows(data)     # Writing data

print("Table data has been extracted and saved to CSV successfully.")
