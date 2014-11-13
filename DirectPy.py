import requests

class DIRECTV:
    """DirectPy.py by Eric Walters (github.com/sentry07)

    Control a DirecTV receiver over the network using
    DirecTV's SHEF protocol. For more information on
    enabling the SHEF interface, please see this PDF:
    https://www.satinstalltraining.com/homeautomation/DTV-MD-0359-DIRECTV_SHEF_Command_Set-V1.3.C.pdf
    """    
    def __init__(self, ip, port=8080):
        self.ip = ip
        self.port = port
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
            return major
        else:
            return '%s-%s' % (major,minor)

    def get_standby(self):
        """Return standby status of the receiver."""
        jResp = requests.get('%s/info/mode' % (self.base_url)).json()
        self.standby = (jResp['mode'] == 1)
        
        return self.standby
        
    def get_channel(self, channel):
        """Return program information for a channel. Specify a standard (249) or HD (249-1) channel."""
        major,minor = self._parse_channel(channel)
        jResp = requests.get('%s/tv/getProgInfo?major=%s&minor=%s' % (self.base_url,major,minor)).json()

        return jResp

    def get_tuned(self):
        """Returns the channel and program information of the current channel."""
        jResp = requests.get('%s/tv/getTuned' % (self.base_url)).json()
        self.channel = self._combine_channel(jResp['major'],jResp['minor'])
        
        return jResp

    def tune_channel(self, channel):
        """Change the channel on the receiver. Specify a standard (249) or HD (249-1) channel."""
        major,minor = self._parse_channel(channel)

        jResp = requests.get('%s/tv/tune?major=%s&minor=%s' % (self.base_url,major,minor)).json()
        if jResp['status']['code'] == 200:
            self.channel = channel

        return jResp

    def key_press(self, key):
        """Emulate pressing a key on the remote.

        Supported keys: power, poweron, poweroff, format, 
        pause, rew, replay, stop, advance, ffwd, record, 
        play, guide, active, list, exit, back, menu, info, 
        up, down, left, right, select, red, green, yellow, 
        blue, chanup, chandown, prev, 0, 1, 2, 3, 4, 5, 
        6, 7, 8, 9, dash, enter
        """
        if not key.lower() in self.valid_keys:
            raise ValueError('Invalid key: ' + key)
        
        jResp = requests.get('%s/remote/processKey?key=%s&hold=keyPress' % (self.base_url,key)).json()

        return jResp
