import csv
import random
from datetime import datetime, timedelta
import time
import os


def generate_random_data(output_file, num_rows=100, live=False, archive_file=None):
    """
    Generate random GPS data with timestamp, latitude, longitude, and altitude.

    Parameters:
    - output_file (str): Path to save the generated data.
    - num_rows (int): Number of data points to generate.
    - live (bool): Whether to simulate real-time data generation.
    - archive_file (str): Optional path to append data to an archive file.
    """
    # Truncate the file to clear previous contents
    with open(output_file, mode='w', newline='') as live_file:
        live_file.truncate()  # Clear the file

    start_time = datetime.now()
    latitude = 42.0  # Starting latitude (adjust as needed)
    longitude = -83.0  # Starting longitude (adjust as needed)
    altitude = 100.0  # Starting altitude (adjust as needed)

    try:
        with open(output_file, mode='w', newline='') as live_file:
            live_writer = csv.writer(live_file)
            live_writer.writerow(['timestamp', 'latitude', 'longitude', 'altitude'])  # Write headers

            for i in range(num_rows):
                # Generate random data
                timestamp = start_time.strftime('%Y-%m-%dT%H:%M:%SZ')
                latitude += random.uniform(-0.0005, 0.0005)  # Random drift for latitude
                longitude += random.uniform(-0.0005, 0.0005)  # Random drift for longitude
                altitude += random.uniform(-2.0, 5.0)  # Altitude fluctuation

                # Create a new row of data
                data_row = [timestamp, round(latitude, 6), round(longitude, 6), round(altitude, 2)]

                # Write to the live data file
                live_writer.writerow(data_row)
                live_file.flush()  # Ensure data is written to disk immediately

                # Append to archive file if specified
                if archive_file:
                    append_to_archive(data_row, archive_file)

                # Print debug info if in live mode
                if live:
                    print(f"Generated live row {i + 1}: {data_row}")
                    time.sleep(0.5)  # Simulate real-time data generation

                # Increment timestamp for the next row
                start_time += timedelta(seconds=1)

    except Exception as e:
        print(f"Error generating data: {e}")


def append_to_archive(data_row, archive_file):
    """
    Append a row of data to an archive file.

    Parameters:
    - data_row (list): The data row to append.
    - archive_file (str): Path to the archive file.
    """
    try:
        with open(archive_file, mode='a', newline='') as archive:
            archive_writer = csv.writer(archive)
            # Write headers if the file is empty
            if archive.tell() == 0:
                archive_writer.writerow(['timestamp', 'latitude', 'longitude', 'altitude'])
            archive_writer.writerow(data_row)
    except Exception as e:
        print(f"Error appending to archive: {e} - Row: {data_row}")


if __name__ == "__main__":
    # File paths
    output_path = "data/gps_live_data.csv"
    archive_path = "data/gps_archive_data.csv"

    # Generate data with live simulation
    print("Generating live GPS data...")
    generate_random_data(output_file=output_path, num_rows=100, live=True, archive_file=archive_path)
    print("Data generation complete!")
