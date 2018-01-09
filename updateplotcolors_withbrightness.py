"""
Exercise2 : Solution

"""
import cv2
import numpy as np
import matplotlib
import time

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
    figure, ax = plt.subplots(1, 2, figsize=(10, 5))
    count = 0
    intensity = []
    frametime = []

    # Define some plot parameters
    ax[1].set_xlabel('Frames')
    ax[1].set_ylabel('Average Intensity')

    starttime = time.time()
    while vc.isOpened():
        try:
            for i in stream_frames(vc):
                # i[0] : rgb image
                # i[1] : intensity of image

                # Add to a list for plotting a stream and delete when done.
                # Not the prettiest way to do this - Any better ideas?
                intensity.append(i[1])
                frametime.append(count)

                if count == 0:
                    im = plot_img(image=i[0], framecount=count, AxisHandle=ax[0])  # Plot axis for first frame
                else:
                    plot_img(image=i[0], framecount=count, AxisHandle=ax[0],
                             ImageHandle=im)  # Add data to axis for subsequent frames to speed up plotting

                # Change color of intensity trace if image intensity is lower than a threshold
                plot_intensitytrace(axis=ax[1], xdata=frametime, imageintensity=intensity, framecount=count,
                                    framespersec=fps, threshold=50)

                # Stuff to show and stream plot
                plt.show(block=False)
                plt.pause(0.001)

                if len(intensity) > fps:  # Reduce list size, if you are not going to do anything with it
                    intensity = delete_list(intensity, fps)
                    frametime = delete_list(frametime, fps)

                count += 1


        # Its ugly but does the job. If you like keypress to quit, opencv has a nice function called cv2.WaitKey
        # but it only works if you plot using opencv librabry as well
        except KeyboardInterrupt:
            elapsedtime = time.time() - starttime
            print('The collection FPS was {:0.2f}'.format(count / elapsedtime))
            vc.release()
            break


def delete_list(list, todelete):
    i = 0
    while i < todelete - 1:
        del list[0]
        i += 1
    return list


# def motiondetection(image):


def stream_frames(video_capture):
    """
    This generator function acquires images, convert to rgb, get mean intensity
    and yield necessary results
    :param  video_capture: the video capture object from opencv
    :yield  RGB_image
            Image Intensity
    """
    _, frame = video_capture.read()  # Read image from webcam
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert to rgb
    intensity = np.mean(rgb)  # Get mean intensity
    yield rgb, intensity


def plot_img(image, framecount, **kwargs):
    """
    This function plots image from the webcam
    :param  image: rgb image
            framecount: present frame number

    :kwargs AxisHandle: figure axis for plotting
            ImageHandle: image axis to plot all subsequent
                        frames after the first frame
    """

    kwargs['AxisHandle'].set_title(f'Frame Number {framecount}')
    if 'ImageHandle' in kwargs.keys():  # For all other frames
        kwargs['ImageHandle'].set_data(image)
    else:  # For first frame
        im = kwargs['AxisHandle'].imshow(image)
        kwargs['AxisHandle'].axis('off')
        return im


def plot_intensitytrace(axis, xdata, imageintensity, framecount, framespersec, threshold):
    """
    This function plots image and intensity of image through time
    :param  axis: figure axis for plotting
            imageintensity: intensity of image
            framecount: present frame number
            framepersec: Frames per second of camera to fix window width
            threshold: itensity threshold below which plot colors are changed
    """
    xdata = np.array(xdata)
    imageintensity = np.array(imageintensity)

    # Change color of plot if intensity decreases below a threshold
    axis.plot(xdata[imageintensity < threshold], imageintensity[imageintensity < threshold], '*-', color='r')
    axis.plot(xdata[imageintensity > threshold], imageintensity[imageintensity > threshold], '.-', color='b')

    axis.set_xlim((framecount - framespersec, framecount))  # Keep window size a one second


display_images()
