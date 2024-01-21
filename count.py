import xml.etree.ElementTree as ET
import datetime

def count_total_stops(file_path):
    """
    Count the total number of stops in the NaPTAN XML file.

    Args:
    file_path (str): Path to the NaPTAN XML file.

    Returns:
    int: The total number of stops in the dataset.
    """
    try:
        # Parse the XML file
        tree = ET.parse(file_path)
        root = tree.getroot()

        # Count the number of StopPoint elements
        stop_points = root.findall('.//{http://www.naptan.org.uk/}StopPoints/{http://www.naptan.org.uk/}StopPoint')
        return len(stop_points)

    except Exception as e:
        print(f"Error occurred: {e}")
        return None

if __name__ == "__main__":
    # Replace this with the absolute path to your NaPTAN XML file
    file_path = 'C:\\Users\\benja\\PycharmProjects\\naptan_analysis\\data\\170124\\NaPTAN.xml'

    total_stops = count_total_stops(file_path)

    # Output the total number of stops
    print(f"Total number of stops in the dataset: {total_stops}")

    # Optionally, you can also export this count to a file if needed
    # timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    # with open(f'total_stops_count_{timestamp}.txt', 'w') as file:
    #     file.write(str(total_stops))
    #     print(f"Total stops count exported to total_stops_count_{timestamp}.txt")
