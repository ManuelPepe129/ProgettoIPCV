# Creators:
# - Manuel Pepe
# - Marco Cupelli

import cv2
import matplotlib.pyplot as plt
import numpy as np
from detector import Detector
import time
from HandTracking_MediaPipe import HandDetector
from VLCPlayer import VLCPlayer
from videocapture import VideoCapture


def main():
    videocapture = VideoCapture()

    # enable Matplotlib interactive mode
    plt.ion()

    # prep a variable for the first run
    ax_img = None

    # prep face cascade object
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye_tree_eyeglasses.xml')

    # detectors
    detector = Detector(face_cascade, eye_cascade, videocapture)
    handDetector = HandDetector(maxHands=1, detectionCon=0.9)

    presence_timer = 0
    current_time = time.time()

    # creo un player con un video
    player = VLCPlayer("videos/OP001.mp4")
    # metto il video in play
    player.play()

    ROI_size = (250, 300)

    fingerIDs = [8, 12, 16, 20]

    pausedForHands = False
    pausedForPresence = False

    while videocapture.is_opened():

        elapsed_time = time.time() - current_time
        current_time = time.time()

        # get the current frame
        frame = videocapture.grab_frame()
        frame = cv2.flip(frame, +1);
        videocapture.equalize_frame()
        frame_equalized = detector.draw_face_rect()

        if not pausedForHands:
            presence_timer = face_eyes_detector(detector, elapsed_time, presence_timer)

            # print(presence_timer)
            if presence_timer >= 3:
                player.pause()
                pausedForPresence = True
            else:
                player.play()
                pausedForPresence = False
        else:
            presence_timer = 0

        """
            HAND DETECTION
        """

        cv2.rectangle(frame, [0, 0, ROI_size[0], ROI_size[1]], (0, 255, 255), 4)
        ROI = frame[0:ROI_size[1], 0:ROI_size[0]]  # NB: la prima è y

        if not pausedForPresence:
            # Limito la zona di input ad una ROI

            handDetector.findHands(ROI)
            lmList = handDetector.findPosition(ROI, draw=False, radius=8)

            if len(lmList) != 0 and not handDetector.discard:
                """
                    Controlli per volume
                """
                # Controlli su posizione reciproca tra pollice e indice
                # Controllo che la y dell'indice sia maggiore della y del pollice
                if lmList[8][2] <= lmList[4][2]:
                    # Calcolo la distanza tra pollice e indice
                    thumb_index_distance = handDetector.findDistance(4, 8, frame)

                    """
                        utilizzo la distanza tra il polso e il metacarpo del mignolo
                        per normalizzare la distanza tra pollice indice
                        senza dover avere la distanza dalla camera
                    """

                    # Calcolo la distanza tra il polso e il metacarpo del mignolo (per normalizzare la distanza tra
                    # pollice e indice)

                    dist = handDetector.findDistance(0, 17, frame, False)
                    minDist = dist / 100 * 15  # distanza minima per avere volume zero
                    maxDist = dist / 100 * 150  # distanza minima per avere volume massimo

                    # TODO: provare ad usare gli ultimi N valori per impostare il volume come la media di essi

                    # Imposto il volume
                    volume = np.interp(thumb_index_distance, [minDist, maxDist], [0, 100])
                    player.set_volume(volume)

                    # Disegna una barra in base alla % volume mentre si aggiorna
                    cv2.rectangle(frame, (50, 150), (85, 400), (255, 0, 0), cv2.FILLED)
                    cv2.rectangle(frame, (50, 150), (85, 400 - int(volume / 100 * 250)), (255, 255, 255), cv2.FILLED)
                    cv2.putText(frame, f'{player.get_volume()}%', (40, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0),
                                2)

                fingersOpened = 0
                fingersClosed = 0

                # controllo che il pollice sia aperto o chiuso
                if lmList[4][1] > lmList[3][1]:
                    fingersOpened += 1
                    print("Thumb opened")
                else:
                    fingersClosed += 1
                    print("Thumb closed")

                for finger in fingerIDs:
                    if fingersOpened >= 1 and fingersClosed >= 1:
                        break
                    elif lmList[finger][2] < lmList[finger - 2][2]:
                        fingersOpened += 1
                        print(f"Finger {finger} opened")
                    else:
                        fingersClosed += 1
                        print(f"Finger {finger} closed")

                if fingersOpened == 5:
                    player.play()
                    pausedForHands = True
                elif fingersClosed == 5:
                    player.pause()
                    pausedForHands = False

        if ax_img is None:
            ax_img = plt.imshow(frame)
            plt.axis("off")  # hide axis, ticks, ...
            plt.title("Camera Capture")
            # show the plot!
            plt.show()
        else:
            # set the current frame as the data to show
            ax_img.set_data(frame)
            videocapture.update_figure()
            plt.pause(1 / 30)  # pause: 30 frames per second


def face_eyes_detector(detector, elapsed_time, presence_timer):
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
    return presence_timer


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit(0)
