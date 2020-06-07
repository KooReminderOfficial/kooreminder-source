#!/usr/bin/env python3

try:
    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk, Gdk

except Exception:
    stderr.write('[-] Gtk is not installed!\n')
    exit(1)


if __name__ != '__main__':
    print(f'Running ThemeManager')
    themer = Gtk.CssProvider()
    themer.load_from_path('Files/Themes/current_theme')
    Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), themer, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)