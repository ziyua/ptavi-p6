#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
#Practica 6 - Miguel Angel Fernandez Sanchez
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import SocketServer
import os
import sys

SERVER_DATA = sys.argv
if len(SERVER_DATA) != 4:
    print "Usage: python server.py IP port audio_file"
    raise SystemExit
IP = SERVER_DATA[1]
try:
    PORT = int(SERVER_DATA[2])
except TypeError:
    print "Usage: python server.py IP port audio_file"
    raise SystemExit
AUDIO_FILE = SERVER_DATA[3]

class SIPHandler(SocketServer.DatagramRequestHandler):
    """
    SIP server class
    """

    def handle(self):

        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            cadena = self.rfile.read()
            if cadena != "":
                list_words = cadena.split()
                if list_words[0] == 'INVITE':
                    correo = list_words[1]
                    correo = correo.split(":")[1]
                    trying = "SIP/2.0 100 Trying\r\n\r\n"
                    ring = "SIP/2.0 180 Ring\r\n\r\n"
                    twhd_ok = "SIP/2.0 200 OK\r\n\r\n"
                    self.wfile.write(trying)
                    self.wfile.write(ring)
                    self.wfile.write(twhd_ok)

            # Si no hay más líneas salimos del bucle infinito
            else:
                break

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    serv = SocketServer.UDPServer((IP, PORT), SIPHandler)
    print "Listening..."
    serv.serve_forever()
