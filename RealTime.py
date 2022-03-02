import os
import pyrealsense2 as rs
import numpy as np
import cv2
import moviepy.editor as moviepy
import glob


def adjust_gamma(image, gamma=1.3):
    """
    Use lookup table mapping the pixel values [0, 255] to their adjusted gamma values
    Bigger default gamma value means brighter img
    :param image: input image
    :param gamma: gamma value
    :return:
    """
    invGamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** invGamma) * 255
                      for i in np.arange(0, 256)]).astype("uint8")
    return cv2.LUT(image, table)


# Video file
fps = 30
string = "03.02_video_01"
avistring = "03.02_video_01.avi"
fourcc = cv2.VideoWriter_fourcc(*'MJPG')
vout = cv2.VideoWriter()

# Eye detection preprocess
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

# Configure IR stream
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.infrared, 640, 480, rs.format.y8, 30)

# Start input streaming
pipeline.start(config)

# Ignore first 1sec for camera warm-up
for i in range(30):
    frames = pipeline.wait_for_frames()
    infrared_frame = frames.first(rs.stream.infrared)
    IR_image = np.asanyarray(infrared_frame.get_data())
i = 0
try:
    while True:
        # Read image
        frames = pipeline.wait_for_frames()
        infrared_frame = frames.first(rs.stream.infrared)
        IR_image = np.asanyarray(infrared_frame.get_data())

        # Display image
        cv2.imshow('IR image', IR_image)

        # Write into pic files
        filename = "D:\\PycharmProjects\\IR\\Rec 03.03\\video\\" + str(i) + ".png"
        cv2.imwrite(filename, IR_image)
        i += 1

        # Exit on ESC key
        c = cv2.waitKey(1) % 0x100

        # Screenshot on SPACE key
        if c % 256 == 32:
            img = cv2.imshow('IR screenshot', IR_image)
            filename = "D:\\PycharmProjects\\IR\\Rec 03.03\\" + str(i) + ".png"
            cv2.imwrite(filename, IR_image)
            i += 1
        if c == 27:
            break

finally:

    pipeline.stop()
    cv2.destroyAllWindows()
vout.open(avistring, fourcc, 20.0, (640,480), True)
for j in range(0, i):
    img = cv2.imread("D:\\PycharmProjects\\IR\\Rec 03.03\\video\\" + str(j) + ".png")
    img = adjust_gamma(img)
    vout.write(img)

files = glob.glob('D:\\PycharmProjects\\IR\\Rec 03.03\\video\\*')
for f in files:
    os.remove(f)
vout.release()
clip = moviepy.VideoFileClip(avistring)
clip.write_videofile("%s.mp4" % string)
os.remove(avistring)
