#!/usr/bin/python
'''
	Original Author: Igor Maculan - n3wtron@gmail.com
	A Simple mjpg stream http server
	Added commnand server for UMSS project DroneSimon
'''
import threading

import cv2
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import StringIO
import time

import VisualFilters
import Reconocedor_Fuego_Humo
from PIL import Image

capture=None
mode = 0

class CommandHandler(BaseHTTPRequestHandler):

	def do_GET(self):
		global mode
		print self.path
		cmd = self.path
		self.send_response(200)
		if cmd == "/?cmd=0" :
			mode = VisualFilters.NADA
		if cmd == "/?cmd=1" :
			mode = VisualFilters.RESALTAR_CUERPOS
		elif cmd == "/?cmd=2" :
			mode = VisualFilters.RESALTAR_HUMO
		elif cmd == "/?cmd=3" :
			mode = VisualFilters.RESALTAR_FUEGO
		elif cmd == "/?cmd=4" :
			mode = VisualFilters.RESALTAR_BORDES
		elif cmd == "/?cmd=5" :
			mode = VisualFilters.RESALTAR_LINEAS_RECTAS
		elif cmd == "/?cmd=6" :
			mode = VisualFilters.RESALTAR_AZUL
		elif cmd == "/?cmd=7" :
			mode = VisualFilters.RESALTAR_ROJO
		elif cmd == "/?cmd=8" :
			mode = VisualFilters.RESALTAR_VERDE
		elif cmd == "/?cmd=9" :
			mode = VisualFilters.RESALTAR_BLANCO
		elif cmd == "/?cmd=10" :
			VisualFilters.inicializarMOG()
			mode = VisualFilters.DETECTAR_MOVIMIENTO
		elif cmd == "/?cmd=11" :
			mode = VisualFilters.RESALTAR_COLORES_FUEGO

class CamHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		if self.path.endswith('.mjpg'):
			self.send_response(200)
			self.send_header('Content-type','multipart/x-mixed-replace; boundary=--jpgboundary')
			self.end_headers()
			while True:
				try:
					rc,img = capture.read()
					if not rc:
						continue
					if mode == VisualFilters.RESALTAR_COLORES_FUEGO :
						img = VisualFilters.aumentarIntensidadPorRangoDeColor(img, 0, 18, 105, 255, 183, 255)

					if mode == VisualFilters.RESALTAR_BORDES:
						img = VisualFilters.encontrarBordesCanny(img)

					if mode == VisualFilters.DETECTAR_MOVIMIENTO:
						img = VisualFilters.detectarMovimiento(img)

					if mode == VisualFilters.RESALTAR_LINEAS_RECTAS:
						img = VisualFilters.marcarRectas(img)

					if mode == VisualFilters.RESALTAR_HUMO:
						img, porc = Reconocedor_Fuego_Humo.detectar_humo(img)

					if mode == VisualFilters.RESALTAR_FUEGO:
						img, porc = Reconocedor_Fuego_Humo.detectar_fuego(img)

					if mode == VisualFilters.RESALTAR_AZUL:
						img = VisualFilters.resalteColor(img, VisualFilters.PARAMETRO_AZUL)

					if mode == VisualFilters.RESALTAR_ROJO:
						img = VisualFilters.resalteColor(img, VisualFilters.PARAMETRO_ROJO)

					if mode == VisualFilters.RESALTAR_VERDE:
						img = VisualFilters.resalteColor(img, VisualFilters.PARAMETRO_VERDE)

					if mode == VisualFilters.RESALTAR_BLANCO:
						img = VisualFilters.resalteColor(img, VisualFilters.PARAMETRO_BLANCO)

					imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
					jpg = Image.fromarray(imgRGB)
					tmpFile = StringIO.StringIO()
					jpg.save(tmpFile,'JPEG')
					self.wfile.write("--jpgboundary")
					self.send_header('Content-type','image/jpeg')
					self.send_header('Content-length',str(tmpFile.len))
					self.send_header('Date', str(11-11-1111))
					self.send_header('mime-type', "image/jpeg")
					self.end_headers()
					jpg.save(self.wfile,'JPEG')
					time.sleep(0.05)
				except KeyboardInterrupt:
					break
			return
		if self.path.endswith('.html'):
			self.send_response(200)
			self.send_header('Content-type','text/html')
			self.end_headers()
			self.wfile.write('<html><head></head><body>')
			self.wfile.write('<img src="http://127.0.0.1:8080/stream.mjpg"/>')
			self.wfile.write('</body></html>')
			return

class CommandThread ( threading.Thread ):

   def run ( self ):
		server = HTTPServer(('',8081), CommandHandler)
		print "command server started"
		server.serve_forever()


def main():
	global capture
	capture = cv2.VideoCapture(0)
	capture.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 640);
	capture.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 480);
#	capture.set(cv2.cv.CV_CAP_PROP_SATURATION,0.2);
	global img
	try:
		cmdserver = CommandThread()
		cmdserver.start()

		server = HTTPServer(('',8080),CamHandler)
		print "streaming server started"
		server.serve_forever()
	except KeyboardInterrupt:
		capture.release()
		server.socket.close()

if __name__ == '__main__':
	main()
