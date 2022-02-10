import math

import cv2
import time
import numpy as np
import mediapipe as mp
from HandTracking_MediaPipe import HandDetector
from VLCPlayer import VLCPlayer
from videocapture import VideoCapture

pTime = 0
cTime = 0
videocapture = VideoCapture()
detector = HandDetector(maxHands=1)
player = VLCPlayer("videos/OP001.mp4")
player.play()
while videocapture.is_opened():
    # ottengo il frame dalla camera
    frame = videocapture.grab_frame()
    # cerco le mani con mediapipe
    frame = detector.findHands(frame)
    lmList = detector.findPosition(frame, draw=False, radius=8)

    # TODO: limitare zona input
    cv2.rectangle(frame, [0, 0, 250, 250], (0, 255, 255), 4)

    if len(lmList) != 0:
        # TODO: Controlli su posizione reciproca tra pollice e indice
        # Controllo che la y dell'indice sia maggiore della y del pollice
        if lmList[8][2] <= lmList[4][2]:
            # Calcolo la distanza tra pollice e indice
            thumb_index_distance = detector.findDistance(4, 8, frame)

            """
                utilizzo la distanza tra il polso e il metacarpo del mignolo
                per normalizzare la distanza tra pollice indice
                senza dover avere la distanza dalla camera
            """

            # Calcolo la distanza tra il polso e il metacarpo del mignolo (per normalizzare la distanza tra pollice e indice)

            dist = detector.findDistance(0, 17, frame, False)
            minDist = dist / 100 * 15  # distanza minima per avere volume zero
            maxDist = dist / 100 * 150  # distanza minima per avere volume massimo

            # TODO: provare ad usare gli ultimi N valori per impostare il volume come la media di essi

            # Imposto il volume
            volume = np.interp(thumb_index_distance, [minDist, maxDist], [0, 100])
            player.set_volume(volume)

            # TODO: disegnare barra % volume mentre si aggiorna il volume
            cv2.rectangle(frame, (50, 150), (85, 400), (255, 0, 0), cv2.FILLED)
            cv2.rectangle(frame, (50, 150), (85, 400 - int(volume / 100 * 250)), (255, 255, 255), cv2.FILLED)
            cv2.putText(frame, f'{int(volume)}%', (40, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)

    # Draw FPS
    """
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(frame, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 0, 255), 3)
    """

    cv2.imshow("Image", frame)
    cv2.waitKey(1)
