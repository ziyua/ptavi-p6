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
                    resp = "SIP/2.0 100 Trying\r\n\r\n"
                    resp = resp + "SIP/2.0 180 Ring\r\n\r\n"
                    resp = resp + "SIP/2.0 200 OK\r\n\r\n"
                    self.wfile.write(resp)
                elif list_words[0] == 'BYE':
					self.wfile.write("SIP/2.0 200 OK\r\n\r\n")
                elif list_words[0] == "ACK":
                    os.system('chmod 755 mp32rtp')
                    to_exe = './mp32rtp -i 127.0.0.1 -p 23032 < ' + AUDIO_FILE
                    os.system(to_exe)
                else:
					self.wfile.write("SIP/2.0 405 Method Not Allowed\r\n\r\n")

            # Si no hay más líneas salimos del bucle infinito
            else:
                break

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    serv = SocketServer.UDPServer((IP, PORT), SIPHandler)
    print "Listening..."
    serv.serve_forever()
