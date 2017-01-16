#!/usr/bin/python
# Copyright (C) 2017  Szymon Nieznański
# 
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from sys import argv, exit
import signal
import yaml

from Service import Service
from Monitor import Monitor

FIELDS_WITH_GLOBALS = [
    'refresh_interval',   'refresh_timeout', 'flapping_detection_interval',
    'notification_title', 'notification_text', 'notification_timeout',
    'label_ok', 'label_error'
]

def main():
    fh_services = open(argv[1])
    config = yaml.safe_load(fh_services)
    fh_services.close()

    service_objects = []
    for service in config['services']:
        for field in FIELDS_WITH_GLOBALS:
            if field not in service:
                service[field] = config[field]
        service_objects.append(Service(**service))

    if len(config['services']) == 0:
        print('No services found')
        exit()

    app = Monitor(service_objects, config)
    Gtk.main()

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()
