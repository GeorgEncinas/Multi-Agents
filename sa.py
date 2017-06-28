import numpy as np
import cv2
import contorno
class GrillaPos:
	def __ini__(self):
		self.x=0
		self.y=0
		
	def lista_objetos(self, img, color, obje=None):
		dpos = contorno.Posicionamiento()
		if obje is not None:
			listaPosObjetos1 = dpos.get_contornos(img,'red')
			listaPosObjetos2 = dpos.get_contornos(img,'blue')
			lista_final = np.concatenate([listaPosObjetos1,listaPosObjetos2])
			return lista_final
		else :
				
			listaPosObjetos = dpos.get_contornos(img, color)
			return listaPosObjetos		
	def pos_ocupadas (self, obj):

		pos_oc =[];
		objetos = obj
		for ob in objetos:
			i = 0
			w = 0
			while i < 640:
				j=0
				q=0
				while j < 480:
					if ob[1]*2 > j and ob[1]*2 < j+40 :
						if ob[0]*2 > i and ob[0]*2 < i+40 :
							pos_oc.append([ob,[w,q]])
							j = j + 40
							q = q+1
						else: 
							
							j = j + 40
							q = q+1
					else:
						#print ob
						#print i,j
						j = j + 40
						q=q+1
				i = i + 40
				w=w+1
				
				
		return pos_oc
	#lista de pixeles cx cy de objetos mision 
	
	def mejor_mision(self, auto, pos_ob):
		x=16
		y=12
		mision = []
		ganador = []
		po = pos_ob
		ganadores =[]
		while len(po)>0:
			while mision in po:
				if mision[0]<auto[0]:
					if mision[1]<auto[1]:
						if x>auto[0]-mision[0] and y>auto[1]-mision[1]:
							x = auto[0]-mision[0]
							y = auto[1]-mision[1]
							ganador = mision
					else:
						if x > auto[0]-mision[0] and y > mision[1]-auto[1]:
							x = auto[0]-mision[0]
							y = mision[1]-auto[1]
							ganador = mision
				else:
					if mision[1]<auto[1]:
						if x > mision[0]-auto[0] and y > auto[1]-mision[1]:
							x = mision[0]-auto[0]
							y = auto[1]-mision[1]
							ganador = mision
					else :
						if x > mision[0]-auto[0] and y > mision[1]-auto[1]:
							x = mision[0]-auto[0]
							y = mision[1]-auto[1] 
							ganador = mision
				ganadores.append(ganador)
				po.remove(ganador)
		return ganadores
						
				
# Create a black image


# Draw a blue line with thickness of 5 px


d = GrillaPos()

img = cv2.imread("img13.jpg")
img = cv2.resize(img,(640,480))
#print pos_mis
objetoss = d.lista_objetos(img,"blue")
#ubucacion en grilla
pos_oc = d.pos_ocupadas(objetoss)
# mejor poscision con el auto
#pos_con_auto = d.mejor_mision([8,0],pos_oc)

print pos_oc

