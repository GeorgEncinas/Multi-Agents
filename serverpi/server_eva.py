#!/usr/bin/python2.7
#import bluetooth
import socket
import time
import serial

host = "192.168.1.205"
#host = "localhost"
bt_address = '20:13:05:15:05:44'
port = 1
"""
ser = serial.Serial(
	port='/dev/ttyAMA0',
	baudrate = 9600,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS,
	timeout=1
)
"""

ser = serial.Serial(port='/dev/ttyUSB0',baudrate=38400)
print "Serial Connected"

"""
blue_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
blue_sock.connect((bt_address,port))
print "connected"
"""

def procesar_mensaje(msg):
    if msg == "AA":
        ser.write("$A,35,60,35,60\r\n")
    elif msg == "BB":
        ser.write("$A,-35,60,-35,60\r\n")
    elif msg == "DD":
		ser.write("$A,-20,20,20,20\r\n")
    elif msg == "DD2":
		ser.write("$A,-20,40,20,40\r\n")
    elif msg == "DIST":
        blue_sock.send("DIST")
        time.sleep(1)
        dist = blue_sock.recv(1024)
        time.sleep(1)
        client.send(dist)
    elif msg == "CC":
		ser.write("$A,20,20,-20,20\r\n")
    elif msg == "CC2":
		ser.write("$A,20,40,-20,40\r\n")
    elif msg == "EE":
        ser.write("$P,0\r\n")
    elif msg == "FF":
        ser.write("$P,1\r\n")
    elif msg == "SS":
        blue_sock.send("SS")
        time.sleep(1)
        res = blue_sock.recv(1024)
        time.sleep(1)
        client.send(res)
    elif msg == "CAPTURE":
        blue_sock.send("CAPTURE")
        time.sleep(1)
        res = blue_sock.recv(1024)
        time.sleep(1)
        client.send(res)
    elif msg == "MSG":
        blue_sock.send("MSG")
        time.sleep(1)
        res = blue_sock.recv(1024)
        time.sleep(1)
        client.send(res)
    elif msg == "PP":
        ser.write("$A,10,10,10,10\r\n")


server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((host,8089))
print "Agente escuchando en el puerto 8089"
server.listen(1)
(client, address) = server.accept()
print "cliente conectado"
print client
print address

while True:
    mensaje = client.recv(1024)
    print mensaje
    procesar_mensaje(mensaje)

    
