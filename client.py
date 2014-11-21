#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Programa cliente que abre un socket a un servidor
"""

import socket
import sys
import re


class SIPclient():

    def __init__(self, Addr, User):
        self.PROTOCOL = r'^SIP/2.0\s\d{3}\s\w+'
        self.User = User
        # Cliente UDP simple.
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Bind Address: jose@12.34.56.78(ip):5060(port) -> Addr = (12.34.56.78, 5060)
        self.my_socket.connect(Addr)

    def sendSIP(self, Method):
        LINE = Method + ' sip:' + self.User + ' SIP/2.0\r\n'
        print "Enviando: " + LINE
        self.my_socket.send(LINE + '\r\n')

    def receiveRTP(self, portRTP):
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.my_socket.bind(('', portRTP))

        while 1:
            data = self.my_socket.recv(1024)
            print data

    recvRTP = False

    def receiveSIP(self, bufferSiza=1024):
        try:
            data, addrs = self.my_socket.recvfrom(bufferSiza)
        except socket.error:
            sys.exit('Error: No server listening at ' + SERVER + ' port ' + str(PORT))

        # SIP/2.0 100/180/200 Trying/Ring/Ok
        data = data.strip()
        print 'Receive -- ', repr(data), len(data), addrs
        mat = re.match(self.PROTOCOL, data)
        if mat is not None:
            Num = data.split()[1]
            if Num == "200":
                self.sendSIP('ACK')
                if self.recvRTP:
                    portRTP = int(data.split()[4])
                    self.receiveRTP(portRTP)
                    self.recvRTP = False
            elif Num == "100":  # SIP/2.0 Trying 100
                self.recvRTP = True
                self.receiveSIP()
            else:
                self.receiveSIP()
        else:
            print 'Not aquì RTP, if echo ERROR', repr(data)
        # else: No correcta msg que envia por servidor.

    def closeSIP(self):
        print "Terminando socket..."
        self.my_socket.close()
        print "Fin."

if __name__ == '__main__':
     # Usege:
    Usage = "Usage: python client.py method receiver@IP:SIPport"
    if len(sys.argv) != 3:
        sys.exit(Usage)

    try:
        SERVER, PORT = sys.argv[2].split('@')[1].split(':')
        PORT = int(PORT)
    except:
        sys.exit(Usage)

    # Init SIPclient
    mySIP = SIPclient((SERVER, PORT), sys.argv[2])

    # vamos a enviar (INVITE, jose@127.0.0.1:8000)
    mySIP.sendSIP(sys.argv[1])

    mySIP.receiveSIP()
    mySIP.closeSIP()
