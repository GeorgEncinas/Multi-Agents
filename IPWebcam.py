import cv2
import urllib2

class IPWebcam:
    def __init__(self,host):
        self.host = host
        self.port = '8080'
        self.url  = 'http://' + host + ':' + self.port + '/photo.jpg'
        self.filePath = '/tmp/foto_mapeo.jpg'
        self.conn = None
        self.mat = None

    def getPhoto(self):
        self.conn = urllib2.urlopen(self.url)
        photo = self.conn.read()
        temp_file = open(self.filePath,'w')
        temp_file.write(photo)
        temp_file.close()
        self.mat = cv2.imread(self.filePath)
        return self.mat

def main():
    webcam = IPWebcam("192.168.1.33")
    foto = webcam.getPhoto()
    cv2.imshow("foto",foto)
    cv2.waitKey(0)

if __name__ == '__main__':
    main()

        


