#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
#Practica 6 - Miguel Angel Fernandez Sanchez
"""
Programa cliente que abre un socket a un servidor
"""

import socket
import sys

# Cliente UDP simple.
user_data = sys.argv
method_list = ['INVITE', 'BYE']
lista_ack = ['SIP/2.0', '100', 'Trying', 'SIP/2.0', '180', 'Ring',
                 'SIP/2.0', '200', 'OK']

if len(user_data) != 3:
    print "Usage: python client.py method receiver@IP:SIPport"
    raise SystemExit

user_info = user_data[2].split("@")
VER = "SIP/2.0"
RECEPTOR = user_info[0]
METODO = user_data[1]
# Comprobamos si el método es conocido
if METODO not in method_list:
    print "Unknown method -- Use 'INVITE' or 'BYE'"
    raise SystemExit

# Dirección IP del servidor.
# Comprobamos si el puerto introducido es correcto
IP = user_info[1].split(":")[0]
try:
    PORT = int(user_info[1].split(":")[1])
except TypeError:
    print "Usage: python client.py method receiver@IP:SIPport"
    raise SystemExit

# Contenido que vamos a enviar
LINE = METODO + " sip:" + RECEPTOR + "@" + IP + " " + VER + '\r\n\r\n'


# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto

my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
my_socket.connect((IP, PORT))

# Comprobamos si hay un servidor escuchando
try:
    LINE2 = 'INVITE pepe-batman@123.23.12.12 SIP/2.0'
    print "Enviando: " + LINE2
    my_socket.send(LINE2 + '\r\n')
    data = my_socket.recv(1024)
except socket.error:
    print "Error: No server listening at " + IP + " port " + str(PORT)
    raise SystemExit

print data

if data.split() == lista_ack:
    LINE = 'ACK sip:' + RECEPTOR + '@' + IP + " " + VER
    print "Enviando: " + LINE
    my_socket.send(LINE + '\r\n')
    data2 = my_socket.recv(1024)
    print data2
print "Terminando socket..."


# Cerramos todo
my_socket.close()
print "Fin."
