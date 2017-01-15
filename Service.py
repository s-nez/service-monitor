from time import sleep
from random import randint
from threading import Thread
import socket

class Service(object):
    def __init__(self, **kwargs):
        self.name             = kwargs['name']
        self.address          = kwargs['address']
        self.port             = kwargs['port']
        self.refresh_interval = kwargs['refresh_interval']
        self.refresh_timeout  = kwargs['refresh_timeout']

        self._status_timestamps = { 'ERROR': None, 'OK': None }
        self._thread = Thread(target = self.refresh_status)
        self._thread.start()

    def refresh_status(self):
        while True:
            self.status = 'REFRESH'
            try:
                socket.create_connection((self.address, self.port),
                                          self.refresh_timeout)
            except socket.error as e:
                self.status = 'ERROR'
                print('got "%s" while trying %s:%d' % (e, self.address, self.port))

            if self.status == 'REFRESH':
                self.status = 'OK'

            sleep(self.refresh_interval)
