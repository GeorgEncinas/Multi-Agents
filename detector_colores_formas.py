import numpy as np
import cv2
import math

class DetectorColoresFormas():

    def __init__(self):
        self.LOWER_RED = np.array([0, 0, 100])
        self.UPPER_RED = np.array([80, 80, 255])

        self.LOWER_BLUE = np.array([105, 50, 50])
        self.UPPER_BLUE = np.array([135, 255, 255])

        self.verde_bajos = np.array([25, 50, 50])
        self.verde_altos = np.array([90, 255, 255])
        self.LOWER_MAGENTA = np.array([100, 50, 50])
        self.UPPER_MAGENTA = np.array([240, 255, 255])

    def detectar_color_forma(self, imagen, color, forma):
        mascara = self._detectar_color(imagen, color)
        formas = self._detectar_forma(mascara, forma)
        return formas

    def detectar_forma(self, imagen, forma):
        mascara_azul = self._detectar_color(imagen, "blue")
        mascara_rojo = self._detectar_color(imagen, "red")
        mascara = cv2.add(mascara_azul, mascara_rojo)
        formas = self._detectar_forma(mascara, forma)
        return formas

    def detectar_color(self, imagen, color):
        mascara = self._detectar_color(imagen, color)
        objetos = self.obtener_centroides(mascara)
        return objetos

    def obtener_centroides(self, mascara):
        formas = []
        contornos, _ = cv2.findContours(mascara, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for c in contornos:
            momentos = cv2.moments(c)
            if momentos['m00'] > 300:
                try:
                    cx, cy = self.get_centroide(momentos)
                    formas.append((cx, cy))
                except Exception:
                    continue
        return formas

    def _detectar_color(self, imagen, color):
        imagen = cv2.blur(imagen, (7, 7))
        if (color == "blue"):
            imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)
            mascara = cv2.inRange(imagen, self.LOWER_BLUE, self.UPPER_BLUE)
            mascara = self.eliminar_ruido(mascara)
        elif (color == "red"):
            mascara = cv2.inRange(imagen, self.LOWER_RED, self.UPPER_RED)
            mascara = self.eliminar_ruido(mascara)
        elif (color == "magenta"):
            imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)
            mascara = cv2.inRange(imagen, self.LOWER_MAGENTA, self.UPPER_MAGENTA)
            mascara = self.eliminar_ruido(mascara)
        elif (color == "green"):
            imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)
            mascara = cv2.inRange(imagen, self.verde_bajos, self.verde_altos)
            mascara = self.eliminar_ruido(mascara)
        return mascara

    def eliminar_ruido(self, mascara):
        mascara = cv2.morphologyEx(mascara, cv2.MORPH_CLOSE, (5, 5), iterations=3)
        mascara = cv2.erode(mascara, (5, 5), iterations=3)
        return mascara

    def _detectar_forma(self, mascara, forma):
        formas = []
        contornos, _ = cv2.findContours(mascara, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for c in contornos:
            momentos = cv2.moments(c)
            if momentos['m00'] > 300:
                try:
                    approx = self.get_approx(c)
                    cx,cy = self.get_centroide(momentos)
                    tam_approx = len(approx)
                    if tam_approx >= 3:
                        j = 0
                        for i in range(0, tam_approx, 1):
                            a, b, c = self.get_posiciones(i, tam_approx)
                            [[x1, y1]], [[x2, y2]], [[x3, y3]] = approx[a], approx[b], approx[c]
                            angulo = self.get_angulo(x1, y1, x2, y2, x3, y3)
                            if (angulo > 80 and angulo < 100):
                                j += 1
                        if j >= 2 and forma == "cuadrado":
                            formas.append((cx, cy))
                        elif(j<2 and forma == "circulo"):
                            formas.append((cx, cy))
                except Exception:
                    continue
        return formas

    def get_posiciones(self, i, tam_approx):
        a, b, c = 0, i, 0
        if (i - 1) < 0:
            a = tam_approx - 1
        else:
            a = i - 1
        if (i + 1) >= tam_approx:
            c = 0
        else:
            c = i + 1
        return a, b, c

    def get_approx(self, contorno):
        epsilon = 0.01 * cv2.arcLength(contorno, True)
        approx = cv2.approxPolyDP(contorno, epsilon, True)
        return approx

    def get_centroide(self, momentos):
        cx = int(momentos['m10'] / momentos['m00'])
        cy = int(momentos['m01'] / momentos['m00'])
        return  cx, cy

    def get_angulo(self, x1, y1, x2, y2, x3, y3):
        mab = ((y2 - y1) / float(x2 - x1))
        mbc = ((y3 - y2) / float(x3 - x2))
        B = (mbc - mab) / float(1 + mbc * (mab))
        angulo = math.atan(B)
        grados = np.degrees(angulo)
        return abs(grados)

    def get_angulo_punto(self, imagen, x, y):
        tam_y, tam_x = np.size(imagen, 0), np.size(imagen, 1)
        cx, cy = tam_x/2, tam_y-1
        #cv2.circle(img, (cx, cy), 8, (255, 0, 0), thickness=3)
        angulo = math.atan2(y - cy, x - cx)
        angulo = math.degrees(angulo) * (-1)
        return int(angulo)-90

img = cv2.imread("C:\\Users\\Portatil\\Documents\\Universidad\\Materias\\AgentesInteligentes\\Imagens\\temp\\30cm\\14-33-38.jpg")
img = cv2.resize(img, (640, 480))

detector = DetectorColoresFormas()

res = detector.detectar_color(img, "blue")
#res = detector.detectar_color(img, "red")
#res = detector.detectar_forma(img, "cuadrado")
#res = detector.detectar_forma(img, "circulo")
#res = detector.detectar_color_forma(img, "blue", "cuadrado")
#res = detector.detectar_color_forma(img, "blue", "circulo")
#res = detector.detectar_color_forma(img, "red", "cuadrado")
#res = detector.detectar_color_forma(img, "red", "circulo")

print(str(len(res)))

for a in res:
    (x, y) = a
    angulo = detector.get_angulo_punto(img, x, y)
    cv2.circle(img, (x, y), 2, (255, 0, 200), thickness=2)
    cv2.putText(img, str(angulo), (x, y), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 0.4, (0, 0, 0))
cv2.imshow("Resultado", img)
cv2.waitKey(0)
