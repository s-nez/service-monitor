from time import sleep
from random import randint
from threading import Thread
import socket

REFRESH_INTERVAL = 5

class Service(object):
    def __init__(self, name, address, port):
        self.name    = name
        self.address = address
        self.port    = port
        self._thread = Thread(target = self.refresh_status)
        self._thread.start()

    def refresh_status(self):
        while True:
            self.status = 'REFRESH'
            try:
                socket.create_connection((self.address, self.port))
            except socket.error as e:
                self.status = 'ERROR'
                print('got "%s" while trying %s:%d' % (e, self.address, self.port))

            if self.status == 'REFRESH':
                self.status = 'OK'

            sleep(REFRESH_INTERVAL)
