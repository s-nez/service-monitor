import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, Pango, GObject
import cairo
import signal

FONT_NAME       = 'Liberation Mono'
FONT_SIZE       = 14
PADDING         = 5
EDGE_X_OFFSET   = 10
EDGE_Y_OFFSET   = 50
ICON_SIZE       = Gtk.IconSize.LARGE_TOOLBAR
REFRESH_TIMEOUT = 1000

ICON_NAMES = {
    'OK':      'network-transmit-receive',
    'ERROR':   'network-error',
    'REFRESH': 'network-receive'
}

class Monitor(Gtk.Window):
    def __init__(self, services):
        super(Monitor, self).__init__()
        self._services = services
        self.setup()
        self.init_ui()
        GObject.timeout_add(REFRESH_TIMEOUT, self.update_status_icons)

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
        for row, service in enumerate(self._services):
            label = Gtk.Label()
            label.set_text(service.name)
            label.set_xalign(0)  # left-align the text
            font_description = FONT_NAME + ' ' + str(FONT_SIZE)
            label.modify_font(Pango.FontDescription(font_description))
            label.modify_fg(Gtk.StateFlags.NORMAL, Gdk.color_parse('white'))
            grid.attach(label, 1, row, 1, 1)
            grid.attach(Gtk.Image(), 2, row, 1, 1)

        self._service_grid = grid
        self.update_status_icons()
        self.add(grid)

        required_height = len(self._services) * (FONT_SIZE + PADDING)
        required_width  = max(map(lambda x: len(x.name), self._services)) \
                            * (FONT_SIZE + PADDING)
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
        cr.set_operator(cairo.OPERATOR_CLEAR)
        cr.paint()
        cr.set_operator(cairo.OPERATOR_OVER)

    def update_status_icons(self):
        for row, service in enumerate(self._services):
            name = ICON_NAMES[service.status]
            icon = self._service_grid.get_child_at(2, row)
            icon.set_from_icon_name(name, ICON_SIZE)
        return True
