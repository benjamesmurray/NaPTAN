import xml.etree.ElementTree as ET
import csv
import datetime
from collections import Counter

def find_duplicates(file_path):
    """
    Find duplicate ATCO and NaPTAN codes in the NaPTAN XML file.

    Args:
    file_path (str): Path to the NaPTAN XML file.

    Returns:
    list of tuples: A list of tuples with duplicate ATCO codes.
    list of tuples: A list of tuples with duplicate NaPTAN codes.
    """
    try:
        # Parse the XML file
        tree = ET.parse(file_path)
        root = tree.getroot()
        stop_points = root.find('{http://www.naptan.org.uk/}StopPoints')

        # Counters for ATCO and NaPTAN codes
        atco_counter = Counter()
        naptan_counter = Counter()

        # Iterate over all StopPoint elements
        for stop_point in stop_points.findall('{http://www.naptan.org.uk/}StopPoint'):
            # Extract ATCO and NaPTAN codes
            atco_code_elem = stop_point.find('{http://www.naptan.org.uk/}AtcoCode')
            naptan_code_elem = stop_point.find('{http://www.naptan.org.uk/}NaptanCode')
            if atco_code_elem is not None and atco_code_elem.text:
                atco_counter[atco_code_elem.text] += 1
            if naptan_code_elem is not None and naptan_code_elem.text:
                naptan_counter[naptan_code_elem.text] += 1

        # Extract duplicates
        atco_duplicates = [(code, count) for code, count in atco_counter.items() if count > 1]
        naptan_duplicates = [(code, count) for code, count in naptan_counter.items() if count > 1]

        return atco_duplicates, naptan_duplicates

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

    atco_duplicates, naptan_duplicates = find_duplicates(file_path)

    # Export duplicates to CSV files with a timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    csv_filename_atco = f'atco_duplicates_{timestamp}.csv'
    export_to_csv(atco_duplicates, csv_filename_atco, ['ATCO Code', 'Count'])
    print(f"Exported ATCO duplicates to {csv_filename_atco}")

    csv_filename_naptan = f'naptan_duplicates_{timestamp}.csv'
    export_to_csv(naptan_duplicates, csv_filename_naptan, ['NaPTAN Code', 'Count'])
    print(f"Exported NaPTAN duplicates to {csv_filename_naptan}")
