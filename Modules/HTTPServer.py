import math
import time
from threading import Thread

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from Common.Logger import Logger
from Common.Store import Store


class HttpServer:
    def __init__(self, st: Store, lg: Logger):
        self.config = st.config
        self.st = st
        self.lg = lg

        self.api = FastAPI()
        origins = ["*"]
        self.api.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        self.server_loop = Thread(target=self.serve, daemon=True, args=())

    def start(self):
        self.server_loop.start()

    def serve(self):
        @self.api.post("/api/v1/post/cv_mode")
        async def set_manual_mode(data: Request):
            data = await data.json()
            if self.st.pull_data("cv_mode") != data["cv_mode"]:
                self.st.push_data("cv_alignment", 0)
                self.st.push_data("cv_task_complete", False)
            self.st.push_data("cv_mode", data['cv_mode'])
            return {
                "status": "OK",
                "cv_alignment": self.st.pull_data("cv_alignment"),
                "cv_task_complete": self.st.pull_data("cv_task_complete"),
            }

        self.lg.init("Инициализация завершена.")
        if int(self.st.config['general']['show_errors']) == 1:
            uvicorn.run(self.api, host="0.0.0.0", port=5052)
        else:
            uvicorn.run(self.api, host="0.0.0.0", port=5052, log_level="critical")
