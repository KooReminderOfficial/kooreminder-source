#!/usr/bin/env python3

from sys import stderr, exit

try:
    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk, GObject, GLib

except Exception:
    stderr.write('[-] Gtk is not installed!\n')
    exit(1)


class Alarm:
    def __init__(self, array):
        self.time = array[1]
        self.title = array[2]
        self.repeat = array[3]
        self.sound_file = array[4]

        self.btn_label = Gtk.Button.new_with_label('')
        label = self.btn_label.get_child()
        label.set_xalign(0.0)
        label.set_line_wrap(True)
        label.set_markup(self.__str__())
        self.btn_label.get_style_context().add_class('alarm')
    
    def get_button(self):
        return self.btn_label
    
    def get_data(self):
        return {
            'time': self.time,
            'title': self.title,
            'repeat': self.repeat,
            'sound_file': self.sound_file,
        }
    
    def __str__(self):
        return f'<big><big><b>{self.time[:5]}</b></big></big>\n<small><small>{self.title}, <i>{self.repeat}</i></small></small>'