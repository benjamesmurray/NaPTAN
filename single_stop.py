import xml.etree.ElementTree as ET
import datetime


def extract_atco_code_data(file_path, atco_code):
    """
    Extract and print data for a specific ATCO code to a .txt file, without namespace prefixes.

    Args:
    file_path (str): Path to the NaPTAN XML file.
    atco_code (str): The ATCO code to search for.
    """
    try:
        # Parse the XML file
        tree = ET.parse(file_path)
        root = tree.getroot()

        # Define the namespace
        ns = {'n': 'http://www.naptan.org.uk/'}

        # Find the StopPoint with the specified ATCO code
        stop_point = root.find(f".//n:StopPoints/n:StopPoint[n:AtcoCode='{atco_code}']", namespaces=ns)
        if stop_point is not None:
            # Register namespace to prevent ns0 prefix
            ET.register_namespace('', 'http://www.naptan.org.uk/')

            # Get all data for this StopPoint as a string
            stop_point_data = ET.tostring(stop_point, encoding='unicode', method='xml')

            # Export to a .txt file with a timestamp
            timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            txt_filename = f'atco_code_{atco_code}_{timestamp}.txt'
            with open(txt_filename, 'w') as file:
                file.write(stop_point_data)
                print(f"Data for ATCO code {atco_code} exported to {txt_filename}")
        else:
            print(f"No data found for ATCO code {atco_code}")

    except Exception as e:
        print(f"Error occurred: {e}")


if __name__ == "__main__":
    # Replace this with the absolute path to your NaPTAN XML file
    file_path = 'C:\\Users\\benja\\PycharmProjects\\naptan_analysis\\data\\170124\\NaPTAN.xml'
    # Replace this with the ATCO code you want to search for
    atco_code = '260000T11'

    extract_atco_code_data(file_path, atco_code)
