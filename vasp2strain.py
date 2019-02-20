import sys
import math
#import numpy as np
#import matplotlib
#matplotlib.rcParams['mathtext.fontset'] = 'stix'
#matplotlib.use('PDF')
#matplotlib.use('Agg')
#import matplotlib.pyplot as plt
#from matplotlib import rc
#from matplotlib.collections import LineCollection
#rc('text',usetex = False)

def dot_product(a1,a2):
    sum = 0.0
    for i in range(len(a1)):
        sum = sum + (a1[i]-a2[i])*(a1[i]-a2[i])
    return sum

class KPOINTS:
    def __init__(self):
        f = open("BANDKS")
        lines = f.readlines()
        f.close()
        
        self.parse(lines)
        
    def parse(self, lines):
        self.nkpt = int(lines[1])
        nbandlines = (len(lines)-4+1)/3
        
        self.bandlimits = []
        self.bandsymbol = []
        nline = 3
        for n in range(nbandlines):            
            for i in range(2):
                nline = nline + 1
                sline = lines[nline].split()
                a = float(sline[0])
                b = float(sline[1])
                c = float(sline[2])
                self.bandlimits.append([a,b,c])
                self.bandsymbol.append(sline[-1])
            nline = nline + 1

        nn = 0
        self.spoint = {}
        self.kdist = []
        sum = 0.0
        for n in range(nbandlines):
            n1 = n*2
            n2 = n*2 + 1
            a1 = self.bandlimits[n1]
            a2 = self.bandlimits[n2]
            
            base = 0.0
            if len(self.kdist) >= 1:
                base = self.kdist[-1]
                
            for i in range(self.nkpt):
                a3 = [0,0,0]
                for j in range(len(a1)):
                    a3[j] = a1[j] + (a2[j]-a1[j])*i/(self.nkpt-1)
                
                l1 = base + math.sqrt(dot_product(a3,a1))
                self.kdist.append(l1)
                if i == 0 or i == self.nkpt-1:                    
                    if self.kdist[-1] in self.spoint:
                        if self.spoint[self.kdist[-1]][0] != self.bandsymbol[nn]:
                            self.spoint[self.kdist[-1]].append(self.bandsymbol[nn])
                    else:
                        self.spoint[self.kdist[-1]] = [self.bandsymbol[nn]]
                    nn = nn + 1
                    

class VaspBand:
    def __init__(self, lines, fermi, ymin, ymax, title):
        self.lines = lines
	self.fermi = fermi
        self.ymin = ymin
        self.ymax = ymax
	self.title = title
        self.get_info()
        self.get_energy()
        self.kp = KPOINTS()
        
    def draw_bands(self):
#        rc('text', usetex=True)
#        rc('font', family='serif')
#    	rc('xtick', labelsize=16)
#	rc('ytick', labelsize=16)
    
        self.vbm = []
        self.cbm = []
        
        nbands = self.nbands
#        plt.figure(figsize=(5,8))        
        for n in range(nbands):
            xs = []
            ys = []
            for k in range(self.nkpt):
                xs.append(self.kp.kdist[k])
                ys.append(self.evals[k][n])
            
#            for m in range(len(xs)):
#                print xs[m], ys[m]
                
#            print 

            if ( n == self.nele/2-1 ):
                self.vbm = ys
            if ( n == self.nele/2 ):
                self.cbm = ys
	
        self.fermi = (max(self.vbm) + min(self.cbm))/2.0
        gap = -max(self.vbm) + min(self.cbm)
	print max(self.vbm), min(self.cbm)
#	for i in range(len(self.vbm)):		
#            print i+1, self.vbm[i], self.cbm[i]
	
	# print "VBM"
	# nn=2
	# for i in range(nn,len(self.vbm)-nn):
	#     if (self.vbm[i] > self.vbm[i-nn] and self.vbm[i] > self.vbm[i+nn]):
	# 	print i+1, self.vbm[i]-self.fermi	    	    

	# print "CBM"
	# nn=2
	# for i in range(nn,len(self.cbm)-nn):
	#     if (self.cbm[i] < self.cbm[i-nn] and self.cbm[i] < self.cbm[i+nn]):
	# 	print i+1, self.cbm[i]-self.fermi	    	    

#        print self.fermi
        xt = []
        yt = []

        for key in self.kp.spoint:
            label = self.kp.spoint[key]
#            print key, label
            tics = ""
            if len(label) > 1:
                tics = label[0] + "(" + label[1] + ")"
            else:
                tics = label[0]
                        
            xt.append(key)
            yt.append(tics)
        
#            plt.axvline(key,color='black',ls='-')


    def make_bands(self):
        for n in range(self.nbands):
            for k in range(self.nkpt):
#                print k, self.evals[k][n]
                print self.kp.kdist[k], self.evals[k][n]
            
            print
            
        print "#", self.kp.spoint
            
    def get_info(self):
        line = self.lines[5]
        sline = line.split()
        self.nbands = int(sline[2])
        self.nkpt = int(sline[1])
     	self.nele = int(sline[0])
#	print self.nbands, self.nkpt
	   
    def get_energy(self):
        self.kpoints = []
        self.evals = []
        for n in range(self.nkpt):
            nstart = n*(2+self.nbands) + 7
            line = self.lines[nstart]
#	    print line
            sline = line.split()
            kx = float(sline[0])
            ky = float(sline[1])
            kz = float(sline[2])
            self.kpoints.append([kx,ky,kz])
            
            nstart = nstart + 1
            self.evals.append([])
            for m in range(self.nbands):
                nline = nstart + m
                line = self.lines[nline]
                sline = line.split()
                ev = float(sline[1]) - self.fermi
                self.evals[-1].append(ev)

                

def main():
    filename = sys.argv[1]
    ymin = float(sys.argv[2])
    ymax = float(sys.argv[3])
    title = sys.argv[4]
    file = open(filename, 'r')
    lines = file.readlines()
    vasp = VaspBand(lines, 0, ymin, ymax, title)
#    vasp.make_bands()
    vasp.draw_bands()

#    print "fermi=",vasp.fermi
#    print "maintitle=",'"',vasp.title,'"'

def main_kpoint():
    kp = KPOINTS()

if __name__ == '__main__':
    main()
