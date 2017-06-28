import numpy as np
import math
import cv2
class Posicionamiento:

    def __init__(self):
        self.LOWER_RED = np.array([0,0,100])
        self.UPPER_RED = np.array([80,80,255])
        self.LOWER_BLUE = np.array([100, 0, 15])
        self.UPPER_BLUE = np.array([255, 100, 100])
        self.blanco_bajo = np.array([0, 0, 170])
        self.blanco_alto = np.array([255, 200, 255])
        
        self.amarillo_bajo = np.array([15, 30, 20])
        self.amarillo_alto = np.array([25, 275, 255])
        
        self.centro = (160, 240)
        self.areas = {'100':1218, '90':1395, '80':1557.5,'70':1973.5, '60':2620.5, '50':3356.5, '40':6485.0, '30':6601.0, '20':10545.5}

    def obtener_datos_forma(self, image, forma, color):
        image = cv2.resize(image, (10,10))
        mascara = self.obtener_mascara(image, color)

    def obtener_forma(self):
        pass

    def obtener_mascara(self, image, color):
        image = cv2.resize(image, (320, 240))
        mascara = None
        image = cv2.blur(image, (7,7))
        image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        if(color=='blue'):
            mascara = cv2.inRange(image, self.LOWER_BLUE, self.UPPER_BLUE)
            mascara = cv2.erode(mascara, (5,5))
            mascara = cv2.dilate(mascara, (5,5))
            cv2.imshow("mask azul",mascara)
            cv2.imwrite("imgee.jpg",mascara)
        elif(color == 'red'):
            mascara = cv2.inRange(image, self.LOWER_RED, self.UPPER_RED)
            mascara = cv2.erode(mascara, (5, 5))
            mascara = cv2.dilate(mascara, (5, 5))
            cv2.imshow("mask azul",mascara)
            cv2.imwrite("imgee.jpg",mascara)
        elif(color == 'blanco'):
            mascara = cv2.inRange(image_hsv, self.blanco_bajo, self.blanco_alto)
            mascara = cv2.erode(mascara, (5, 5))
            mascara = cv2.dilate(mascara, (5, 5))
        elif(color == 'amarillo'):
            mascara = cv2.inRange(image_hsv, self.amarillo_bajo, self.amarillo_alto)
            mascara = cv2.erode(mascara, (5, 5))
            mascara = cv2.dilate(mascara, (5, 5))
        cv2.imshow("mask",mascara)
        return mascara
        
    def obtener_contornos(self, mascara):
		_,contours, inheriters = cv2.findContours(mascara, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		pos =[]
		for c in contours:
			moments = cv2.moments(c)
			# Se verifica si el area es mayor a 500
			if moments['m00'] > 0:
				try:
					cx = int(moments['m10'] / moments['m00'])
					cy = int(moments['m01'] / moments['m00'])
					pos.append([cx,cy])
				except Exception:
								print Exception.message
		return pos

    def obtener_area(self, mascara):
        mat_areas = []
        _, contours, inheriters = cv2.findContours(mascara, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for c in contours:
            moments = cv2.moments(c)
            if moments['m00'] > 100:
                #print moments['m00']
                try:
                    cx = int(moments['m10']/moments['m00'])#punto centroide x
                    cy = int(moments['m01']/moments['m00'])
                    mat_areas.append([c, moments['m00'], cx, cy])
                except Exception:
                    print Exception 
        return mat_areas
		
    def pintar_centroide(self, mat_areas, img):
        for [c, area, cx, cy] in mat_areas:
            cv2.circle(img, (cx, cy), 3, (0, 255, 0), -1)
            #print area
            angulo = self.obtener_angulo(cx, cy)
            #cv2.putText(img, str(area))#, org, fontFace, fontScale, color[, thickness[, lineType[, bottomLeftOrigin]]])
            #cv2.putText(img, str(area), (cx, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.4,(0,0,0))#,cv2.CV_AA)
            cv2.putText(img, str(angulo), (cx, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.4,(0,0,0))#,cv2.CV_AA)

        return img

    def obtener_distancia_aprox(self, mat_areas):
        for [c, area] in mat_areas:
            if(area<100 and area>0):
                #buscar distancia del area
                pass

    def obetener_centro_imagen(self):
        pass

    def obtener_angulo(self, x, y):
        (cx, cy) = self.centro
        angulo = math.atan2(y-cy, x-cx)
        angulo = math.degrees(angulo)*(-1)
        # con el centroide obtener el angulo respecto al punto meio de la imagen
        return angulo
    def get_auto(self, imagen):
		img = cv2.resize(imagen, (320, 240))
		mascara = d.obtener_mascara(img, "amarillo")
		pos = d.obtener_contornos(mascara)
		return pos
		
    def get_contornos(self, imagen, color):
		img = cv2.resize(imagen, (320, 240))
		mascara = d.obtener_mascara(img, color)
		pos = d.obtener_contornos(mascara)
		return pos
		
    def get_forma(self, imagen, color):
        img = cv2.resize(imagen, (320, 240))
        mascara = d.obtener_mascara(img, color)
        pos = d.obtener_contornos(mascara)
        mat_area = d.obtener_area(mascara)
        img = d.pintar_centroide(mat_area, img)
        return img
d = Posicionamiento()
        
