#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import SocketServer
import sys
import os
import re


class EchoHandler(SocketServer.DatagramRequestHandler):
    """
    Echo server class
    """
    ALLOW = 'INVITE|ACK|BYE|CANCEL|OPTIONS|REGISTER'
    PROTOCOL = r'(' + ALLOW + ')\ssip:\w+@(\w+|\d+(\.\d+){3}):\d+\sSIP/2.0'
    PORT_RTP = 23032

    def send_single(self, text):
        """
        Enviar información de inmediato.
        """
        self.socket.sendto(text, self.client_address)

    def handle(self):
        """
        Receive package and procesar
        """
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read().strip()
            # Recive INVITE|ACK|BYE sip:receptor@IP:port SIP/2.0
            m = re.match(self.PROTOCOL, line)
            if not m is None:
                if line.split()[0] == 'INVITE':
                    # 100 Trying
                    self.send_single('SIP/2.0 100 Trying\r\n\r\n')
                    # 180 Ring
                    self.send_single('SIP/2.0 180 Ringing\r\n\r\n')
                    # 200 OK
                    self.wfile.write('SIP/2.0 200 OK\r\n\r\n')
                elif line.split()[0] == 'ACK':
                    # send RTP
                    ip = self.client_address[0]
                    # mp3 to rtp
                    aEjecutar = './mp32rtp -i ' + ip + ' -p ' \
                                + '23032 < ' + sys.argv[3]
                    print "Vamos a ejecutar $ ", aEjecutar
                    # File Permissions
                    os.system('chmod +x mp32rtp')
                    os.system(aEjecutar)
                    # Error!! serv va a send '' a client. [Malformed package]
                elif line.split()[0] == 'BYE':
                    # Solo Send 200 OK
                    self.wfile.write('SIP/2.0 200 OK\r\n\r\n')
                else:
                    # YES -> INVITE|ACK|BYE   NOT -> CANCEL|OPTIONS|REGISTER
                    self.wfile.write('SIP/2.0 405 Method Not Allowed\r\n\r\n')
            elif line:
                # bad msg:
                self.wfile.write('SIP/2.0 400 Bad Request\r\n\r\n')
            else:
                break


if __name__ == "__main__":
    if len(sys.argv) != 4 or not os.path.exists(sys.argv[3]):
        # IP server para eth0 eth1 lo, diff Interfaces.
        sys.exit('Usage: python server.py IP port audio_file')
    else:
        # Creamos servidor de eco y escuchamos
        serv = SocketServer.UDPServer((sys.argv[1], int(sys.argv[2])), EchoHandler)
        print "Listening..."
        serv.serve_forever()
