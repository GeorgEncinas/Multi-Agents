import time
import socket

class mover :
	def __init__(self, mision_r):
		self.hrom = True
		self.vrtm = True
		self.estado = 1 #1 horizontal 2 vertical
		self.retorno = True
		self.mision_rafo= mision_r
		
	def abrir_pinza(self):
		robot4.send("EE")
		
	def mover_auto (self , mision, auto, modo):
		y = -3
		x = -3
		ref = []
		iniy = 1	
		if mision[0]<auto[0]:
			if mision[1]<auto[1]:
					hro=False
					x = auto[0]-mision[0]
					vrt = False
					print "madito auto1"
					y = auto[1]-mision[1]
					ref = [hro,vrt]
			else:
				hro=False
				x = auto[0]-mision[0]
				vrt = True
				print "madito auto2"
				y = mision[1]-auto[1]
				iniy = 1
				ref = [hro,vrt]
		else:
			if mision[1]<auto[1]:
				hro=True
				x = mision[0]-auto[0]
				vrt = False
				print "madito auto3"
				y = auto[1]-mision[1]
				ref = [hro,vrt]
			else :
				hro = True
				x = mision[0]-auto[0]
				vrt = True
				print "madito auto4"
				y = mision[1]-auto[1] 
				iniy = 1
				ref = [hro,vrt]
				 
		print x,y		 
		
		print self.hrom
		if self.estado==1:
			if self.hrom != ref[0]:
				print "Vuelta"
				
				robot4.send("CC2")
				time.sleep(2)
				self.hrom = ref[0]
		if self.estado==0:
			if self.vrtm != ref[1]:
				print "Vuelta"
				
				robot4.send("CC2")
				time.sleep(2)
				self.vrtm = ref[1]
				
		while True:
			#mover en X
			if self.estado==1:
				if x > 0:
					print "mover 1x"
					x=x-1
					robot4.send("AA")
					time.sleep(1)
				else:
					if(y > 0):
						if iniy > 0 :
							if self.vrtm == True:
								if self.hrom == True :
									robot4.send("CC")
									print "der CC"
									time.sleep(1)
									self.estado=0
									iniy = 0
								else:
									robot4.send("DD")
									print "der DD"
									time.sleep(1)
									self.estado=0
									iniy = 0
							else :
								if self.hrom == True :
									robot4.send("CC")
									print "der CC1"
									time.sleep(1)
									self.estado=0
									iniy = 0
								else:
									robot4.send("DD")
									print "der DD1"
									time.sleep(1)
									self.estado=0
									iniy = 0
						
							
						print "mover 1y"
						y=y-1
						robot4.send("AA")
						time.sleep(1)
					else :
						break
			else: 
				if y > 0:
					print "mover 1y"
					y=y-1
					robot4.send("AA")
					time.sleep(1)
				else:
					if(x > 0):
						if iniy > 0 :
							if self.hrom == True:
								if self.vrtm == True :
									robot4.send("CC")
									print "der CC"
									time.sleep(1)
									self.estado=1
									iniy = 0
								else:
									robot4.send("DD")
									print "der DD"
									time.sleep(1)
									self.estado=1
									iniy = 0
							else :
								if self.vrtm == True :
									robot4.send("CC")
									print "der CC1"
									time.sleep(1)
									self.estado=1
									iniy = 0
								else:
									robot4.send("DD")
									print "der DD1"
									time.sleep(1)
									self.estado=1
									iniy = 0
						
							
						print "mover 1x de y"
						x=x-1
						robot4.send("AA")
						time.sleep(1)
					else :
						break
		print "ff"
		#mdo autonomo
		if modo == True :
			time.sleep(2)
			robot4.send("FF")	
		else:
			robot4.send("AA")
			time.sleep(1)
			robot4.send("EE")
			time.sleep(1)
			robot4.send("BB")
					
d = mover("{1:\"blue\",2:\"none\"}")
robot4 = socket.socket(
    socket.AF_INET, socket.SOCK_STREAM)
#now connect to the web server on port 80
# - the normal http port
robot4.connect(("192.168.0.102", 8080))
#para recto
autito = [2,4]
#para L
# dar valores para controlar la pocicion del auto y del objeto
#obj = [2,3]
#aut = [5,10]
objetitos = [[10, 5],[6,8],[4,5]]
for ob in objetitos:
	d.abrir_pinza()
	d.mover_auto(ob,autito,True)
	time.sleep(1)
	d.mover_auto(autito,ob,False)
	time.sleep(1)
	d.abrir_pinza()
	time.sleep(1)
robot4.send("CLOSE")
