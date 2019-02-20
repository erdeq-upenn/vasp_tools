#!/usr/bin/env python
"""
Plotting the bands of siesta
"""

import sys
import numpy as np
import matplotlib.pyplot as plt

from matplotlib import rc

class siestabands:
    def __init__(self,lines):
        self.fermi = 0.0
        self.nkpt = 0
        self.emin = 0
        self.emax = 0
        self.kmin = 0
        self.kmax = 0
        self.nbands = 0
        self.ispin = 1
        self.bands = []
        self.kval = []
        nline = len(lines)
        for n in range(nline):
            line = lines[n]
            if (line.find("E_F") > -1):
                self.parse_fermi(line)
            if (line.find("k_min") > -1):
                self.parse_krange(line)
            if (line.find("E_min") > -1):
                self.parse_erange(line)
            if (line.find("Nbands") > -1):
                self.parse_nbands(line)
            if (line.find("#") == -1):
                break
            
        self.parse_bands(lines[n:])
        
#        self.print_info()
#        self.print_whole()

    def print_whole(self):
        for n in range(self.nbands):
            for ik in range(self.nkpt):
                print '%12.6f %12.6f' % (self.kval[ik], self.bands[n][ik])
            print 
            print 

    def print_info(self):
        print "Fermi level ", self.fermi
        print "nkpt ", self.nkpt
        print "kmin, kmax ", self.kmin, self.kmax
        print "nbands, ispin", self.nbands, self.ispin
        
    def parse_nbands(self,line):
        sline = line.split()
        self.nbands = int(sline[5])
        self.ispin = int(sline[6])
        self.nkpt = int(sline[7])
        
    def parse_krange(self,line):
        sline = line.split()
        self.kmin = float(sline[4])
        self.kmax = float(sline[5])
    def parse_erange(self,line):
        sline = line.split()
        self.emin = float(sline[4])
        self.emax = float(sline[5])

    def parse_fermi(self,line):
        sline = line.split()
        self.fermi = float(sline[3])

    def parse_bands(self,lines):
        for n in range(self.nbands):
            n1 = (self.nkpt+2)*n
            n2 = n1 + self.nkpt
            self.parse_band(lines[n1:n2])
    
    def parse_band(self,lines):
        self.bands.append([])
        for line in lines:
            sline = line.split()
            if (len(self.kval) < self.nkpt):
                self.kval.append(float(sline[0]))
                
            self.bands[-1].append(float(sline[1]))
   

class drawbands:
    def __init__(self,siesta,ymin,ymax):
        self.kval = siesta.kval
        self.bands = siesta.bands
        self.ymin = ymin
        self.ymax = ymax
        self.xmin = siesta.kmin
        self.xmax = siesta.kmax
        self.fermi = siesta.fermi
        rc('text', usetex=True)
#        rc('font', family='serif')
        
    def plot(self):        
        nbands = len(self.bands)
        plt.figure(figsize=(7,10))
        for n in range(nbands):
            plt.plot(self.kval, self.bands[n], color='black')
            
#        nkpt = len(self.kval)
#        fermiline = []
#        for n in range(nkpt):
#            fermiline.append(self.fermi)
#        plt.plot(self.kval, fermiline, color='red')

        plt.xticks((self.xmin, self.xmax),(r'\Gamma', r'X'),fontsize=16)        
        plt.ylim(self.ymin, self.ymax)
        plt.xlim(self.xmin, self.xmax)
        plt.ylabel('Energy (eV)', fontsize=16)
#        plt.show()
        plt.savefig("bands.pdf", format='pdf')
        plt.savefig("bands.png", format='png')
        
def main():
    datafile = sys.argv[1]
    file = open(datafile, 'r')
    ymin = float(sys.argv[2])
    ymax = float(sys.argv[3])
    lines = file.readlines()
    siesta = siestabands(lines)
    drawbd = drawbands(siesta,ymin,ymax)
    drawbd.plot()
    file.close()

if __name__ == '__main__':
    main()
