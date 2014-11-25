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
lista_ack = ['SIP/2.0', '100', 'Trying', 'SIP/2.0', '180',
             'Ringing', 'SIP/2.0', '200', 'OK']
usage = "Usage: python client.py method receiver@IP:SIPport"
if len(user_data) != 3:
    print usage
    raise SystemExit

user_info = user_data[2].split("@")
VER = "SIP/2.0"
RECEPTOR = user_info[0]
METODO = user_data[1]
# Comprobamos si el método es conocido
if METODO not in method_list:
    print usage
    raise SystemExit

# Dirección IP del servidor.
# Comprobamos si el puerto introducido es correcto
IP = user_info[1].split(":")[0]
try:
    PORT = int(user_info[1].split(":")[1])
except ValueError:
    print usage
    raise SystemExit

# Contenido que vamos a enviar
LINE = METODO + " sip:" + RECEPTOR + "@" + IP + " " + VER + '\r\n'

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto

my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
my_socket.connect((IP, PORT))

# Comprobamos si hay un servidor escuchando
try:
    print "Enviando: " + LINE
    my_socket.send(LINE + '\r\n')
    data = my_socket.recv(1024)
    print "Recibido: " + data
except socket.error:
    print "Error: No server listening at " + IP + " port " + str(PORT)
    raise SystemExit

if data.split() == lista_ack:
    LINE2 = 'ACK sip:' + RECEPTOR + '@' + IP + " " + VER
    print "Enviando: " + LINE2
    my_socket.send(LINE2 + '\r\n\r\n')
    data2 = my_socket.recv(1024)
    print "Recibido: " + data2
print "Terminando socket..."

# Cerramos todo
my_socket.close()
print "Fin."
