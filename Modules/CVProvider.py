import time
from threading import Thread

from Common.Logger import Logger
from Common.Store import Store


class CVProvider:
    def __init__(self, st: Store, lg: Logger):
        self.st = st
        self.lg = lg

        self.runnable = Thread(target=self.run, args=(), daemon=True)

    def start(self):
        self.runnable.start()

    def run(self):
        while True:
            time.sleep(0.05)

            if self.st.pull_data("cv_mode") == "yellow_gate":
                #
                #
                # ТУТ КАКИЕ-ТО МАНИПУЛЯЦИИ
                #
                #

                # Тут отправка отклонения от центра кадра
                self.st.push_data("cv_alignment", 0)

                # Тут задаётся граничное условие для завершения
                if True:
                    self.st.push_data("cv_task_complete", True)

            elif self.st.pull_data("cv_mode") == "buoy_of_truth":
                #
                #
                # ТУТ КАКИЕ-ТО МАНИПУЛЯЦИИ
                #
                #

                # Тут отправка типа буйка: -1 синий 1 зелёный
                self.st.push_data("cv_alignment", 0)

                # Тут задаётся граничное условие для завершения
                if True:
                    self.st.push_data("cv_task_complete", True)

            if self.st.pull_data("cv_mode") == "green_buoy":
                #
                #
                # ТУТ КАКИЕ-ТО МАНИПУЛЯЦИИ
                #
                #

                # Тут отправка отклонения от центра кадра
                self.st.push_data("cv_alignment", 0)

                # Тут задаётся граничное условие для завершения
                if True:
                    self.st.push_data("cv_task_complete", True)

            if self.st.pull_data("cv_mode") == "blue_buoy":
                #
                #
                # ТУТ КАКИЕ-ТО МАНИПУЛЯЦИИ
                #
                #

                # Тут отправка отклонения от центра кадра
                self.st.push_data("cv_alignment", 0)

                # Тут задаётся граничное условие для завершения
                if True:
                    self.st.push_data("cv_task_complete", True)

            if self.st.pull_data("cv_mode") == "dock":
                #
                #
                # ТУТ КАКИЕ-ТО МАНИПУЛЯЦИИ
                #
                #

                # Тут отправка отклонения от центра кадра
                self.st.push_data("cv_alignment", 0)

                # Тут задаётся граничное условие для завершения
                if True:
                    self.st.push_data("cv_task_complete", True)


