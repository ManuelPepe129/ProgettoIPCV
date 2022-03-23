import math

import cv2
import time
import numpy as np
import mediapipe as mp
from HandTracking_MediaPipe import HandDetector
from VLCPlayer import VLCPlayer
from videocapture import VideoCapture


def main():

    videocapture = VideoCapture()
    handDetector = HandDetector(maxHands=1, detectionCon=0.9)
    player = VLCPlayer("videos/OP001.mp4")
    player.play()
    ROI_size = (250, 300)
    while videocapture.is_opened():
        # ottengo il frame dalla camera
        frame = videocapture.grab_frame()
        # cerco le mani con mediapipe

        # Limito la zona di input ad una ROI
        cv2.rectangle(frame, [0, 0, ROI_size[0], ROI_size[1]], (0, 255, 255), 4)
        ROI = frame[0:ROI_size[1], 0:ROI_size[0]]  # NB: la prima è y

        handDetector.findHands(ROI)
        lmList = handDetector.findPosition(ROI, draw=False, radius=8)

        if len(lmList) != 0 and not handDetector.discard:

            # Controllo che la y dell'indice sia maggiore della y del pollice
            if lmList[8][2] <= lmList[4][2]:
                # Calcolo la distanza tra pollice e indice
                thumb_index_distance = handDetector.findDistance(4, 8, frame)

                """
                    Utilizzo la distanza tra il polso e il metacarpo del mignolo
                    per normalizzare la distanza tra pollice indice
                    senza dover avere la distanza dalla camera
                """

                # Calcolo la distanza tra il polso e il metacarpo del mignolo (per normalizzare la distanza tra pollice e indice)

                dist = handDetector.findDistance(0, 17, frame, False)
                minDist = dist / 100 * 15  # distanza minima per avere volume zero
                maxDist = dist / 100 * 150  # distanza minima per avere volume massimo


                # Imposto il volume
                volume = np.interp(thumb_index_distance, [minDist, maxDist], [0, 100])
                player.set_volume(volume)

                # Disegna una barra, durante la modifica del volume, in base alla % volume
                cv2.rectangle(frame, (50, 150), (85, 400), (255, 0, 0), cv2.FILLED)
                cv2.rectangle(frame, (50, 150), (85, 400 - int(volume / 100 * 250)), (255, 255, 255), cv2.FILLED)
                cv2.putText(frame, f'{player.get_volume()}%', (40, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)


        cv2.imshow("Image", frame)
        cv2.waitKey(1)


if __name__ == "__main__":
    try:

        main()
    except KeyboardInterrupt:
        exit(0)
