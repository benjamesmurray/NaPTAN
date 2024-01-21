import xml.etree.ElementTree as ET
import csv
import datetime
from collections import defaultdict

def find_atco_with_no_naptan_and_grouped_by_type(file_path):
    """
    Find ATCO codes that have no associated NaPTAN codes in the NaPTAN XML file,
    and group them by stop type.

    Args:
    file_path (str): Path to the NaPTAN XML file.

    Returns:
    dict: A dictionary with stop types as keys and counts of ATCO codes with no NaPTAN codes as values.
    list of tuples: A list of tuples with ATCO codes and stop types for stops with no NaPTAN codes.
    """
    try:
        # Parse the XML file
        tree = ET.parse(file_path)
        root = tree.getroot()
        stop_points = root.find('{http://www.naptan.org.uk/}StopPoints')

        # Dictionary to store counts and list to store details of ATCO codes with no NaPTAN codes, grouped by stop type
        counts_by_type = defaultdict(int)
        atco_and_type = []

        # Iterate over all StopPoint elements
        for stop_point in stop_points.findall('{http://www.naptan.org.uk/}StopPoint'):
            # Extract ATCO, NaPTAN codes, and StopType
            atco_code_elem = stop_point.find('{http://www.naptan.org.uk/}AtcoCode')
            naptan_code_elem = stop_point.find('{http://www.naptan.org.uk/}NaptanCode')
            stop_type_elem = stop_point.find('{http://www.naptan.org.uk/}StopClassification/{http://www.naptan.org.uk/}StopType')
            if atco_code_elem is not None and atco_code_elem.text and (naptan_code_elem is None or not naptan_code_elem.text):
                stop_type = stop_type_elem.text if stop_type_elem is not None else 'Unknown'
                counts_by_type[stop_type] += 1
                atco_and_type.append((atco_code_elem.text, stop_type))

        return counts_by_type, atco_and_type

    except Exception as e:
        print(f"Error occurred: {e}")
        return None, None

def export_to_csv(data, filename, column_names):
    """
    Export a list of tuples to a CSV file.

    Args:
    data (list of tuples): List of data to be exported.
    filename (str): Filename for the CSV file.
    column_names (list): Column names for the CSV file.
    """
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(column_names)
        for row in data:
            writer.writerow(row)

if __name__ == "__main__":
    # Replace this with the absolute path to your NaPTAN XML file
    file_path = 'C:\\Users\\benja\\PycharmProjects\\naptan_analysis\\data\\170124\\NaPTAN.xml'

    counts_by_type, atco_and_type = find_atco_with_no_naptan_and_grouped_by_type(file_path)

    # Export counts by type to a CSV file with a timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    csv_filename_counts = f'atco_with_no_naptan_by_type_{timestamp}.csv'
    export_to_csv(counts_by_type.items(), csv_filename_counts, ['Stop Type', 'Count'])
    print(f"Exported counts to {csv_filename_counts}")

    # Export details of stops with no NaPTAN code to a second CSV file
    csv_filename_details = f'atco_with_no_naptan_details_{timestamp}.csv'
    export_to_csv(atco_and_type, csv_filename_details, ['ATCO Code', 'Stop Type'])
    print(f"Exported details to {csv_filename_details}")
