import socket
import time

#create an INET, STREAMing socket
robot4 = socket.socket(
    socket.AF_INET, socket.SOCK_STREAM)
#now connect to the web server on port 80
# - the normal http port
robot4.connect(("192.168.1.119", 8089))
while True:
    cmd = raw_input("comando >> ")
    robot4.send(cmd)
    respuesta = robot4.recv(1024)
    time.sleep(1)
    print respuesta





