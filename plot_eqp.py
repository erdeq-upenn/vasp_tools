import sys
import math
import numpy as np
import matplotlib
#matplotlib.use('PDF')
import matplotlib.pyplot as plt
from matplotlib import rc


def dot_product(a1,a2):
    sum = 0.0
    for i in range(len(a1)):
        sum = sum + (a1[i]-a2[i])*(a1[i]-a2[i])
    return sum

def getlines(filname):
    fil = open(filname)
    lines = fil.readlines()
    fil.close()
    return lines

def readdata(lines):
    kpt = []    
    ev0 = []
    ev1 = []
    nline = len(lines)
    n = 0
    while n < nline:
        line = lines[n]
        n = n+1
        sl = line.split()
        kpt.append([float(sl[0]),
                    float(sl[1]),
                    float(sl[2])])
        nband = int(sl[3])
        ev0.append([])
        ev1.append([])
        for nb in range(nband):
            line = lines[n]
            n = n+1
            sl = line.split()
            ev0[-1].append(float(sl[2]))
            ev1[-1].append(float(sl[3]))
    return [kpt, ev0, ev1]

def reorder(ev0,ev1):
    nkpt = len(ev0)
    nband = len(ev0[0])
    nev0 = []
    nev1 = []
    for nb in range(nband):
        nev0.append([])
        nev1.append([])
        for nk in range(nkpt):
            nev0[-1].append(ev0[nk][nb])
            nev1[-1].append(ev1[nk][nb])
    return [nev0, nev1]

def distance(kpt):
    ks = [0.0]
    for n in range(1,len(kpt)):
        dis = math.sqrt(dot_product(kpt[n-1],kpt[n]))
        ks.append(dis)
    return ks
            
def drawbands(ks,ev,ev1):
    rc('text', usetex=True)
    rc('font', family='serif')
    rc('xtick', labelsize=16)
    rc('ytick', labelsize=16)
    nbands = len(ev)
    plt.figure(figsize=(6,5))
    plt.subplots_adjust(left=0.15,right=0.95,top=0.95,bottom=0.10)
    for n in range(nbands):
        plt.plot(ks,ev[n],color='black') 
        plt.plot(ks,ev1[n],color='blue')

    xmin = min(ks)
    xmax = max(ks)
    plt.xlim(xmin,xmax)
    plt.ylim(-5,3)
    plt.ylabel('Energy (eV)', fontsize=18)
    #        plt.show()
    plt.savefig("bands.pdf", format='pdf')
    plt.savefig("bands.png", format='png')

lines = getlines(sys.argv[1])
[kpt,ev0,ev1] = readdata(lines)
[ev0,ev1] = reorder(ev0,ev1)
ks = distance(kpt)
drawbands(ks,ev0,ev1)
print len(ks)
