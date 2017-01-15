import gi
gi.require_version('Notify', '0.7')
from gi.repository import Notify
from time import sleep, time
from random import randint
from threading import Thread
import socket

class Service(object):
    def __init__(self, **kwargs):
        Notify.init('Service Monitor')
        self.name             = kwargs['name']
        self.address          = kwargs['address']
        self.port             = kwargs['port']
        self.refresh_interval = kwargs['refresh_interval']
        self.refresh_timeout  = kwargs['refresh_timeout']
        self._notification_title = kwargs['notification_title']
        self._notification_text  = kwargs['notification_text']
        self._flap_int = kwargs['flapping_protection_interval']
        self._labels = {
            'OK':    kwargs['label_ok'],
            'ERROR': kwargs['label_error']
        }

        self.status = None
        self._status_timestamps = { 'OK': 0, 'ERROR': 0 }
        self._thread = Thread(target = self.refresh_status)
        self._thread.start()

    def refresh_status(self):
        while True:
            initial_status = self.status
            self.status = 'REFRESH'

            try:
                socket.create_connection((self.address, self.port),
                                          self.refresh_timeout)
            except socket.error as e:
                self.status = 'ERROR'
                print('got "%s" while trying %s:%d' % (e, self.address, self.port))

            if self.status == 'REFRESH':
                self.status = 'OK'

            if initial_status is not None and \
                self.status != initial_status and self._anti_flap_timeout():
                popup = Notify.Notification.new(
                    self._notification_title % (self.name),
                    self._notification_text  % (self._labels[self.status]),
                    'dialog-info' if self.status == 'OK' else 'dialog-error'
                )
                popup.show()

            sleep(self.refresh_interval)

    def _anti_flap_timeout(self):
        status_time = self._status_timestamps[self.status]
        return  status_time + self._flap_int < time()
