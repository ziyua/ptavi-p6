#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Programa cliente que abre un socket a un servidor
"""

import time
import SocketServer
import socket
import sys
import re


class RTPhandle(SocketServer.DatagramRequestHandler):

    # Add Buffer

    def handle(self):
        while 1:
            data = self.rfile.read()
            # Add data a Buffer, and play audio
            print 'play data audio:', repr(data)
            if not data:
                break
    # Aqui send '', pues tiene [Malformed packet] de 42 byte.
    # solo tiene header 42byte


class SIPclient():

    def __init__(self, Addr, User):
        self.PROTOCOL = r'^SIP/2.0\s\d{3}\s\w+'
        self.User = User
        self.recvRTP = False
        self.Method = ''
        # Cliente UDP simple.
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # jose@12.34.56.78(ip):5060(port) -> Addr = (12.34.56.78, 5060)
        self.my_socket.connect(Addr)

    def sendSIP(self, Method):
        self.Method = Method
        LINE = Method + ' sip:' + self.User + ' SIP/2.0\r\n'
        print "Enviando: " + LINE
        self.my_socket.send(LINE + '\r\n')

    def receiveSIP(self, bufferSiza=1024):
        try:
            data = self.my_socket.recv(bufferSiza)
        except socket.error:
            sys.exit('Error: No server listening at ' +
                     SERVER + ' port ' + str(PORT))

        # SIP/2.0 100/180/200 Trying/Ring/Ok
        data = data.strip()
        print 'Receive -- ', repr(data)
        mat = re.match(self.PROTOCOL, data)
        if mat is not None:
            Num = data.split()[1]
            if Num == "200":
                if self.Method != 'BYE':
                    self.sendSIP('ACK')
            elif Num == "100":  # SIP/2.0 Trying 100
                self.recvRTP = True
                self.receiveSIP()
            else:
                self.receiveSIP()
        else:
            print 'Not aquì RTP, if echo ERROR', repr(data)
        # else: No correcta msg que envia por servidor.

    def endRecvSIP(self):
        sRTP = self.recvRTP
        self.recvRTP = False
        return sRTP

    def closeSIP(self):
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
    if mySIP.endRecvSIP():
        print 'Starting RTP...'
        RTPserv = SocketServer.UDPServer(("", 23032), RTPhandle)
        # exprid time 5.0 seg
        # if 5 seg not receive RTP data(no hay audio), break
        RTPserv.timeout = 5.0
        while 1:
            before = time.time()
            RTPserv.handle_request()
            after = time.time()
            if after - before > RTPserv.timeout:
                break
    # solo need close socket SIP, RTP ya termino.
    mySIP.closeSIP()
