import xml.etree.ElementTree as ET
import csv
import datetime


def analyze_bus_stop_types(file_path):
    atco_codes = []
    matching_stops = []

    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        for stop_point in root.findall('.//{http://www.naptan.org.uk/}StopPoints/{http://www.naptan.org.uk/}StopPoint'):
            stop_type = stop_point.find(
                './/{http://www.naptan.org.uk/}StopClassification/{http://www.naptan.org.uk/}StopType')
            bus_stop_type = stop_point.find(
                './/{http://www.naptan.org.uk/}StopClassification/{http://www.naptan.org.uk/}OnStreet/{http://www.naptan.org.uk/}Bus/{http://www.naptan.org.uk/}BusStopType')

            if stop_type is not None and stop_type.text == 'BCT' and bus_stop_type is not None and bus_stop_type.text == 'FLX':
                atco_code = stop_point.find('.//{http://www.naptan.org.uk/}AtcoCode')
                if atco_code is not None:
                    atco_codes.append(atco_code.text)
                    matching_stops.append(stop_point)

        return atco_codes, matching_stops

    except Exception as e:
        print(f"Error occurred: {e}")
        return None, None


def export_to_csv(data, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['ATCOCode'])
        for item in data:
            writer.writerow([item])


def export_to_xml(stops, filename, original_namespace):
    # Register the original namespace
    ET.register_namespace('', original_namespace)

    root = ET.Element('StopPoints')
    for stop in stops:
        root.append(stop)

    tree = ET.ElementTree(root)
    tree.write(filename, encoding='utf-8', xml_declaration=True)


if __name__ == "__main__":
    file_path = 'C:\\Users\\benja\\PycharmProjects\\naptan_analysis\\data\\170124\\NaPTAN.xml'

    # Specify the original namespace (replace 'http://www.naptan.org.uk/' with the correct namespace from your data)
    original_namespace = 'http://www.naptan.org.uk/'

    atco_codes, matching_stops = analyze_bus_stop_types(file_path)

    if atco_codes is not None and matching_stops is not None:
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

        csv_filename = f'bct_flx_atco_codes_{timestamp}.csv'
        export_to_csv(atco_codes, csv_filename)
        print(f"Exported ATCO codes to {csv_filename}")

        xml_filename = f'bct_flx_stops_{timestamp}.xml'
        export_to_xml(matching_stops, xml_filename, original_namespace)
        print(f"Exported matching stops to {xml_filename}")
    else:
        print("No data to export.")

