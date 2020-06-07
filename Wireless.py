#!/usr/bin/env python3

from PyAccessPoint import pyaccesspoint
import secrets
from string import ascii_letters, digits
import atexit


class Wireless:
    '''
    Wireless functionalities (HotSpot, wireless connection, etc.).
    Unfortunately this requires root privileges.
    '''
    def __init__(self):
        self.access_point = pyaccesspoint.AccessPoint(ssid='KooReminder', inet=None, wlan='wlan0', ip='10.0.0.1', netmask='255.0.0.0')
        self.password = None
        self.password_length = 12
        self.characters = [x for x in ascii_letters + digits]
        self.access_point.stop()
        atexit.register(self.toggle_access_point, False)
    
    def change_password(self):
        self.password = self.generate_password()
        self.access_point.password = self.password
    
    def get_password(self):
        return self.password
    
    def generate_password(self):
        output = ''
        for x in range(self.password_length):
            output += secrets.choice(self.characters)
        return output
    
    def toggle_access_point(self, run_hotspot=None):
        if run_hotspot == False:
            print('Autostop')
            self.access_point.stop()
            return
        elif run_hotspot == True:
            print('Autostart')
            self.access_point.start()
            return
        
        if self.access_point.is_running():
            print('Toggle -> stop')
            self.access_point.stop()
        else:
            print('Toggle -> start')
            self.access_point.start()
