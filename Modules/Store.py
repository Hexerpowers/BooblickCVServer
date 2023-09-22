from Common.Logger import Logger


class Store:
    def __init__(self, config, lg: Logger):
        self.config = config
        self.lg = lg

        self.data = {
            "cv_alignment": 0,
            "task_cv_complete": False,
            "cv_mode": "yellow_gate"
        }

    def clean_runtime(self):
        self.data['initial_heading'] = self.data['heading']
        self.data['position_estimate'] = {"x": 0, "y": 0}

    def pull_data(self, name):
        if name in self.data:
            return self.data[name]
        else:
            self.data[name] = 0
            self.lg.warn('Значение с именем "' + str(name) + '" не обнаружено')
            return self.data[name]

    def push_data(self, name, value):
        self.data[name] = value
        return True
