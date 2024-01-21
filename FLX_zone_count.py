import xml.etree.ElementTree as ET
import csv
import datetime

def analyze_flexible_zones(file_path):
    """
    Analyze stops with StopType BCT and BusStopType FLX, group by the number of positions, and list ATCO codes.
    Include stops that do not have a FlexibleZone as a separate group with zero locations.

    Args:
    file_path (str): Path to the NaPTAN XML file.

    Returns:
    dict: A dictionary with counts and ATCO codes grouped by the number of positions in the FlexibleZone.
    """
    counts = {}
    atco_codes_by_group = {}

    try:
        # Parse the XML file
        tree = ET.parse(file_path)
        root = tree.getroot()

        # Define the namespace
        ns = {'n': 'http://www.naptan.org.uk/'}

        # Iterate over all StopPoint elements with StopType BCT and BusStopType FLX
        for stop_point in root.findall('.//n:StopPoint', namespaces=ns):
            stop_type = stop_point.find('.//n:StopClassification/n:StopType', namespaces=ns)
            bus_stop_type = stop_point.find('.//n:StopClassification/n:OnStreet/n:Bus/n:BusStopType', namespaces=ns)

            if stop_type is not None and stop_type.text == 'BCT' and bus_stop_type is not None and bus_stop_type.text == 'FLX':
                # Get the ATCO code for the stop
                atco_code = stop_point.find('.//n:AtcoCode', namespaces=ns).text
                # Check if FlexibleZone element exists
                flexible_zone = stop_point.find('.//n:StopClassification/n:OnStreet/n:Bus/n:FlexibleZone', namespaces=ns)
                num_locations = 0 if flexible_zone is None else len(flexible_zone.findall('.//n:Location', namespaces=ns))

                # Update counts and ATCO codes by group
                counts[num_locations] = counts.get(num_locations, 0) + 1
                atco_codes_by_group.setdefault(num_locations, []).append(atco_code)

        return counts, atco_codes_by_group

    except Exception as e:
        print(f"Error occurred: {e}")
        return None, None

def export_to_csv(data, filename, header):
    """
    Export data to a CSV file.

    Args:
    data: Data to be exported.
    filename (str): Filename for the CSV file.
    header (list): Header row for the CSV file.
    """
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        for key, value in sorted(data.items()):
            if isinstance(value, list):
                for item in value:
                    writer.writerow([key, item])
            else:
                writer.writerow([key, value])

if __name__ == "__main__":
    # Replace this with the absolute path to your NaPTAN XML file
    file_path = 'C:\\Users\\benja\\PycharmProjects\\naptan_analysis\\data\\170124\\NaPTAN.xml'

    counts, atco_codes_by_group = analyze_flexible_zones(file_path)

    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    if counts is not None:
        # Export counts to a CSV file
        csv_filename_counts = f'flexible_zones_counts_{timestamp}.csv'
        export_to_csv(counts, csv_filename_counts, ['NumberOfPositions', 'Count'])
        print(f"Exported counts data to {csv_filename_counts}")

    if atco_codes_by_group is not None:
        # Export ATCO codes to a second CSV file
        csv_filename_atco_codes = f'flexible_zones_atco_codes_{timestamp}.csv'
        export_to_csv(atco_codes_by_group, csv_filename_atco_codes, ['NumberOfPositions', 'ATCOCode'])
        print(f"Exported ATCO codes data to {csv_filename_atco_codes}")
