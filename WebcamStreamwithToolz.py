"""
Author : Seetha Krishnan
Stream from webcam
"""
import cv2
import numpy as np
import matplotlib
import time
import toolz as tz
import toolz.curried as c

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

plt.style.use('dark_background')  # Dark background for a prettier plot


def display_images():
    """
    This function obtains results from generators and plot image and image intensity
    """
    vc = setup_camera_and_plot()
    ims = stream_frames(vc)  # Get the generator

    fig, ax = plt.subplots(1, 2, figsize=(10, 5))
    im = setup_plotting(imagestream=ims, imageaxis=ax[0], traceaxis=ax[1])

    x_width = 50
    starttime = time.time()  # Time this

    try:
        pipeline = tz.pipe(ims,
                           c.map(lambda x: cv2.cvtColor(x, cv2.COLOR_BGR2RGB)),
                           c.map(c.do(im.set_array)),
                           c.map(lambda x: np.mean(x)),
                           c.sliding_window(x_width))

        for n, i in enumerate(pipeline):
            xdata = np.linspace(n, n + x_width, x_width)
            plot_intensity(axis=ax[1], xdata=xdata, imageintensity=i)
            plt.show(block=False)
            plt.pause(0.001)

    except KeyboardInterrupt:
        elapsedtime = time.time() - starttime
        print('The collection FPS was {:0.2f}'.format(n / elapsedtime))
        vc.release()


def setup_plotting(imagestream, imageaxis, traceaxis):
    """
    Setup the plots
    :param imagestream: generator function that streams images from webcam
    :param imageaxis: axis where will be plotted
    :param traceaxis: axis where intensity trace will be plotted
    :return: imagehandle: the handle object for the axis on which webcam images are plotted
    """
    # Plot a single image to the axis to obtain an image handle
    imagehandle = imageaxis.imshow(next(imagestream))
    imageaxis.axis('off')

    # Plot 
    traceaxis.set_ylabel('Average Intensity')
    traceaxis.set_xlabel('Frames')
    traceaxis.set_title('Blue: Above threshold, Red: Below threshold')

    return imagehandle


def setup_camera_and_plot():
    """
    Opens the webcam using open cv and finds the frame rate
    :return: capture: Capture object from opencv
    """
    capture = cv2.VideoCapture(0)  # Open webcam using opencv 0 = First available camera
    fps = capture.get(cv2.CAP_PROP_FPS)
    print('Frames per second is {:0.2f}'.format(fps))

    return capture


def stream_frames(video_capture):
    """
    This generator function acquires images, convert to rgb, get mean intensity
    and yield necessary results
    :param  video_capture: the video capture object from opencv
    :yield  RGB_image
            Image Inensity
    """
    while True:
        _, frame = video_capture.read()  # Read image from webcam
        small = cv2.resize(frame, (0, 0), fx=0.8, fy=0.8)
        yield small


def plot_intensity(axis, xdata, imageintensity, threshold=40):
    """

    :param axis:
    :param xdata:
    :param imageintensity:
    :param threshold:
    :return:
    """
    imageintensity = np.array(imageintensity)

    # Change color of plot if intensity decreases below a threshold
    axis.plot(xdata[imageintensity < threshold], imageintensity[imageintensity < threshold], '*-',
              color='r', markersize=5)
    axis.plot(xdata[imageintensity > threshold], imageintensity[imageintensity > threshold], '.-',
              color='b', markersize=5)

    axis.set_xlim((xdata[0], xdata[-1]))  # Fix width of plotting window


if __name__ == '__main__':
    display_images()
