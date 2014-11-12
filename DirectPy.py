#####################################################
# DirectPy.py by Eric Walters (github.com/sentry07) #
# ------------------------------------------------- #
# Control a DirecTV receiver over the network using #
# DirecTV's SHEF protocol. For more information on  #
# the SHEF protocol, please search Google for       #
# DirecTV SHEF 1.3                                  #
#####################################################

import urllib.request
import json

class directv:
    def __init__(self,ip,port = 8080):
        self.ip = ip
        self.port = port
        self.standby = False
        self.channel = '0'
        
        self.get_status()
        self.get_tuned()

    ## Get status of the receiver. This only tells us if the receiver is in standby or not.
    def get_status(self):
        w = urllib.request.urlopen('http://%s:%d/info/mode' % (self.ip,self.port))
        jResp = json.loads(w.read().decode('UTF-8'))
        self.standby = (jResp['mode'] == 1)
        
    ## Return information for a channel. You can specify a standard (249) or HD (249-1) channel.
    def get_channel(self,channel):
        _channel = channel.split('-')
        major = _channel[0]
        if len(_channel) == 2:
            minor = _channel[1]
        else:
            minor = 65535

        w = urllib.request.urlopen('http://%s:%d/tv/getProgInfo?major=%s&minor=%s' % (self.ip,self.port,major,minor))
        jResp = json.loads(w.read().decode('UTF-8'))

        return jResp

    ## This gets the channel and program information of the current channel.
    def get_tuned(self):
        w = urllib.request.urlopen('http://%s:%d/tv/getTuned' % (self.ip,self.port))
        jResp = json.loads(w.read().decode('UTF-8'))

        if jResp['minor'] == 65535:
            self.channel = jResp['major']
        else:
            self.channel = '%s-%s' % (jResp['major'],jResp['minor'])
        
        return jResp

    ## This changes the channel on the receiver. You can specify a standard (249) or HD (249-1) channel.
    def tune_channel(self,channel):
        _channel = channel.split('-')
        major = _channel[0]
        if len(_channel) == 2:
            minor = _channel[1]
        else:
            minor = 65535

        w = urllib.request.urlopen('http://%s:%d/tv/tune?major=%s&minor=%s' % (self.ip,self.port,major,minor))
        jResp = json.loads(w.read().decode('UTF-8'))
        if jResp['status']['msg'] == 'OK.':
            self.channel = channel

        return jResp


    ## This emulates pressing a key on the remote.
    ## Supported keys: power, poweron, poweroff, format, 
    ## pause, rew, replay, stop, advance, ffwd, record, 
    ## play, guide, active, list, exit, back, menu, info, 
    ## up, down, left, right, select, red, green, yellow, 
    ## blue, chanup, chandown, prev, 0, 1, 2, 3, 4, 5, 
    ## 6, 7, 8, 9, dash, enter 
    def key_press(self,key):
        w = urllib.request.urlopen('http://%s:%d/remote/processKey?key=%s&hold=keyPress' % (self.ip,self.port,key))
        jResp = json.loads(w.read().decode('UTF-8'))

        return jResp
