import xml.etree.ElementTree as ET


def count_inactive_stops(xml_file_path):
    """
    Parse the XML file and count the number of stops with the status "inactive".

    :param xml_file_path: Path to the XML file
    :return: Count of inactive stops
    """
    # Parse the XML file
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    # Namespace handling for tags
    ns = {'naptan': 'http://www.naptan.org.uk/'}

    # Counter for inactive stops
    inactive_stops_count = 0

    # Iterate through each StopPoint element
    for stop_point in root.findall('.//naptan:StopPoint', ns):
        status = stop_point.get('Status')
        if status and status.lower() == 'inactive':
            inactive_stops_count += 1

    return inactive_stops_count


# Path to your NaPTAN XML dataset file
file_path = 'C:\\Users\\benja\\PycharmProjects\\naptan_analysis\\data\\170124\\NaPTAN.xml'

# Count inactive stops
inactive_stops_count = count_inactive_stops(file_path)

# Print the count of inactive stops
print(f"Number of inactive stops: {inactive_stops_count}")
