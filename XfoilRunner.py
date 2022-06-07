
import subprocess as sp
import os
import string
import pathlib
import matplotlib.pyplot as plt
import time
import numpy as np

plt.ion()
num = 0

xfoilpath = 'xfoil' # intalled in path Ubuntu 18.04 
current_path = str(pathlib.Path(__file__).parent.resolve())
print(current_path)
def Xfoil(Ncrit_Turbulence, Reynolds_Number ):
    def Cmd(cmd):
        msg = cmd+'\n'
        ps.stdin.write(msg.encode('utf-8'))
    try:
        os.remove('./base.log')
    except :
        pass
    ps = sp.Popen(xfoilpath ,stdin=sp.PIPE, shell = True)
    print('FILE PATH : ',f'load {current_path}/base.dat')
    Cmd(f'load base.dat')
    
    Cmd('PANE')
    Cmd('OPER')
    Cmd('iter 1000')
    Cmd('Vpar')
    Cmd('N '+str(Ncrit_Turbulence))
    Cmd(' ')   # For mach number, specify if any
    Cmd('visc '+str(Reynolds_Number))
    Cmd('PACC')
    Cmd('base.log')  
    Cmd(' ')          # For dump file
    Cmd('aseq 0.0 10.0 0.150')
    Cmd(' ')     # escape OPER
    Cmd('quit')  # exit
    ps.stdin.close()
    ps.wait()
    # print(msg)

def Fitness_Value_Calculator(plot = True):   # base contains the data for the latest airfoil.
    global num
    num += 1
    Name_of_file = current_path + "/base.log"
    file_object = open(Name_of_file, 'r')
    Line_reader = file_object.readlines()
    Fitness =0
    LD_rAtio = 0
    counter = 0
    for i in range(12,len(Line_reader)):
        counter +=1
        words = Line_reader[i].split()
        LD_rAtio += float(words[1])/float(words[2])
        if counter!=0:
            avg_LD = LD_rAtio / counter
            Fitness = avg_LD
        else:
            Fitness = 0
    if plot == True:
        plt.scatter([num], [Fitness])
        plt.draw()
        plt.pause(0.001)
    if counter>=5:
        return -1 * Fitness
    else :
        return 0
def Fitness_Value_Calculator_w_Tclcd(target_clcd, plot = True):   # base contains the data for the latest airfoil.
    global num
    num += 1
    Name_of_file = current_path + "/base.log"
    file_object = open(Name_of_file, 'r')
    Line_reader = file_object.readlines()
    Fitness =0
    LD_rAtio = 0
    counter = 0
    for i in range(12,len(Line_reader)):
        counter +=1
        words = Line_reader[i].split()
        LD_rAtio += float(words[1])/float(words[2])
        if counter!=0:
            avg_LD = LD_rAtio / counter
            Fitness = avg_LD
        else:
            Fitness = 0

    if plot == True:
        plt.scatter([num], [Fitness])
        plt.draw()
        plt.pause(0.001)

    if counter>=5:
        return np.abs(target_clcd - Fitness)
    else :
        return 0
