##### This code is an Interface for geometry creation #####
from Bezier_Curve_Geometry import Bezier_Curve_generator
import numpy as np

def Generate_Airfoil(gen):
    name = './base'
    upx = np.linspace(0,1, 50)
    downx = upx

    upy = [0] * 50
    downy = [0] * 50
    # Leading edge
    upy[1] = gen[0]

    downy[1] = -1 * float(gen[1])

    for i in range(2,len(gen)-3):
        upy[i] = float(gen[i]) + float(gen[i+3])
        downy[i] = float(gen[i]) - float(gen[i+3])

    n = 300
    MyBezier = Bezier_Curve_generator(50)
    pupx = MyBezier.curve_interpolation(upx, n)
    pupy = MyBezier.curve_interpolation(upy, n)
    pdownx = MyBezier.curve_interpolation(downx, n)
    pdowny = MyBezier.curve_interpolation(downy, n)

    foilfile = open(name + ".dat", 'w')
    foilfile.write(name + "\n")
    for i in range(n, 0, -1):
        foilfile.write(" %1.6f    %1.6f\n" % (pupx[i], pupy[i]))
    for i in range(0, n + 1):
        foilfile.write(" %1.6f    %1.6f\n" % (pdownx[i], pdowny[i]))
    foilfile.close()
