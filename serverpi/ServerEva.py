import socket
import serial
import threading

class ServerEva:
    def __init__(self,host,port):
        self.host = host
        self.port = port
        self.serial_port = '/dev/ttyUSB0'
        self.buff_serial = 1024
        self.baudrate = 38400
        self.buff_sock = 1024
        self.run_thread = True
        self.serial = None
        self.sock_server = None
        self.server_thread = None
        self.client = None
        self.connectBot()
        self.startServer()

    def connectBot(self):
        self.serial = serial.Serial(port=self.serial_port,baudrate=self.baudrate)
        print "Eva Connected"

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
        print msg
        if msg == "AA":
            self.serial.write("$A,35,60,35,60\r\n")
        elif msg == "BB":
            self.serial.write("$A,-35,60,-35,60\r\n")
        elif msg == "DD":
            self.serial.write("$A,-20,20,20,20\r\n")
        elif msg == "DD2":
            self.serial.write("$A,-20,40,20,40\r\n")
        elif msg == "DIST":
            print "TODO"
        elif msg == "CC":
            self.serial.write("$A,20,20,-20,20\r\n")
        elif msg == "CC2":
            self.serial.write("$A,20,40,-20,40\r\n")
        elif msg == "EE":
            self.serial.write("$P,0\r\n")
        elif msg == "FF":
            self.serial.write("$P,1\r\n")
        elif msg == "SS":
            print "TODO"
        elif msg == "PP":
            self.serial.write("$A,10,10,10,10\r\n")
        elif msg == "CLOSE":
            self.run_thread = False
            self.client.send("connection close")


def main():
    server = ServerEva('192.168.1.205',8080)

if __name__ == '__main__':
    main()
