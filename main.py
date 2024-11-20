import os
import threading
import queue
import csv
from data_generator import generate_random_data
from live_display import display_live_data
import time

def main():
    """
    Main script to visualize data until the generator signals completion.
    """
    # File paths
    live_file = "data/gps_live_data.csv"
    archive_file = "data/gps_archive_data.csv"

    # Ensure the "data" directory exists
    os.makedirs(os.path.dirname(live_file), exist_ok=True)

    # Queue for communication between threads
    data_queue = queue.Queue()

    # Data generation thread
    def generate_data():
        print("Starting data generation thread...")
        # Simulate live data generation
        generate_random_data(output_file=live_file, num_rows=50, live=True, archive_file=archive_file)
        print("Data generation complete!")
        # Signal that data generation is done
        data_queue.put(None)

    # Data reading thread
    def read_data():
        print("Starting data reading thread...")
        with open(live_file, mode="r") as file:
            # Read and debug the header row
            header = file.readline().strip()
            print(f"Header row: {header}")

            while True:
                # Read a new line from the file
                line = file.readline()
                if not line:  # If no new line, wait for data
                    time.sleep(0.5)
                    continue

                # Parse the line into components
                row = line.strip().split(",")
                if len(row) == 4 and row[0] != "timestamp":  # Validate row
                    try:
                        longitude = float(row[2])
                        latitude = float(row[1])
                        altitude = float(row[3])
                        print(f"Pushing to queue: {longitude}, {latitude}, {altitude}")
                        data_queue.put((longitude, latitude, altitude))
                    except ValueError as e:
                        print(f"ValueError: {e} - Row: {row}")

                # Stop condition if generator signals completion
                if data_queue.qsize() == 0 and not file.readable():
                    break

        print("Data reading thread complete.")

    # Start data generation in a separate thread
    data_thread = threading.Thread(target=generate_data)
    data_thread.start()

    # Start data reading in a separate thread
    reader_thread = threading.Thread(target=read_data)
    reader_thread.start()

    # Start visualization on the main thread
    display_live_data(data_queue)

    # Wait for threads to finish
    data_thread.join()
    reader_thread.join()

    print("Main script complete.")

if __name__ == "__main__":
    main()
