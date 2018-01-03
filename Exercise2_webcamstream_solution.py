"""
Exercise2 : Solution

"""
import cv2
import numpy as np
import matplotlib

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

plt.style.use('dark_background')  # Dark background for a prettier plot


def display_images():
    """
    This function obtains results from generators and plot image and image intensity
    """
    vc = cv2.VideoCapture(0)  # Open webcam using opencv 0 = First available camera
    figure, ax = plt.subplots(1, 2, figsize=(10, 5))

    count = 0
    intensity = []
    g = stream_frames(vc)

    for i in g:
        # i[0] : rgb image
        # i[1] : intensity of image
        intensity.append(i[1])
        plot_image_and_brightness(axis=ax, image=i[0], imageintensity=intensity, framecount=count)
        count += 1
        if cv2.waitKey(1) & 0xFF == ord('q'):
            # Clean up if q is pressed
            plt.close('all')
            g.close()
            break

def stream_frames(video_capture):
    """
    This generator function acquires images, convert to rgb, get mean intensity
    and yield necessary results
    :param  video_capture: the video capture object from opencv
    :yield  RGB_image
            Image Intensity
    """
    try:
        while True:
            _, frame = video_capture.read()  # Read image from webcam
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert to rgb
            intensity = np.mean(rgb)  # Get mean intensity
            yield rgb, intensity
    except GeneratorExit:
        print('Closing Cameras')
        video_capture.release()


def plot_image_and_brightness(axis, image, imageintensity, framecount):
    """
    This function plots image and intensity of image through time
    :param  axis: figure axis for plotting
            image: rgb image
            imageintensity: intensity of image
            framecount: present frame number
    """

    # Plot RGB image
    axis[0].imshow(image)
    axis[0].axis('off')
    axis[0].set_title(f'Frame Number {framecount}')

    # Plot intensity
    axis[1].plot(imageintensity, '.-')
    axis[1].set_ylabel('Average Intensity')

    # Stuff to show and stream plot
    plt.show(block=False)
    plt.pause(0.001)


display_images()
