import xml.etree.ElementTree as ET
import csv
import datetime

def analyze_flexible_zone_positions(file_path):
    counts = {
        'easting_northing_only_stops': 0,
        'lat_long_only_stops': 0,
        'both_stops': 0,
        'easting_northing_zero_stops': 0,
        'lat_long_zero_stops': 0
    }

    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        namespaces = {'n': root.tag.split('}')[0].strip('{')}  # Extract namespace

        for stop_point in root.findall('.//n:StopPoint', namespaces):
            easting_northing_found = False
            lat_long_found = False
            easting_northing_zero_found = False
            lat_long_zero_found = False

            flexible_zones = stop_point.findall('.//n:FlexibleZone', namespaces)
            for fz in flexible_zones:
                locations = fz.findall('.//n:Location', namespaces)
                for location in locations:
                    translation = location.find('.//n:Translation', namespaces)

                    easting = None
                    northing = None
                    latitude = None
                    longitude = None

                    if translation is not None:
                        easting = translation.find('n:Easting', namespaces)
                        northing = translation.find('n:Northing', namespaces)
                        latitude = translation.find('n:Latitude', namespaces)
                        longitude = translation.find('n:Longitude', namespaces)
                    else:
                        easting = location.find('n:Easting', namespaces)
                        northing = location.find('n:Northing', namespaces)

                    if easting is not None and northing is not None:
                        easting_northing_found = True
                        if easting.text == '0' or northing.text == '0':
                            easting_northing_zero_found = True
                    if latitude is not None and longitude is not None:
                        lat_long_found = True
                        if latitude.text == '0.0' or longitude.text == '0.0':
                            lat_long_zero_found = True

            # Increment the counts based on the flags
            if easting_northing_found and not lat_long_found:
                counts['easting_northing_only_stops'] += 1
            elif lat_long_found and not easting_northing_found:
                counts['lat_long_only_stops'] += 1
            elif easting_northing_found and lat_long_found:
                counts['both_stops'] += 1
            if easting_northing_zero_found:
                counts['easting_northing_zero_stops'] += 1
            if lat_long_zero_found:
                counts['lat_long_zero_stops'] += 1

        return counts

    except Exception as e:
        print(f"Error occurred: {e}")
        return counts  # Return the counts dictionary even if there is an error


def export_to_csv(data, filename):
    """
    Export a dictionary of data to a CSV file.

    Args:
    data (dict): Dictionary of data to be exported.
    filename (str): Filename for the CSV file.
    """
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for key, value in data.items():
            writer.writerow([key, value])

if __name__ == "__main__":
    # Replace this with the absolute path to your NaPTAN XML file
    file_path = 'C:\\Users\\benja\\PycharmProjects\\naptan_analysis\\data\\170124\\NaPTAN.xml'

    counts = analyze_flexible_zone_positions(file_path)

    # Export to a CSV file with a timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    csv_filename = f'flexible_zone_positions_{timestamp}.csv'
    export_to_csv(counts, csv_filename)
    print(f"Exported data to {csv_filename}")
