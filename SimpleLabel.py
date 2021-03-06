# Copyright (C) 2017  Szymon Nieznański (s.nez@member.fsf.org)
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
