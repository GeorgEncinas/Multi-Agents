'''Donde g = grados y v = velocidad'''

def ai(grades, speed):
    if(grades>=0):
        points = ((grades/90)*40/2)
        return "$A,"+str(speed) + "," + str(points) + "," + str(-speed) + "," + str(points)
    #    cant_encoders = [speed, points, -speed, points]
    else:
        grades = -1 *grades
        points = ((grades/90)*40/2)
        return "$A,"+str(-speed) + "," + str(points) + "," + str(speed) + "," + str(points)
    #    cant_encoders = [-speed points, speed, points]
    #print(str(cant_encoders))

#ai(270, 20)
