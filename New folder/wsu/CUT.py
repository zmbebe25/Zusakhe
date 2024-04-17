import pdfplumber
import os
import pandas as pd

def extract_tables_to_csv(pdf_path, output_folder):
    """
    Extracts tables from all pages in a PDF file and saves them into a single CSV file.

    :param pdf_path: Path to the PDF file.
    :param output_folder: Folder where the CSV files will be saved.
    """
    rows_list = []  # Initialize an empty list to store rows
    
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages):
            tables = page.extract_tables()

            for table_index, table in enumerate(tables):
                for row in table[1:]:
                    rows_list.append(row)  # Append row to the list
                
    # Convert the list of rows into a pandas DataFrame
    combined_df = pd.DataFrame(rows_list)
    
    # Save the combined DataFrame as a CSV file
    combined_csv_path = os.path.join(output_folder, "combined_tables.csv")
    combined_df.to_csv(combined_csv_path, index=False, header=None)  # No need for header as it's not provided in the rows
    print(f"Combined tables saved to {combined_csv_path}")

# Example usage
pdf_path = "C:/Users/Zusakhe Mbebe/Downloads/29d5c50a-7541-4934-974a-a900f99686b9.pdf" 
output_folder = "DutFees"

if __name__ == "__main__":
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)  # Create the output folder if it doesn't exist
    extract_tables_to_csv(pdf_path, output_folder)
