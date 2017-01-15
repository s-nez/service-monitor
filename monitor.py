#!/usr/bin/python
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from sys import argv
import signal
import yaml

from Service import Service
from Monitor import Monitor

def main():
    fh_services = open(argv[1])
    services    = yaml.safe_load(fh_services)
    fh_services.close()

    service_objects = map(
            lambda x: Service(x['name'], x['address'], x['port']),
            services)
    app = Monitor(list(service_objects))
    Gtk.main()

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()
