import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, Pango, GObject
import cairo
import signal
import math

from SimpleLabel import SimpleLabel

PADDING         = 10
EDGE_X_OFFSET   = 10
EDGE_Y_OFFSET   = 50
ICON_SIZE       = Gtk.IconSize.LARGE_TOOLBAR
REFRESH_TIMEOUT = 1000
TITLE           = 'Services'
FONT_NAME = 'Liberation Mono'
FONT_SIZE = 14

FIXED_ROWS = 1

STATUS_LABELS = {
    'OK':    ('available',  'green'),
    'ERROR': ('unavailable', 'red')
}

class Monitor(Gtk.Window):
    def __init__(self, services):
        super(Monitor, self).__init__()
        self._services = services
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

        title_label = SimpleLabel(TITLE, 'white', 0.5)
        title_label.set_margin_bottom(15)
        grid.attach(title_label, 1, 0, 3, 1)

        for row, service in enumerate(self._services):
            row += FIXED_ROWS  # FIXME: hack
            name_label   = SimpleLabel(service.name, 'white', 0)
            status_label = SimpleLabel('...', 'white', 1)

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

        required_height = len(self._services) * (FONT_SIZE + PADDING)
        required_width  = (
            max(map(lambda x: len(x.name), self._services))
            + max(map(lambda x: len(x[0]), STATUS_LABELS.values()))
        ) * FONT_SIZE - 45 # FIXME: hack
        self.resize(required_width, required_height)

        # Position the window in the lower right corner of the screen
        self.set_gravity(Gdk.Gravity.SOUTH_EAST)
        self_width, self_height = self.get_size()
        root_win = Gdk.get_default_root_window()
        root_width, root_height = root_win.get_width(), root_win.get_height()
        self.move(root_width - self_width - EDGE_X_OFFSET,
                root_height - self_height - EDGE_Y_OFFSET)

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
            if service.status != 'REFRESH':
                spinner.stop()
                label = self._service_grid.get_child_at(2, row)
                label_desc = STATUS_LABELS[service.status]
                label.set_text(label_desc[0])
                label.set_text_color(label_desc[1])
            else:
                spinner.start()

        return True
