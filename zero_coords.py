import xml.etree.ElementTree as ET
import csv
import datetime


def find_invalid_stops_and_export(xml_file_path):
    """
    Parse the XML file and find stops with invalid position values (easting, northing, latitude, or longitude)
    being some form of zero, and export the results to CSV and XML files.

    :param xml_file_path: Path to the XML file
    """
    # Parse the XML file
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    # Namespace handling for tags
    ns = {'naptan': 'http://www.naptan.org.uk/'}
    ET.register_namespace('', ns['naptan'])

    # Lists to store invalid stops and their corresponding XML elements
    invalid_stops = []
    invalid_stop_elements = []

    # Iterate through each StopPoint element
    for stop_point in root.findall('.//naptan:StopPoint', ns):
        location = stop_point.find('.//naptan:Location', ns)
        if location is not None:
            translation = location.find('naptan:Translation', ns)
            if translation is not None:
                longitude = translation.find('naptan:Longitude', ns)
                latitude = translation.find('naptan:Latitude', ns)
                easting = translation.find('naptan:Easting', ns)
                northing = translation.find('naptan:Northing', ns)

                if (longitude is not None and float(longitude.text) == 0.0) or \
                        (latitude is not None and float(latitude.text) == 0.0) or \
                        (easting is not None and float(easting.text) == 0.0) or \
                        (northing is not None and float(northing.text) == 0.0):
                    atco_code = stop_point.find('naptan:AtcoCode', ns).text
                    invalid_stops.append(atco_code)
                    invalid_stop_elements.append(stop_point)

    # Timestamp for file naming
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    # Export to CSV
    csv_file_path = f"invalid_stops_{timestamp}.csv"
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['ATCOCode'])
        for atco_code in invalid_stops:
            writer.writerow([atco_code])

    # Export to XML
    xml_file_path = f"invalid_stops_{timestamp}.xml"
    root_element = ET.Element('{http://www.naptan.org.uk/}NaPTAN')
    for stop_element in invalid_stop_elements:
        root_element.append(stop_element)
    tree = ET.ElementTree(root_element)
    tree.write(xml_file_path, encoding='utf-8', xml_declaration=True)


# Path to your NaPTAN XML dataset file
file_path = 'C:\\Users\\benja\\PycharmProjects\\naptan_analysis\\data\\170124\\NaPTAN.xml'

# Find invalid stops and export to CSV and XML
find_invalid_stops_and_export(file_path)
