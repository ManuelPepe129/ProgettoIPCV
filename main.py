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
from collections import Counter
import sys


def main():
    videocapture = VideoCapture()

    # Abilito la modalità interattiva di matplotlib
    plt.ion()

    # Creo una variabile per il primo run
    ax_img = None

    # Creazione dell'oggetto face cascade e dell'oggetto eye cascade
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye_tree_eyeglasses.xml')

    # Detectors
    detector = Detector(face_cascade, eye_cascade, videocapture)
    handDetector = HandDetector(maxHands=1, detectionCon=0.9)

    presence_timer = 0
    current_time = time.time()

    # Creo un player con un video
    if len(sys.argv) > 1:
        player = VLCPlayer(sys.argv[1])
    else:
        player = VLCPlayer("videos/videoplayback.mp4")


    # Metto il video in play
    player.play()

    # Definisco la grandezza (x, y) della regione d'interesse
    ROI_size = (250, 300)

    # Individuo i punti corrispondenti alle punte delle dita 
    fingerIDs = [4, 8, 12, 16, 20]

    pausedForHands = False
    pausedForPresence = False

    while videocapture.is_opened():

        # Creo una variabile che definisce il tempo trascorso
        elapsed_time = time.time() - current_time
        current_time = time.time()

        # Ottengo il frame corrente e lo equalizzo
        frame = videocapture.grab_frame()

        # frame = cv2.flip(frame, +1)
        videocapture.equalize_frame()
        detector.draw_face_rect()

        # Verifico che non sia stato impartito un comando di pausa con la mano
        if not pausedForHands:

            presence_timer = face_eyes_detector(detector, elapsed_time, presence_timer)

            # Se non vengono rilavati gli occhi e il volto per un numero di secondi
            # il video viene messo automaticamente in pausa
            if presence_timer >= 3:
                player.pause()
                pausedForPresence = True
            else:
                player.play()
                pausedForPresence = False
        else:
            presence_timer = 0

        # # #    HAND DETECTION    # # #

        # Definisco la regione di interesse (ROI) ovvero l'area
        # in cui possono essere impartiti i comandi, all'interno del frame
        cv2.rectangle(frame, [0, 0, ROI_size[0], ROI_size[1]], (0, 255, 255), 4)
        ROI = frame[0:ROI_size[1], 0:ROI_size[0]]  # NB: la prima coordinata è y

        # Verifico che il video non sia stato messo in pausa per l'assenza dell'utente (volto/occhi non rilevati)
        if not pausedForPresence:
            # Limito la zona di input ad una ROI
            handDetector.findHands(ROI)
            lmList = handDetector.findPosition(ROI, draw=False, radius=8)

            if len(lmList) != 0 and not handDetector.discard:
                fingersOpened = [False, False, False, False,
                                 False]  # resetto l'array di booleani per il controllo delle dita

                """
                    Gesture per interrompere/riprendere la riproduzione con la mano
                """

                # Verifico per ogni dito della mano che sia aperto o chiuso
                for i in range(len(fingerIDs)):
                    if i == 0:
                        # Verifico che il pollice sia aperto o chiuso
                        if lmList[4][1] > lmList[3][1]:
                            fingersOpened[0] = True
                        else:
                            fingersOpened[0] = False
                    else:
                        fingersOpened[i] = lmList[fingerIDs[i]][2] < lmList[fingerIDs[i] - 2][2]

                count = Counter(fingersOpened)
                if count[True] == 5:
                    # Se la mano è aperta completamente la riproduzione riprende
                    player.play()
                    pausedForHands = False
                elif count[False] == 5:
                    # Se la mano è chiusa completamente la riproduzione si interrompe
                    player.pause()
                    pausedForHands = True
                elif fingersOpened[0] and fingersOpened[1] and count[True] == 2 and player.is_playing():
                    """
                        Gesture per il controllo del volume 
                    """
                    # Controlli su posizione reciproca tra pollice e indice
                    # Controllo che la y dell'indice sia maggiore della y del pollice
                    if lmList[8][2] <= lmList[4][2]:
                        # Calcolo la distanza tra pollice e indice
                        thumb_index_distance = handDetector.findDistance(4, 8, frame)

                        """
                            Utilizzo la distanza tra il polso e il metacarpo del mignolo
                            per normalizzare la distanza tra pollice indice
                            senza dover avere la distanza dalla camera
                        """

                        # Calcolo la distanza tra il polso e il metacarpo del mignolo
                        # (per normalizzare la distanza tra pollice e indice)

                        dist = handDetector.findDistance(0, 17, frame, False)
                        minDist = dist / 100 * 15  # distanza minima per avere volume zero
                        maxDist = dist / 100 * 150  # distanza minima per avere volume massimo

                        # Imposto il volume di riproduzione
                        volume = np.interp(thumb_index_distance, [minDist, maxDist], [0, 100])
                        player.set_volume(volume)

                        width = int(videocapture.cap.get(cv2.CAP_PROP_FRAME_WIDTH))  # float `width`

                        # Disegna a video, durante l'aggiornamento, una barra in base alla % di volume
                        cv2.rectangle(frame, (width - 50, 150), (width - 85, 400), (255, 0, 0), cv2.FILLED)
                        cv2.rectangle(frame, (width - 50, 150), (width - 85, 400 - int(volume / 100 * 250)),
                                      (255, 255, 255), cv2.FILLED)
                        cv2.putText(frame, f'{player.get_volume()}%', (width - 65, 450), cv2.FONT_HERSHEY_COMPLEX, 1,
                                    (255, 0, 0), 2)

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        if ax_img is None:
            ax_img = plt.imshow(frame)
            plt.axis("off")  # nasconde gli assi
            plt.title("Camera Capture")
            # mostra il plot
            plt.show()
        else:
            ax_img.set_data(frame)
            videocapture.update_figure()
            plt.pause(1 / 30)  # pausa: 30 frame al secondo


def face_eyes_detector(detector, elapsed_time, presence_timer):
    # Il video si mette in pausa se si esce dall'inquadratura della camera per un numero di secondi
    # oppure se si chiudono entrambi gli occhi

    # Ottengo il volto
    detector.detect_face()

    # Se ho un volto allora verifico se gli occhi sono aperti o chiusi
    if len(detector.faces) > 0:
        detector.detect_eyes()
        if len(detector.eyes) > 0:
            # ho rilevato che gli occhi sono aperti
            presence_timer = 0
        else:
            # ho rilevato che gli occhi sono chiusi
            presence_timer += elapsed_time
    else:
        presence_timer += elapsed_time
    return presence_timer


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit(0)
