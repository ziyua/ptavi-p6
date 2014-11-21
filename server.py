#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import random
import SocketServer
import sys
import os
import re


class EchoHandler(SocketServer.DatagramRequestHandler):
    """
    Echo server class
    """

    PROTOCOL = r'(INVITE|ACK|BYE|CANCEL|OPTIONS|REGISTER)\ssip:\w+@(\w+|\d+(\.\d+){3}):\d+\sSIP/2.0'
    PORT_RTP = random.randint(1024, 65535)

    def send_single(self, text):
        print 'Send -- ', text[:-4]
        self.socket.sendto(text, self.client_address)  # send Tring Ring and ACK # Port sip: 5060
        # self.wfile.write(text)

    def handle(self):
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read().strip()
            # Recive INVITE|ACK|BYE sip:receptor@IP:port SIP/2.0
            m = re.match(self.PROTOCOL, line)
            if not m is None:
                if line.split()[0] == 'INVITE':
                    # INVITE: client --> servidor: Src Port (client): ca-2 (5065),          Dst Port (servidor): sip (5060) igual a ACK  or BYE
                    # 100 Trying
                    self.send_single('SIP/2.0 100 Trying\r\n\r\n')
                    # 180 Ring
                    self.send_single('SIP/2.0 180 Ring\r\n\r\n')
                    # Send 200 OK
                    self.send_single('SIP/2.0 200 OK\r\nm=audio ' + str(self.PORT_RTP) + ' RTP/AVP 8 101\r\n\r\n')
                elif line.split()[0] == 'ACK':
                    # ACK client -> servidor: Src Port (client)   : ca-2 (5065),           Dst Port (servidor)  : sip (5060); igual a INVITE  or BYE
                    #                                                                                                  |receive Port (Peer a Peer?)Puedo difinir 5060 ACK INVITE and BYE.)
                    #                                                                ++++++++++++son servidor+++++++++++
                    #                                                                |send Port (No puedo definir en mp32rtp.)
                    # RTP In sip.cap:         Src Port (servidor) : telelpathstart (5010), Dst Port (client)    : 12440 (12440)
                    #                 Dst port es <Random />.
                    #                 Src port es <5010 />
                    ip = self.client_address[0]
                    aEjecutar = './mp32rtp -i ' + ip + ' -p ' + str(self.PORT_RTP) + ' < ' + sys.argv[3]  # Port '23032' Dst es <Rondom />
                    print "Vamos a ejecutar $ ", aEjecutar
                    os.system(aEjecutar)  # 1. otro task
                    print '-- Send end --'
                elif line.split()[0] == 'BYE':
                    # Solo Send 200 OK
                    # BYE (client -> servidor): Src Port (client): ca-2 (5065), Dst Port (servidor): sip (5060); igual a INVITE  or ACK
                    self.send_single('SIP/2.0 200 OK\r\n\r\n')
                else:
                    # YES -> INVITE|ACK|BYE   NOT -> CANCEL|OPTIONS|REGISTER
                    self.send_single('SIP/2.0 405 Method Not Allowed\r\n\r\n')
            elif line:
                # bad msg:
                self.send_single('SIP/2.0 400 Bad Request\r\n\r\n')
            else:
                break


if __name__ == "__main__":
    if len(sys.argv) != 4 or not os.path.exists(sys.argv[3]):
        sys.exit('Usage: python server.py IP port audio_file')
    else:
        # Creamos servidor de eco y escuchamos
        serv = SocketServer.UDPServer(("", int(sys.argv[2])), EchoHandler)
        print "Listening..."
        serv.serve_forever()
