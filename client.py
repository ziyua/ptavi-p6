#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Programa cliente que abre un socket a un servidor
"""

import socket
import sys


class SIPclient():

    def __init__(self, Addr, User):
        """
        connect server SIP, socket UDP.
        """
        self.PROTOCOL = ['SIP/2.0', '100', 'Trying', 'SIP/2.0', '180', 'Ringing', 'SIP/2.0', '200', 'OK']
        self.User = User
        # Cliente UDP simple.
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # jose@12.34.56.78(ip):5060(port) -> Addr = (12.34.56.78, 5060)
        self.my_socket.connect(Addr)

    def sendSIP(self, Method):
        """
        Send package SIP: INVITE sip:pep8@127.0.0.1:5060 SIP/2.0
        """
        LINE = Method + ' sip:' + self.User + ' SIP/2.0\r\n'
        print "Enviando: " + LINE
        self.my_socket.send(LINE + '\r\n')

    def receiveSIP(self, bufferSiza=1024):
        """
        Receive package SIP: Trying, Ring, OK
        """
        try:
            data = self.my_socket.recv(bufferSiza)
        except socket.error:
            sys.exit('Error: No server listening at ' +
                     SERVER + ' port ' + str(PORT))

        # SIP/2.0 100/180/200 Trying/Ring/Ok
        data = data.strip()
        print 'Receive -- ', repr(data)
        Num = data.split()[-2]
        if data.split() == self.PROTOCOL and Num == "200":
            self.sendSIP('ACK')
        # else: No correcta msg que envia por servidor.

    def closeSIP(self):
        """
        close SIP connect.
        """
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
    mySIP = SIPclient((SERVER, PORT), User=sys.argv[2])

    # vamos a enviar (INVITE, jose@127.0.0.1:8000)
    mySIP.sendSIP(Method=sys.argv[1])
    mySIP.receiveSIP()

    # if RTP: print 'Starting receive RTP...'
    mySIP.closeSIP()
