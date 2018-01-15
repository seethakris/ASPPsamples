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
    vc = cv2.VideoCapture(0)  # Open webcam using opencv 0 = First available camera
    fps = vc.get(cv2.CAP_PROP_FPS)
    print('Frames per second is {:0.2f}'.format(fps))
    x_width = 50

    figure, ax = plt.subplots(1, 2, figsize=(10, 5))
    imstream = stream_frames(vc)
    im = ax[0].imshow(next(imstream))
    ax[0].axis('off')

    count = 0
    starttime = time.time()

    try:
        pipeline = tz.pipe(imstream,
                           c.map(lambda x: cv2.cvtColor(x, cv2.COLOR_BGR2RGB)),
                           c.map(c.do(im.set_array)),
                           c.map(lambda x: np.mean(x)),
                           c.sliding_window(x_width),
                           )

        for n, i in enumerate(pipeline):
            xdata = np.linspace(n, n + x_width, x_width)
            plot_intensity(axis=ax[1], xdata=xdata, imageintensity=i)
            plt.show(block=False)
            plt.pause(0.001)

    except KeyboardInterrupt:
        elapsedtime = time.time() - starttime
        print('The collection FPS was {:0.2f}'.format(count / elapsedtime))
        vc.release()


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
    imageintensity = np.array(imageintensity)

    # Change color of plot if intensity decreases below a threshold
    axis.plot(xdata[imageintensity < threshold], imageintensity[imageintensity < threshold], '*-', color='r')
    axis.plot(xdata[imageintensity > threshold], imageintensity[imageintensity > threshold], '.-', color='b')

    axis.set_xlim((xdata[0], xdata[-1]))  # Fix width of plotting window
    axis.set_ylabel('Average Intensity')
    axis.set_xlabel('Frames')


if __name__ == '__main__':
    display_images()
