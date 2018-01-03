## Sample program that acquires a single image from the webcam

import cv2
import numpy as np
import time
import matplotlib.pyplot as plt


def display_images(method='numpy'):
    vc = cv2.VideoCapture(0)
    # Generate just one image
    g = stream_frames(video_capture=vc)
    bgrframe = next(g)  # Generate an image from the webcam

    ## The video captured is in format bgr but matplotlib requires rgb
    starttime = time.time()
    rgbframe = convert_bgr_to_rgb(bgrframe, method=method)
    print(f'Time to convert using {method} = {(time.time() - starttime):0.4f} seconds')

    # Plot frame
    figure, ax = plt.subplots(1, 2, figsize=(10, 5))
    intensity = check_imageintensity(image=rgbframe[:, :, :])  # Try plotting different
    plot_image_and_brightness(axis=ax, image=rgbframe[:, :, :], imageintensity=intensity)

    g.close()


def check_imageintensity(image):
    # This function acquires image intensity
    imageintensity = np.mean(image)
    return imageintensity


def convert_bgr_to_rgb(bgr, method='numpy'):
    # This function converts image to RGB
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
    # Plot webcam image
    axis[0].imshow(image)
    axis[0].axis('off')

    # Plot intensity of frame
    axis[1].plot(imageintensity, '*')
    axis[1].set_ylabel('Average Intensity')
    plt.show()  # To show matplotlib plot


def stream_frames(video_capture):
    # This function acquires image
    try:
        while True:
            _, frame = video_capture.read()
            yield frame
    except GeneratorExit:
        print('Closing camera..')
        video_capture.release()


display_images(method='opencv')

