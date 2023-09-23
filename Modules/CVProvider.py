import time
from threading import Thread

import cv2
import numpy
import numpy as np
import rtsp

from Common.Logger import Logger
from Common.Store import Store
from Modules.buoy_detection import find_gates, find_buoy, find_dock


class CVProvider:
    def __init__(self, st: Store, lg: Logger):
        self.st = st
        self.lg = lg

        self.runnable = Thread(target=self.run, args=(), daemon=True)

        self.rtsp_address = "rtsp://localhost:8554/asd"

    def start(self):
        self.runnable.start()

    def run(self):
        with rtsp.Client(rtsp_server_uri=self.rtsp_address) as client:
            time.sleep(2)
            _image = numpy.array(client.read())
            # _image = _image[:, :, ::-1].copy()
            not_found_counter = 0
            while True:
                cv2.waitKey(10)

                if self.st.pull_data("cv_mode") == "yellow_gate":

                    cords = find_gates(_image, np.array([5, 141, 101]), np.array([33, 215, 149]), "Gate", 4)

                    # Тут отправка отклонения от центра кадра
                    if cords is not None:
                        self.st.push_data("cv_alignment", int(cords[0]-int(_image.shape[1]/2)))

                    # Тут задаётся граничное условие для завершения
                    if cords is None:
                        not_found_counter += 1
                    else:
                        not_found_counter = 0
                    if not_found_counter == 20:
                        self.st.push_data("cv_task_complete", True)
                        not_found_counter = 0

                elif self.st.pull_data("cv_mode") == "buoy_of_truth":

                    # Тут отправка типа буйка: -1 синий 1 зелёный
                    self.st.push_data("cv_alignment", 1)

                    # Тут задаётся граничное условие для завершения
                    if True:
                        self.st.push_data("cv_task_complete", True)

                elif self.st.pull_data("cv_mode") == "green_buoy":
                    lower = np.array([5, 141, 101])
                    higher = np.array([33, 215, 149])
                    cords = find_buoy(_image, lower, higher, "Warning", 4, 1)

                    # Тут отправка отклонения от центра кадра
                    self.st.push_data("cv_alignment", int(cords[0]-int(_image.shape[1]/2)))

                elif self.st.pull_data("cv_mode") == "blue_buoy":
                    lower = np.array([5, 141, 101])
                    higher = np.array([33, 215, 149])
                    cords = find_buoy(_image, lower, higher, "Warning", 4, 1)

                    # Тут отправка отклонения от центра кадра
                    self.st.push_data("cv_alignment", int(cords[0]-int(_image.shape[1]/2)))

                elif self.st.pull_data("cv_mode") == "dock":
                    lower = np.array([5, 141, 101])
                    higher = np.array([33, 215, 149])
                    cords = find_dock(_image, lower, higher, "Warning", 4)

                    # Тут отправка отклонения от центра кадра
                    self.st.push_data("cv_alignment", int(cords[0]-int(_image.shape[1]/2)))

                    # Тут задаётся граничное условие для завершения
                    if False:
                        self.st.push_data("cv_task_complete", True)

                else:
                    pass

                _image = numpy.array(client.read(raw=True))
                # _image = _image[:, :, ::-1].copy()


