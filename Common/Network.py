import time

from netifaces import interfaces, ifaddresses, AF_INET


class Network:
    def __init__(self, config, st, lg):
        self.config = config
        self.st = st
        self.lg = lg

    def wait_for_connection(self):
        subnets = str(self.config['network']['working_subnets']). \
            replace(' ', '').replace('[', '').replace(']', '').split(',')
        local_addresses = []
        for subnet in subnets:
            self.lg.init("Ожидание подключения с подсетью " + subnet + "...")
        net_available = False
        while not net_available:
            for ifaceName in interfaces():
                addresses = [i['addr'] for i in ifaddresses(ifaceName).setdefault(AF_INET, [{'addr': 'No IP addr'}])]
                for addr in addresses:
                    for subnet in subnets:
                        if subnet in addr:
                            local_addresses.append(addr)
            if len(local_addresses) > 0:
                net_available = True
                for addr in local_addresses:
                    self.lg.init("Сетевое подключение [" + str(addr) + "] обнаружено.")
            time.sleep(1)
