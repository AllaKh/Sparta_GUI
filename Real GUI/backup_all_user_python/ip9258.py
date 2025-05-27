#
# IP Power 9258 networked power switch class
#
# This work is released under the Creative Commons Zero (CC0) license.
# See http://creativecommons.org/publicdomain/zero/1.0/

# Example use:
#
# import time
# from ip9258 import Ip9258
#
# ip9258 = Ip9258('192.168.1.10', 'admin', 'password')
#
# for i in range(4):
#     ip9258.on(i)
#     time.delay(1)
#
#     ip9258.off(i)
#     time.delay(1)

import urllib.request, urllib.error, urllib.parse

class Ip9258:
    def __init__(self, hostname, username, password):
        self._hostname = hostname

        # create a password manager
        password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
        password_mgr.add_password(None, 'http://' + hostname, username, password)
        handler = urllib.request.HTTPBasicAuthHandler(password_mgr)
        opener = urllib.request.build_opener(handler)
        # Now all calls to urllib2.urlopen use our opener.
        urllib.request.install_opener(opener)

    def on(self, port):
        old = self.get(port) 
        urllib.request.urlopen('http://' + self._hostname + '/set.cmd?cmd=setpower+p6' + str(port) + '=1')
        return old

    def off(self, port):
        old = self.get(port)
        urllib.request.urlopen('http://' + self._hostname + '/set.cmd?cmd=setpower+p6' + str(port) + '=0')
        return old

    def get(self, port):
        s = urllib.request.urlopen('http://' + self._hostname + '/set.cmd?cmd=getpower'  ).read()
        p = 'p6' + str(port)+'='
        return s.decode('ascii').split(p)[1][0]
    
    def set(self, port,value):
        old = self.get(port)
        urllib.request.urlopen('http://' + self._hostname + '/set.cmd?cmd=setpower+p6' + str(port) + '='+str(value))
        return old
