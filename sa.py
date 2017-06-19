import numpy as np
import cv2
import contorno
class GrillaPos:
	def __ini__(self):
		self.x=0
		self.y=0
		
	def lista_objetos(self, img):
		dpos = contorno.Posicionamiento()
		listaPosObjetos = dpos.get_contornos(img,'blanco')
		return listaPosObjetos
	
	def pos_ocupadas (self, img):

		pos_oc =[];
		objetos = d.lista_objetos(img)
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
	def pos_mision (self, pos, img):
		i = 0
		j = 0
		q = 0
		w = 0
		lista_pos_obmision = []
		for ob in pos:
			while i < 16:
				while j < 12:
					if pos[q,w][1] > (j*40) and pos[q,w][1] < (j*40)+40 :
						if pos[q,w][0] > (i*40) and pos[q,w][0] < (i*40)+40 :
							lista_pos_obmision.append([pos[q,w]],[i,j])
							j=j+1
							q=q+1
					else:
						j=j+1
						q=q+1
				w=w+1
		return pos_oc
		
		
		 
						
				
# Create a black image


# Draw a blue line with thickness of 5 px


d = GrillaPos()
r = contorno.Posicionamiento()


img = cv2.imread("img4.jpg")
img = cv2.resize(img,(640,480))
pos_mis = r.get_contornos(img,'blue')
#print pos_mis
pos_oc = d.pos_ocupadas(img)
print pos_oc
x=0
y=0
while x < 640 :
	cv2.line(img,(x,0),(x,640),(255,0,0),1)
	x=x+40
	
while y < 480 :
	cv2.line(img,(0,y),(640,y),(255,0,0),1)
	y=y+40
	
#Display the image
cv2.imshow("img",img)

cv2.waitKey(0)
