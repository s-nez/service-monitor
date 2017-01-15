import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, Pango, GObject

class SimpleLabel(Gtk.Label):
    def __init__(self, text, color, align, font_description):
        super(SimpleLabel, self).__init__()
        self.set_text(text)
        self.set_xalign(align)
        self.modify_font(Pango.FontDescription(font_description))
        self.set_text_color(color)

    def set_text_color(self, color):
        self.modify_fg(Gtk.StateFlags.NORMAL, Gdk.color_parse(color))
