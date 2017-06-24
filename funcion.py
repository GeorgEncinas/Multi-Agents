'''Donde g = grados y v = velocidad'''

def ai(g, v):
    if(g>=0):
        p = ((g/90)*40/2)
        A = [v, p, -v, p]
    else:
        g = -1 *g
        p = ((g/90)*40/2)
        A = [-v, p, v, p]
    print(str(A))

ai(270, 20)
