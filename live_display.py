import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import queue

def display_live_data(data_queue):
    """
    Visualize live data from the queue in 3D space with a properly aligned and fixed-size rocket image.
    Parameters:
    - data_queue (queue.Queue): Queue containing the GPS data.
    """
    print("Starting live data visualization...")

    # Load the rocket image and rotate it to align vertically
    rocket_image_path = "rocket.png"  # Image file path
    rocket_img = Image.open(rocket_image_path).convert("RGBA")  # Ensure transparency
    rocket_img = rocket_img.rotate(90, expand=True)  # Rotate to point upward (Z-axis)
    rocket_img = rocket_img.resize((40, 120))  # Fixed size
    rocket_img = np.array(rocket_img) / 255.0  # Normalize image for matplotlib

    # Ensure transparency (remove any black background artifacts)
    alpha_channel = rocket_img[..., 3]  # Extract alpha (transparency) channel
    rocket_img[alpha_channel == 0] = [0, 0, 0, 0]  # Set fully transparent pixels to 0

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
            ax.plot(longitudes, latitudes, altitudes, label="Rocket Path", alpha=0.7)

            # Place the rocket image at the last position
            img_x, img_y, img_z = longitudes[-1], latitudes[-1], altitudes[-1]

            # Fixed size for rocket image
            img_width, img_height = 0.0001, 0.0002  # Small fixed dimensions
            X, Y = np.meshgrid(
                np.linspace(img_x - img_width, img_x + img_width, rocket_img.shape[1]),
                np.linspace(img_y - img_height, img_y + img_height, rocket_img.shape[0]),
            )
            Z = np.full_like(X, img_z)  # Constant altitude for the image plane

            # Add image as a surface
            ax.plot_surface(
                X, Y, Z,
                rstride=1, cstride=1,
                facecolors=rocket_img,
                shade=False,
            )

            plt.pause(0.05)  # Reduce lag with shorter pause time

        except queue.Empty:
            print("Queue is empty, waiting for data...")
            continue

    print("Visualization complete.")
    plt.show()