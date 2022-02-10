import cv2
import matplotlib.pyplot as plt


class VideoCapture:
    def __init__(self):
        # init the camera
        self.frame_equalized = None
        self.frame = None
        self.cap = cv2.VideoCapture(0)
        # create a figure to be updated
        self.fig = plt.figure()
        self.fig.canvas.mpl_connect("close_event", lambda event: self.handle_close(event))

    def grab_frame(self):
        """
        Method to grab a frame from the camera
        :param cap: the VideoCapture object
        :return: the captured image
        """
        ret, self.frame = self.cap.read()
        return self.frame

    def equalize_frame(self):
        """
        Method to equalize the grabbed frame from the camera
        :return:
        """
        if self.frame is None:
            self.grab_frame()
        gray_frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        self.frame_equalized = clahe.apply(gray_frame)
        # frame_equalized = cv2.equalizeHist(gray_frame)  # equalization
        return self.frame_equalized

    def handle_close(self, event):
        """
        Handle the close event of the Matplotlib window by closing the camera capture
        :param event: the close event
        """
        self.cap.release()

    def is_opened(self):
        """
        :return: true if the capture is still opened
        """
        return self.cap.isOpened()

    def update_figure(self):
        """
        Updates the figure associated to the shown plot
        """
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
