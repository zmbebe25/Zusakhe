import json
import pdfplumber

pdf_path = "C:/Users/Zusakhe Mbebe/Downloads/uj-undergraduate-prospectus-2024.pdf"
output_json_path = "C:/Users/Zusakhe Mbebe/course-data/Zusakhe/Auto-requirements/Zusakhe.json"

# Define the pages you want to extract
pages_to_extract = [33, 34, 35,41]

# Open the PDF file
with pdfplumber.open(pdf_path) as pdf:
    # Iterate over the specified pages
    for page_number in pages_to_extract:
        page = pdf.pages[page_number - 1]  # Adjust index since pages are zero-indexed
        
        # Extract the table
        table = page.extract_table()
        
        # Convert the table to a list of dictionaries
        table_data = []
        for row in table:
            # Replace None values with an empty string
            row = ["" if cell is None else cell for cell in row]
            # Convert each row to a dictionary with column names as keys
            row_dict = dict(zip(range(len(row)), row))
            # Reverse specific fields
            keys_to_reverse = [1, 3, 4, 5, 6, 7]
            for key in keys_to_reverse:
                if key in row_dict:
                    row_dict[key] = row_dict[key][::-1]  # Reverse the string
            table_data.append(row_dict)
        
        # Write the extracted data into a JSON file
        json_filename = f"Page{page_number}.json"
        with open(output_json_path + json_filename, "w") as json_file:
            json.dump(table_data, json_file, indent=4)

print("Extraction completed. Data saved in:", output_json_path)
