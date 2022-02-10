# Creators:
# - Manuel Pepe
# - Marco Cupelli

import cv2
import matplotlib.pyplot as plt
from VLCPlayer import VLCPlayer
from videocapture import VideoCapture
# import detector
from detector import Detector
import time


def main():
    videocapture = VideoCapture()

    # enable Matplotlib interactive mode
    plt.ion()

    # prep a variable for the first run
    ax_img = None

    # prep face cascade object
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye_tree_eyeglasses.xml')

    detector = Detector(face_cascade, eye_cascade, videocapture)

    presence_timer = 0
    current_time = time.time()

    player = VLCPlayer("videos/videoplayback.mp4")
    player.play()

    while videocapture.is_opened():

        elapsed_time = time.time() - current_time
        current_time = time.time()

        # get the current frame
        videocapture.grab_frame()
        videocapture.equalize_frame()
        frame_equalized = detector.draw_face_rect()

        # il video si mette in pausa se si esce dall'inquadratura della camera per un tot di secondi
        # oppure se si chiudono entrambi gli occhi

        # ottengo la faccia
        detector.detect_face()
        # se ho una faccia -> ottengo gli occhi
        if len(detector.faces) > 0:
            detector.detect_eyes()
            if len(detector.eyes) > 0:
                # ho trovato degli occhi
                presence_timer = 0
            else:
                # gli occhi sono chiusi
                presence_timer += elapsed_time
        else:
            presence_timer += elapsed_time

        print(presence_timer)
        if presence_timer >= 3:
            player.pause()
        else:
            player.play()

        if ax_img is None:
            # convert the current (first) frame in grayscale
            ax_img = plt.imshow(frame_equalized, "gray")
            plt.axis("off")  # hide axis, ticks, ...
            plt.title("Camera Capture")
            # show the plot!
            plt.show()
        else:
            # set the current frame as the data to show
            ax_img.set_data(frame_equalized)
            videocapture.update_figure()
            plt.pause(1 / 30)  # pause: 30 frames per second


if __name__ == "__main__":
    try:

        main()
    except KeyboardInterrupt:
        exit(0)
