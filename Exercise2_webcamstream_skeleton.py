"""
Exercise2 :
Use this skeleton and the webcam_getoneframe.py as a sample to write your own that streams continuously
from webcam and plots intensity of image across time
Hints :
1. Consolidate the functions - acquiring image, converting to rgb and calculating intensity,
into a single generator function.
2. Acquire the results of this generator function within an infinite loop.
3. Quit the loop with key press (example if statement below)
4. Yield can spit out two results. You can obtain that by
for i in g:
    print(i[0]) #First output
    print(i[1]) #Second output
"""

import cv2
import numpy as np
import matplotlib

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

plt.style.use('dark_background')  # Dark background for a prettier plot


def display_images():
    """
    Main function to call
    This function should obtain results from generators and plot image and image intensity
    Create a for loop to iterate the generator functions
    """
    vc = cv2.VideoCapture(0)  # Open webcam
    figure, ax = plt.subplots(1, 2, figsize=(10, 5))  # Intiialise plot

    count = 0  # Counter for number of aquired frames
    intensity = []  # Append intensity across time

    # For loop over generator here
    intensity.append(imageintensity)
    plot_image_and_brightness()  # Call plot function
    count += 1

    # This triggers exit sequences when user presses q
    if cv2.waitKey(1) & 0xFF == ord('q'):
        # Clean up here
        plt.close('all')  # close plots
        generator.close()  # Use generator exit for clean up,
        break  # break loop


def plot_image_and_brightness(axis, image, imageintensity, framecount):
    """
    This function plots image and intensity of image through time
    :param  axis: figure axis for plotting
            image: rgb image
            imageintensity: intensity of image
            framecount: present frame number
    """

    # Plot RGB Image
    axis[0].imshow(image)
    axis[0].axis('off')
    axis[0].set_title(f'Frame Number {framecount}')

    # Plot intensity
    axis[1].plot(imageintensity, '.-')
    axis[1].set_ylabel('Average Intensity')

    # Stuff to show and stream plot
    plt.show(block=False)
    plt.pause(0.001)


def stream_frames(video_capture):
    """
    Use an infinite loop and write a generator function that should acquire image, convert to rgb,
    get mean intensity and yield necessary results
    :param  video_capture: the video capture object from opencv
    :yield  RGB_image
            Image Intensity
    """


display_images()
