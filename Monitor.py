import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, Pango, GObject
import cairo
import signal
import math

from SimpleLabel import SimpleLabel

DEFAULT_SETTINGS = {
    'window_gravity': 'bottom_right',
    'edge_x_offset': 10,
    'edge_y_offset': 50,

    'font_name': 'Liberation Mono',
    'font_size': 14,

    'title':       'Services',
    'label_ok':    'available',
    'label_error': 'unavailable',
    'color_ok':    'green',
    'color_error': 'red'
}

WINDOW_GRAVITIES = {
    'top_left':     Gdk.Gravity.NORTH_WEST,
    'top_right':    Gdk.Gravity.NORTH_EAST,
    'bottom_right': Gdk.Gravity.SOUTH_EAST,
    'bottom_left':  Gdk.Gravity.SOUTH_WEST
}

PADDING         = 10
ICON_SIZE       = Gtk.IconSize.LARGE_TOOLBAR
REFRESH_TIMEOUT = 1000
FIXED_ROWS = 1  # FIXME: hack

class Monitor(Gtk.Window):
    def __init__(self, services, settings):
        super(Monitor, self).__init__()
        self._services = services

        self._settings = settings
        for setting, value in DEFAULT_SETTINGS.items():
            if setting not in self._settings:
                self._settings[setting] = value
        self._settings['window_gravity'] = \
            WINDOW_GRAVITIES[self._settings['window_gravity']]
        self._font_description = self._settings['font_name'] \
            + ' ' + str(self._settings['font_size'])

        print('Got settings:', str(self._settings))

        self.setup()
        self.init_ui()
        GObject.timeout_add(REFRESH_TIMEOUT, self.update_status_indicators)

    def setup(self):
        self.set_app_paintable(True)
        self.set_keep_below(True)
        self.set_type_hint(Gdk.WindowTypeHint.DOCK)

        screen = self.get_screen()
        visual = screen.get_rgba_visual()
        if visual != None and screen.is_composited():
            self.set_visual(visual)


    def init_ui(self):
        self.connect('draw', self.on_draw)

        grid = Gtk.Grid()
        grid.set_column_spacing(5)
        grid.set_border_width(5)

        font = self._font_description

        title_label = SimpleLabel(self._settings['title'], 'white', 0.5, font)
        title_label.set_margin_bottom(15)
        grid.attach(title_label, 1, 0, 3, 1)

        no_status_placeholder = (' ' * (self._max_len_status_label()-3)) + '...'
        for row, service in enumerate(self._services):
            row += FIXED_ROWS  # FIXME: hack
            name_label   = SimpleLabel(service.name, 'white', 0, font)
            status_label = SimpleLabel(no_status_placeholder, 'white', 1, font)

            spinner = Gtk.Spinner()
            spinner.start()

            grid.attach(spinner, 0, row, 1, 1)
            grid.attach(name_label, 1, row, 1, 1)
            grid.attach(status_label, 2, row, 1, 1)

        self._service_grid = grid
        self.update_status_indicators()

        frame = Gtk.Frame()
        frame.add(grid)
        self.add(frame)

        font_size = self._settings['font_size']
        required_height = len(self._services) * (font_size + PADDING)
        required_width  = max(
            [self._max_len_service_name(), self._max_len_status_label()]
            ) * font_size;
        self.resize(required_width, required_height)

        self.set_gravity(self._settings['window_gravity'])
        self_width, self_height = self.get_size()
        root_win = Gdk.get_default_root_window()
        root_width, root_height = root_win.get_width(), root_win.get_height()
        x_offset, y_offset = \
            self._settings['edge_x_offset'], self._settings['edge_y_offset']
        self.move(root_width - self_width - x_offset - 110,
                root_height - self_height - y_offset)

        self.connect('delete-event', Gtk.main_quit)
        self.show_all()


    def on_draw(self, wid, cr):
        cr.set_operator(cairo.OPERATOR_OUT) # don't draw over existing objects
        cr.set_source_rgba(0.0, 0.0, 0.0, 0.9)
        cr.paint()
        cr.set_operator(cairo.OPERATOR_OVER)

    def update_status_indicators(self):
        for row, service in enumerate(self._services):
            row += FIXED_ROWS  # FIXME: hack
            spinner = self._service_grid.get_child_at(0, row)
            if service.status == 'OK':
                spinner.stop()
                label = self._service_grid.get_child_at(2, row)
                label.set_text(self._settings['label_ok'])
                label.set_text_color(self._settings['color_ok'])
            elif service.status == 'ERROR':
                spinner.stop()
                label = self._service_grid.get_child_at(2, row)
                label.set_text(self._settings['label_error'])
                label.set_text_color(self._settings['color_error'])
            else:
                spinner.start()

        return True

    def _max_len_service_name(self):
        return max(map(lambda x: len(x.name), self._services))

    def _max_len_status_label(self):
        return max(map(lambda x: len(x),
            [ self._settings['label_ok'], self._settings['label_error'] ]))

