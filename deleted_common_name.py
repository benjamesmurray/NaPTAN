import xml.etree.ElementTree as ET
import csv
import datetime
import re

def find_atco_with_delete_in_descriptor(file_path):
    """
    Find ATCO codes with 'DELETE' or variations in the Descriptor's CommonName in the NaPTAN XML file.

    Args:
    file_path (str): Path to the NaPTAN XML file.

    Returns:
    list of tuples: A list of tuples with ATCO codes and the corresponding CommonName values.
    """
    try:
        # Parse the XML file
        tree = ET.parse(file_path)
        root = tree.getroot()
        stop_points = root.find('{http://www.naptan.org.uk/}StopPoints')

        # List to store ATCO codes with 'DELETE' or variations in Descriptor's CommonName
        atco_with_delete = []

        # Regex pattern for 'delete' or variations in any case
        delete_pattern = re.compile(r'delet\w*', re.IGNORECASE)

        # Iterate over all StopPoint elements
        for stop_point in stop_points.findall('{http://www.naptan.org.uk/}StopPoint'):
            # Extract ATCO code and Descriptor's CommonName
            atco_code_elem = stop_point.find('{http://www.naptan.org.uk/}AtcoCode')
            descriptor_elem = stop_point.find('{http://www.naptan.org.uk/}Descriptor')
            if atco_code_elem is not None and atco_code_elem.text and descriptor_elem is not None:
                common_name_elem = descriptor_elem.find('{http://www.naptan.org.uk/}CommonName')
                if common_name_elem is not None and common_name_elem.text and delete_pattern.search(common_name_elem.text):
                    atco_with_delete.append((atco_code_elem.text, common_name_elem.text))

        return atco_with_delete

    except Exception as e:
        print(f"Error occurred: {e}")
        return None

def export_to_csv(data, filename):
    """
    Export a list of tuples to a CSV file.

    Args:
    data (list of tuples): List of data to be exported.
    filename (str): Filename for the CSV file.
    """
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for atco_code, common_name in data:
            writer.writerow([atco_code, common_name])

if __name__ == "__main__":
    # Replace this with the absolute path to your NaPTAN XML file
    file_path = 'C:\\Users\\benja\\PycharmProjects\\naptan_analysis\\data\\170124\\NaPTAN.xml'

    atco_with_delete = find_atco_with_delete_in_descriptor(file_path)

    # Count and print the number of records with 'DELETE' or variations in the Descriptor's CommonName
    count_delete = len(atco_with_delete)
    print(f"Number of ATCO codes with 'DELETE' or variations in Descriptor's CommonName: {count_delete}")

    # Export to a CSV file with a timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    csv_filename = f'atco_with_delete_{timestamp}.csv'
    export_to_csv(atco_with_delete, csv_filename)
    print(f"Exported data to {csv_filename}")
