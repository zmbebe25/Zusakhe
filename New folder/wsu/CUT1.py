import csv
import json

def csv_to_json(csv_file_path, json_file_path):
    """
    Converts a CSV file to JSON format, using the first row of the CSV as keys for the JSON objects.

    :param csv_file_path: Path to the source CSV file.
    :param json_file_path: Path where the output JSON file will be saved.
    """
    # Initialize an empty list to store the converted rows
    data = []

    # Open the CSV file and read data
    with open(csv_file_path, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        
        # Convert each row into a dictionary with keys from the first row and append to data list
        for row in csv_reader:
            data.append(row)

    # Open the JSON file and write data
    #Run Once, after running it change "mode='w'" to "mode='a'"
    with open(json_file_path, mode='w', encoding='utf-8') as json_file:
        json_file.write(json.dumps(data, indent=4))

# Example usage
csv_file_path = 'C:/Users/Zusakhe Mbebe/Downloads/Zusakhe/DutFees/table_page_1_table_1.csv' # Update this path to your actual CSV file path'
json_file_path = 'DUT_output.json'  # Update this path to your desired JSON output file path

csv_to_json(csv_file_path, json_file_path)