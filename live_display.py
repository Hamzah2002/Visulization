import matplotlib.pyplot as plt
import queue

def display_live_data(data_queue):
    """
    Visualize live data from the queue in 3D space.

    Parameters:
    - data_queue (queue.Queue): Queue containing the GPS data.
    """
    print("Starting live data visualization...")

    # Initialize the 3D plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.set_zlabel('Altitude (m)')

    longitudes = []
    latitudes = []
    altitudes = []

    while True:
        try:
            # Get data from the queue
            data = data_queue.get(timeout=1)
            if data is None:  # Stop signal received
                print("Received stop signal. Visualization ending.")
                break

            # Extract longitude, latitude, and altitude
            longitude, latitude, altitude = data
            print(f"Dequeued data: {longitude}, {latitude}, {altitude}")
            longitudes.append(longitude)
            latitudes.append(latitude)
            altitudes.append(altitude)

            # Update the plot
            ax.clear()
            ax.set_xlabel('Longitude')
            ax.set_ylabel('Latitude')
            ax.set_zlabel('Altitude (m)')
            ax.plot(longitudes, latitudes, altitudes, label="Rocket Path")
            ax.scatter(longitudes[-1], latitudes[-1], altitudes[-1], color="red", label="Current Position")
            ax.legend()
            plt.pause(0.1)

        except queue.Empty:
            print("Queue is empty, waiting for data...")
            continue

    print("Visualization complete.")
    plt.show()
