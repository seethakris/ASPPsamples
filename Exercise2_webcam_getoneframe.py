"""
Sample program that acquires a single image from the webcam and plots image intensity
"""

import cv2
import numpy as np
import time
import matplotlib.pyplot as plt


def display_images(method='numpy'):
    """
    Main function to call
    Obtains a single image from the function stream_frames, plots and exits
    :param method: Method to convert bgr to rgb - opencv or numpy
    """
    vc = cv2.VideoCapture(0)  # Open webcam using opencv library

    # Yield one image from generator function stream_frames
    g = stream_frames(video_capture=vc)
    bgrframe = next(g)

    # The video captured by opencv is in format bgr (blue-green-red) but matplotlib requires rgb
    starttime = time.time()  # calculate elapsed time for conversion
    rgbframe = convert_bgr_to_rgb(bgrframe, method=method)
    print(f'Time to convert using {method} = {(time.time() - starttime):0.4f} seconds')

    # Plot frame and intensity
    figure, ax = plt.subplots(1, 2, figsize=(10, 5))
    intensity = check_imageintensity(image=rgbframe[:, :, :])
    plot_image_and_brightness(axis=ax, image=rgbframe[:, :, :], imageintensity=intensity)

    g.close()  # Call GeneratorExit for cleanup


def check_imageintensity(image):
    """
    This function acquires image intensity
    :param image: rgb image
    :return: imageintensity : average intensity of image
    """

    imageintensity = np.mean(image)
    return imageintensity


def convert_bgr_to_rgb(bgr, method='numpy'):
    """
    This function converts image to RGB
    :param  bgr: bgr image
            method: specify method to convert bgr to rgb - opencv or numpy indexing
    :return: rgb image
    """

    if method == 'numpy':
        rgb = bgr  # Use numpy indexing to convert image to rgb
        # Solution:
        # rgb[:, :, [0, 1, 2]] = bgr[:, :, [2, 1, 0]]
        return rgb
    else:
        # using open cv
        rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
        return rgb


def plot_image_and_brightness(axis, image, imageintensity):
    """
    This function plots image and intensity of image
    :param  axis: figure axis for plotting
            image: rgb image
            imageintensity: intensity of image
    """
    # Plot webcam image
    axis[0].imshow(image)
    axis[0].axis('off')

    # Plot intensity of frame
    axis[1].plot(imageintensity, '*')
    axis[1].set_ylabel('Average Intensity')
    plt.show()  # To show matplotlib plot


def stream_frames(video_capture):
    """
    Generator function that captures image from webcam
    :param  video_capture: the video capture object from opencv
    :yield  frame: image from webcam
    """
    try:
        while True:
            _, frame = video_capture.read()
            yield frame
    except GeneratorExit:
        print('Closing camera..')
        video_capture.release()


display_images(method='opencv')
