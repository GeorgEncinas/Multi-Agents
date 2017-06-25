#!/usr/bin/python2.7
import bluetooth
import socket
import time

host = "192.168.1.119"
bt_address = '20:13:05:15:05:44'
port = 1

blue_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
blue_sock.connect((bt_address,port))
print "connected"

def procesar_mensaje(msg):
    if msg == "AA":
        blue_sock.send("$A,25,40,25,40\r\n")
    elif msg == "BB":
        blue_sock.send("BB")
        time.sleep(1)
        res = blue_sock.recv(1024)
        time.sleep(1)
        client.send(res)
    elif msg == "DD":
        blue_sock.send("DD")
        time.sleep(1)
        res = blue_sock.recv(1024)
        time.sleep(1)
        client.send(res)
    elif msg == "DIST":
        blue_sock.send("DIST")
        time.sleep(1)
        dist = blue_sock.recv(1024)
        time.sleep(1)
        client.send(dist)
    elif msg == "CC":
        blue_sock.send("CC")
        time.sleep(1)
        res = blue_sock.recv(1024)
        time.sleep(1)
        client.send(res)
    elif msg == "EE":
        blue_sock.send("$P,0\r\n")
    elif msg == "FF":
        blue_sock.send("$P,1\r\n")
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

    
