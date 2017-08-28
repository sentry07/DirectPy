#!/usr/bin/env python
import requests

class DIRECTV:
    """DirectPy.py by Eric Walters (github.com/sentry07)

    Control a DirecTV receiver over the network using
    DirecTV's SHEF protocol. For more information on
    enabling the SHEF interface, please see this PDF:
    https://www.satinstalltraining.com/homeautomation/DTV-MD-0359-DIRECTV_SHEF_Command_Set-V1.3.C.pdf

    The clientAddr parameter of the class is used for
    Genie systems that have a server receiver and client
    receivers. To control a client receiver, you must
    know the MAC address and reference it without colons.
    EX: DIRECTV('192.168.1.10',clientAddr='000A959D6816')
    """    
    def __init__(self, ip, port=8080, clientAddr='0'):
        self.ip = ip
        self.port = port
        self.clientAddr = clientAddr
        self.standby = False
        self.channel = '0'
        self.valid_keys = ['power', 'poweron', 'poweroff', 'format', 'pause', 'rew', 'replay', 'stop',
                          'advance', 'ffwd', 'record', 'play', 'guide', 'active', 'list', 'exit',
                          'back', 'menu', 'info', 'up', 'down', 'left', 'right', 'select', 'red',
                          'green', 'yellow', 'blue', 'chanup', 'chandown', 'prev', '0', '1', '2',
                          '3', '4', '5', '6', '7', '8', '9', 'dash', 'enter']

        self.base_url = 'http://%s:%s' % (ip,port)

        self.get_standby()
        self.get_tuned()

    @staticmethod
    def _parse_channel(channel):
        """Return major and minor channel numbers for given channel"""
        try:
            major, minor = channel.split('-')
        except ValueError:
            major = channel
            minor = 65535

        return major,minor

    @staticmethod
    def _combine_channel(major,minor):
        """Return the combined channel number. If minor == 65535, there is no minor channel number."""
        if minor == 65535:
            return str(major)
        else:
            return '%d-%d' % (major,minor)

    def get_standby(self):
        """Return standby status of the receiver."""
        jResp = requests.get('%s/info/mode?clientAddr=%s' % (self.base_url,self.clientAddr)).json()
        if jResp['status']['code'] == 200: 
            self.standby = (jResp['mode'] == 1)
        
        return self.standby
        
    def get_channel(self, channel:"'###' or '###-#'"):
        """Return program information for a channel."""
        if not type(channel) is str:
            raise TypeError('Channel should be a string')
        major,minor = self._parse_channel(channel)
        jResp = requests.get('%s/tv/getProgInfo?major=%s&minor=%s&clientAddr=%s' % (self.base_url,major,minor,self.clientAddr)).json()

        return jResp

    def get_tuned(self):
        """Returns the channel and program information of the current channel."""
        jResp = requests.get('%s/tv/getTuned?clientAddr=%s' % (self.base_url,self.clientAddr)).json()
        self.channel = self._combine_channel(jResp['major'],jResp['minor'])
        
        return jResp

    def tune_channel(self, channel:"'###' or '###-#'"):
        """Change the channel on the receiver."""
        if not type(channel) is str:
            raise TypeError('Channel should be a string')
        major,minor = self._parse_channel(channel)

        jResp = requests.get('%s/tv/tune?major=%s&minor=%s&clientAddr=%s' % (self.base_url,major,minor,self.clientAddr)).json()
        if jResp['status']['code'] == 200:
            self.channel = channel

        return jResp

    def key_press(self, key:str):
        """Emulate pressing a key on the remote. See help() for supported keys.

        Supported keys: power, poweron, poweroff, format, 
        pause, rew, replay, stop, advance, ffwd, record, 
        play, guide, active, list, exit, back, menu, info, 
        up, down, left, right, select, red, green, yellow, 
        blue, chanup, chandown, prev, 0, 1, 2, 3, 4, 5, 
        6, 7, 8, 9, dash, enter
        """
        if not type(key) is str:
            raise TypeError('Key should be a string')
        if not key.lower() in self.valid_keys:
            raise ValueError('Invalid key: ' + key)
        
        jResp = requests.get('%s/remote/processKey?key=%s&hold=keyPress&clientAddr=%s' % (self.base_url,key,self.clientAddr)).json()

        return jResp

    def get_locations(self):
        """Returns the clientAddr for all devices."""
        
        jResp = requests.get('%s/info/getLocations' % (self.base_url)).json()
        
        return jResp
