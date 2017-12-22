import matplotlib
import cv2
import datetime
import numpy as np
# Install pyserial to connect with arduino
import serial

matplotlib.use('TKAgg')
import matplotlib.pyplot as plt

plt.style.use('dark_background')


def stream_frames(video_capture):
    while True:
        _, frame = video_capture.read()
        yield frame


def display_images(maxtime, threshold=10):
    video_capture = cv2.VideoCapture(0)
    starttime = datetime.datetime.now()
    count = 1
    intensity = []
    figure, ax = plt.subplots(1, 2, figsize=(10, 5))
    for frame in stream_frames(video_capture):
        elapsed = (datetime.datetime.now() - starttime).total_seconds()
        intensity.append(check_imageintensity(image=frame, threshold=threshold))
        plot_image_and_brightness(ax, frame, intensity, count)
        count += 1
        if elapsed > maxtime:
            video_capture.release()
            plt.close('all')
            break


def check_imageintensity(image, threshold):
    imageintensity = np.mean(image)
    print(imageintensity)
    if imageintensity < threshold:
        ## Arduino or servo motor codes go here
        print('ZERO!!!')
    return imageintensity


def plot_image_and_brightness(axis, image, imageintensity, framecount):
    axis[0].imshow(image)
    axis[0].axis('off')
    axis[0].set_title(f'Frame Number {framecount}')

    axis[1].plot(imageintensity)
    plt.tight_layout()
    plt.draw()
    plt.pause(0.001)


capturetime = 10  # in seconds
intensitythreshold = 10  # Intensity below which a ttl pulse is sent to the arduino
elapsedtime = display_images(maxtime=capturetime, threshold=intensitythreshold)
