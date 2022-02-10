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
player = VLCPlayer("videos/videoplayback.mp4")
player.play()
while videocapture.is_opened():
    frame = videocapture.grab_frame()
    frame = detector.findHands(frame)
    lmList = detector.findPosition(frame, draw=False, radius=8)

    if len(lmList) != 0:
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]

        # cv2.circle(frame, (x1, y1), 10, (255, 0, 255), cv2.FILLED)
        # cv2.circle(frame, (x2, y2), 10, (255, 0, 255), cv2.FILLED)
        length = math.hypot(x2 - x1, y2 - y1)
        color = (255, 0, 255)
        """
        utilizzo la distanza tra il polso e il metacarpo del mignolo
        per normalizzare la distanza tra pollice indice
        senza dover avere la distanza dalla camera
        """
        # prendo la posizione del polso
        wrist_point = (lmList[0][1], lmList[0][2])
        # prendo la posizione del metacarpo del mignolo
        pinky_mcp_point = (lmList[17][1], lmList[17][2])
        dist = math.hypot(pinky_mcp_point[0] - wrist_point[0], pinky_mcp_point[1] - wrist_point[1])
        minDist = dist / 100 * 15  # distanza minima per avere volume zero
        maxDist = dist / 100 * 150  # distanza minima per avere volume massimo

        volume = np.interp(length, [minDist, maxDist], [0, 100])
        print(volume)
        player.set_volume(volume)
        cv2.line(frame, (x1, y1), (x2, y2), color, 3)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(frame, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 0, 255), 3)

    cv2.imshow("Image", frame)
    cv2.waitKey(1)
