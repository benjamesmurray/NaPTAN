import xml.etree.ElementTree as ET

def count_unique_codes(file_path):
    """
    Count unique ATCO and NaPTAN codes in the given NaPTAN XML file.

    Args:
    file_path (str): Path to the NaPTAN XML file.

    Returns:
    tuple: A tuple containing the count of unique ATCO codes and unique NaPTAN codes.
    """
    try:
        # Parse the XML file
        tree = ET.parse(file_path)
        root = tree.getroot()
        stop_points = root.find('{http://www.naptan.org.uk/}StopPoints')

        # Initialize sets to store unique codes
        atco_codes = set()
        naptan_codes = set()

        # Iterate over all StopPoint elements
        for stop_point in stop_points.findall('{http://www.naptan.org.uk/}StopPoint'):
            # Extract ATCO code
            atco_code_elem = stop_point.find('{http://www.naptan.org.uk/}AtcoCode')
            if atco_code_elem is not None and atco_code_elem.text:
                atco_codes.add(atco_code_elem.text)

            # Extract NaPTAN code
            naptan_code_elem = stop_point.find('{http://www.naptan.org.uk/}NaptanCode')
            if naptan_code_elem is not None and naptan_code_elem.text:
                naptan_codes.add(naptan_code_elem.text)

        return len(atco_codes), len(naptan_codes)

    except Exception as e:
        print(f"Error occurred: {e}")
        return None

if __name__ == "__main__":
    # Replace this with the absolute path to your NaPTAN XML file
    file_path = 'C:\\Users\\benja\\PycharmProjects\\naptan_analysis\\data\\170124\\NaPTAN.xml'


    unique_atco_count, unique_naptan_count = count_unique_codes(file_path)
    if unique_atco_count is not None and unique_naptan_count is not None:
        print(f"Unique ATCO Codes: {unique_atco_count}")
        print(f"Unique NaPTAN Codes: {unique_naptan_count}")
