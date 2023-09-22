import configparser
import os
import time

from Common.Logger import Logger
from Common.Network import Network
from Common.Store import Store
from Modules.CVProvider import CVProvider
from Modules.HTTPServer import HttpServer

config = configparser.ConfigParser()
config.read(os.path.dirname(os.path.abspath(__file__)) + "/init.cfg")

LG = Logger(config)
ST = Store(config, LG)

HS = HttpServer(ST, LG).start()

CP = CVProvider(ST, LG).start()


NW = Network(config, ST, LG)
NW.wait_for_connection()

LG.init('Инициализация завершена.')

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt as e:
    print()
    LG.info('KeyboardInterrupt, остановлено пользователем.')
