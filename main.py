#!/usr/bin/env python3

from sys import argv, exit, stderr
from os import remove, listdir
from os.path import realpath, dirname, isfile
from datetime import datetime
from time import sleep
import sqlite3



import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject, GLib



try:
    import vlc
    from Alarm import Alarm
    from Wireless import Wireless
    
except Exception as e:
    stderr.write('[-] Missing important file!\nBacktrace: {}\n'.format(e))
    exit(2)



class KooReminder:
    def __init__(self):
        self.project_path = dirname(realpath(__file__)) + '/'
        self.alarms = []
        self.alarm_playing = False
        self.player = None
        self.connection = sqlite3.connect(self.project_path + 'Files/Database.db')
        self.cursor = self.connection.cursor()
        self.wireless_functionalities = Wireless()
    
    def load_plugins(self):
        import Plugins

    def setup_ui(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file(self.project_path + 'Files/interface.glade')
        self.builder.connect_signals({
            'goto_screen': lambda x: self.goto_screen(x),
            'align_widget': lambda x: self.align_widget(x),
            'toggle_hotspot': lambda *x: self.toggle_hotspot(),
            'updated_sync_time': lambda *x: self.toggle_device_sync(),
        })

        self.window = self.builder.get_object('window')
        self.window.show_all()

        self.lbl_date = self.builder.get_object('lbl_date')
        self.lbl_time = self.builder.get_object('lbl_time')
        self.lbl_alarmTitle = self.builder.get_object('lbl_alarmTitle')
        self.switch_sync_time = self.builder.get_object('switch_sync_time')
        self.switch_hotspot_mode = self.builder.get_object('switch_hotspot_mode')
        self.entry_hotspot_password = self.builder.get_object('entry_hotspot_password')
        self.lbl_alarmTitle.set_line_wrap(True)

        self.cursor.execute('SELECT VALUE FROM INTEGRATION_SETTINGS WHERE SETTING_ID = "SYNC_TIME";')
        foo = self.cursor.fetchall()[0][0]

        self.switch_sync_time.set_state(foo)
        self.window.connect('destroy', Gtk.main_quit)
    
    def update_label_datetime(self, _):
        weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Sathurday', 'Sunday']
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        now = datetime.now()

        text_date = f'{weekdays[now.weekday()]}, {now.day} {months[now.month - 1]} {now.year}'
        text_time = f'{now.hour:02}:{now.minute:02}:{now.second:02}'

        self.lbl_date.set_text(text_date)
        self.lbl_time.set_text(text_time)

        return True

    def check_updated_alarms(self, _):
        if isfile(self.project_path + 'Files/.__update__'):
            remove(self.project_path + 'Files/.__update__')
            for x in self.alarms:
                x.get_button().destroy()
                del x
            self.alarms = []
            self.load_alarms()
        return True
    
    def load_alarms(self):
        foo = self.cursor.execute('SELECT * FROM INTEGRATION_ALARM;')
        self.alarms = [Alarm(x) for x in foo]
        alarms_stack = self.builder.get_object('alarmsStack')
        for x in self.alarms:
            alarms_stack.pack_start(x.get_button(), False, False, False)
            x.get_button().show()

    def align_widget(self, widget):
        pass

    def toggle_hotspot(self):
        value = not self.switch_hotspot_mode.get_state()
        self.cursor.execute(f'UPDATE INTEGRATION_SETTINGS SET VALUE = {value} WHERE SETTING_ID = "HOTSPOT_MODE";')
        if value:
            self.wireless_functionalities.change_password()
            self.entry_hotspot_password.set_text(self.wireless_functionalities.get_password())
            self.wireless_functionalities.access_point.start()

        else:
            self.entry_hotspot_password.set_text('')
            self.wireless_functionalities.access_point.stop()
        
        print(f'Hotspot running? {self.wireless_functionalities.access_point.is_running()}')

        self.connection.commit()

    def toggle_device_sync(self):
        value = not self.switch_sync_time.get_state()
        self.cursor.execute(f'UPDATE INTEGRATION_SETTINGS SET VALUE = {value} WHERE SETTING_ID = "SYNC_TIME";')
        self.connection.commit()

    def goto_screen(self, screen_ptr):
        notebook = Gtk.Widget.get_ancestor(screen_ptr, Gtk.Notebook)
        child = screen_ptr

        while notebook != None and notebook.__class__.__name__ != 'Window':
            if notebook.__class__.__name__ == 'Notebook':
                page = notebook.page_num(child)
                notebook.set_current_page(page)
                child = notebook
                notebook = notebook.get_parent()
            else:
                notebook = notebook.get_parent()
        
        if self.alarm_playing:
            self.kill_alarm()
    
    def check_alarms(self):
        current_time = datetime.now()

        if current_time.second != 0: return True
        
        for alarm in self.alarms:
            alarm_data = alarm.get_data()
            print(f'checking alarm: {alarm_data}')
            if alarm_data['repeat'][current_time.weekday()] != '_':
                alarm_time = alarm_data['time'].split(':')
                alarm_hour, alarm_minute = int(alarm_time[0]), int(alarm_time[1])
                if alarm_hour == current_time.hour and alarm_minute == current_time.minute:
                    self.play_alarm(alarm)
                    sleep(0.4)
            
        return True

    def play_alarm(self, alarm):
        prefix = self.project_path + 'Files/Sounds/'
        alarm_data = alarm.get_data()
        alarm_sound_path = prefix + alarm_data['sound_file']
        self.lbl_alarmTitle.set_text(alarm_data['title'])

        self.goto_screen(self.lbl_alarmTitle)

        if isfile(alarm_sound_path):
            self.player = vlc.MediaPlayer(alarm_sound_path)

        else:
            self.player = vlc.MediaPlayer(self.project_path + 'Files/Sounds/default')
        
        self.player.play()
        self.alarm_playing = True


    def kill_alarm(self):
        self.player.stop()
        self.alarm_playing = False
        
    def launch_threads(self):
        GLib.timeout_add(300, self.update_label_datetime, self)
        GLib.timeout_add(300, self.check_updated_alarms, self)
        GLib.timeout_add(600, self.check_alarms)
        Gtk.main()



if __name__ == '__main__':
    process = KooReminder()
    process.setup_ui()
    process.load_alarms()
    process.load_plugins()
    process.update_label_datetime(None)
    process.launch_threads()
