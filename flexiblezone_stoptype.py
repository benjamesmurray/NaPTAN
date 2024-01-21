import xml.etree.ElementTree as ET
import csv
import datetime
from collections import defaultdict

def analyze_stops_with_flexible_zone(file_path):
    """
    Analyze stops with FlexibleZone element in the NaPTAN XML file, counting them by BusStopType.

    Args:
    file_path (str): Path to the NaPTAN XML file.

    Returns:
    dict: A dictionary with BusStopType as keys and counts of stops with FlexibleZone as values.
    """
    try:
        # Parse the XML file
        tree = ET.parse(file_path)
        root = tree.getroot()
        stop_points = root.find('{http://www.naptan.org.uk/}StopPoints')

        # Dictionary to store counts of stops with FlexibleZone, grouped by BusStopType
        bus_stop_type_counts = defaultdict(int)

        # Iterate over all StopPoint elements
        for stop_point in stop_points.findall('{http://www.naptan.org.uk/}StopPoint'):
            # Check for FlexibleZone element
            flexible_zone_elem = stop_point.find('{http://www.naptan.org.uk/}StopClassification/{http://www.naptan.org.uk/}OnStreet/{http://www.naptan.org.uk/}Bus/{http://www.naptan.org.uk/}FlexibleZone')
            if flexible_zone_elem is not None:
                # Get BusStopType
                bus_stop_type_elem = stop_point.find('{http://www.naptan.org.uk/}StopClassification/{http://www.naptan.org.uk/}OnStreet/{http://www.naptan.org.uk/}Bus/{http://www.naptan.org.uk/}BusStopType')
                bus_stop_type = bus_stop_type_elem.text if bus_stop_type_elem is not None else 'Unknown'
                bus_stop_type_counts[bus_stop_type] += 1

        return bus_stop_type_counts

    except Exception as e:
        print(f"Error occurred: {e}")
        return None

def export_to_csv(data, filename, column_names):
    """
    Export a list of tuples to a CSV file.

    Args:
    data (iterable of tuples): Iterable of key-value pairs (from a dictionary) to be exported.
    filename (str): Filename for the CSV file.
    column_names (list): Column names for the CSV file.
    """
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(column_names)
        for bus_stop_type, count in data:
            writer.writerow([bus_stop_type, count])

if __name__ == "__main__":
    # Replace this with the absolute path to your NaPTAN XML file
    file_path = 'C:\\Users\\benja\\PycharmProjects\\naptan_analysis\\data\\170124\\NaPTAN.xml'

    bus_stop_type_counts = analyze_stops_with_flexible_zone(file_path)

    # Export to a CSV file with a timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    csv_filename = f'bus_stop_type_with_flexible_zone_{timestamp}.csv'
    export_to_csv(bus_stop_type_counts.items(), csv_filename, ['BusStopType', 'Count of Stops with FlexibleZone'])
    print(f"Exported data to {csv_filename}")
