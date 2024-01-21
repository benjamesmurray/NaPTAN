from collections import defaultdict
import xml.etree.ElementTree as ET

def find_atco_with_multiple_naptan(file_path):
    """
    Find ATCO codes that are associated with multiple NaPTAN codes in the NaPTAN XML file.

    Args:
    file_path (str): Path to the NaPTAN XML file.

    Returns:
    dict: A dictionary mapping ATCO codes to a list of corresponding NaPTAN codes.
    """
    try:
        # Parse the XML file
        tree = ET.parse(file_path)
        root = tree.getroot()
        stop_points = root.find('{http://www.naptan.org.uk/}StopPoints')

        # Dictionary to store ATCO codes mapped to NaPTAN codes
        atco_to_naptan = defaultdict(list)

        # Iterate over all StopPoint elements
        for stop_point in stop_points.findall('{http://www.naptan.org.uk/}StopPoint'):
            # Extract ATCO and NaPTAN codes
            atco_code_elem = stop_point.find('{http://www.naptan.org.uk/}AtcoCode')
            naptan_code_elem = stop_point.find('{http://www.naptan.org.uk/}NaptanCode')
            if atco_code_elem is not None and atco_code_elem.text and naptan_code_elem is not None and naptan_code_elem.text:
                atco_to_naptan[atco_code_elem.text].append(naptan_code_elem.text)

        # Filter out ATCO codes with only one corresponding NaPTAN code
        multiple_naptan_atco = {k: v for k, v in atco_to_naptan.items() if len(v) > 1}

        return multiple_naptan_atco

    except Exception as e:
        print(f"Error occurred: {e}")
        return None

if __name__ == "__main__":
    # Replace this with the absolute path to your NaPTAN XML file
    file_path = 'C:\\Users\\benja\\PycharmProjects\\naptan\\data\\271023\\NaPTAN.xml'

    multiple_naptan_atco = find_atco_with_multiple_naptan(file_path)
    for atco_code, naptan_codes in multiple_naptan_atco.items():
        print(f"ATCO Code: {atco_code}, NaPTAN Codes: {naptan_codes}")
