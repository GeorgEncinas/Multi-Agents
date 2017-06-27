import socket
import bluetooth
import threading

class ServerWalle:
    def __init__(self,host,port):
        self.host = host
        self.port = port
        self.bt_address = '00:15:FF:F3:E2:09'
        self.bt_port = 1
        self.buff_bt = 1024
        self.buff_sock = 1024
        self.run_thread = True
        self.blue_sock = None
        self.sock_server = None
        self.server_thread = None
        self.client = None
        self.connectBot()
        self.startServer()

    def connectBot(self):
        self.blue_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.blue_sock.connect((self.bt_address,self.bt_port))
        print "Walle Connected"

    def startServer(self):
        self.sock_server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sock_server.bind((self.host,self.port))
        self.sock_server.listen(5)
        self.server_thread = threading.Thread(target=self.serveForever)
        self.server_thread.start()

    def serveForever(self):
        (self.client, address) = self.sock_server.accept()
        print "Cliente Conectado"
        print address
        while self.run_thread:
            cmd = self.client.recv(self.buff_sock)
            self.processMessage(cmd)
        self.client.close()
        print "Coneccion cerrada"


    def processMessage(self,msg):
        if msg == "AA":
            self.blue_sock.send("AA")
            res = self.blue_sock.recv(self.buff_bt)
            self.client.send(res)
        elif msg == "BB":
            self.blue_sock.send("BB")
            res = self.blue_sock.recv(self.buff_bt)
            self.client.send(res)
        elif msg == "DD":
            self.blue_sock.send("DD")
            res = self.blue_sock.recv(self.buff_bt)
            self.client.send(res)
        elif msg == "DIST":
            self.blue_sock.send("DIST")
            dist = self.blue_sock.recv(self.buff_bt)
            self.client.send(dist)
        elif msg == "CC":
            self.blue_sock.send("CC")
            res = self.blue_sock.recv(self.buff_bt)
            self.client.send(res)
        elif msg == "EE":
            self.blue_sock.send("EE")
            res = self.blue_sock.recv(self.buff_bt)
            self.client.send(res)
        elif msg == "FF":
            self.blue_sock.send("FF")
            res = self.blue_sock.recv(self.buff_bt)
            self.client.send(res)
        elif msg == "SS":
            self.blue_sock.send("SS")
            res = self.blue_sock.recv(self.buff_bt)
            self.client.send(res)
        elif msg == "MSG":
            self.blue_sock.send("MSG")
            res = self.blue_sock.recv(self.buff_bt)
            self.client.send(res)
        elif msg == "CLOSE":
            self.run_thread = False
            self.client.send("connection close")


def main():
    server = ServerWalle('192.168.1.38',8080)

if __name__ == '__main__':
    main()

