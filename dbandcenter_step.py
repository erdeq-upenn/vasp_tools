import sys

class ATOMDOS:
    def __init__(self,lines):
        self.ep = []
        self.s = []
        self.p = []
        self.d = []
        self.parse(lines[1:])

        self.calc_d_center()
        self.calc_d_width()
        
    def calc_d_center(self):
        nedos = len(self.ep)
        ns = 0.0
        ds = 0.0
        for n in range(nedos):
         #   if (self.ep[n] > 1.0):
	#	continue
            ns = ns + self.ep[n] * self.d[n]
            ds = ds + self.d[n]

        self.d_center = ns / ds

    def calc_d_width(self):
        nedos = len(self.ep)
        ns = 0.0
        ds = 0.0
        for n in range(nedos):
            ns = ns + self.ep[n] * self.ep[n] * self.d[n]
            ds = ds + self.d[n]
        self.d_width = ns / ds

    def get_d_center(self):
        return self.d_center

    def get_d_width(self):
        return self.d_width
        
    def parse(self, lines):
        for line in lines:
            sl = line.split()
            en = float(sl[0])
            s = float(sl[1])
            p = float(sl[2])
            d = float(sl[3])
            self.ep.append(en)
            self.s.append(s)
            self.p.append(p)
            self.d.append(d)
            
    def get_ep(self):
        return self.ep

    def get_s(self):
        return self.s

    def get_p(self):
        return self.p

    def get_d(self):
        return self.d


        
    
class DOSCAR:
    def __init__(self,lines):
        self.natoms = self.getnatoms(lines[0])
        self.efermi = self.getefermi(lines[5])
        self.nedos = self.getnedos(lines[5])
        self.enmin = self.getenmin(lines[5])
        self.enmax = self.getenmax(lines[5])
        nstart = 5 + self.nedos
        self.parse(lines[nstart:])

    def parse(self,lines):
        self.atomdos = []
        for i in range(self.natoms):
            nstart = i*(self.nedos+1)
            nend = (i+1)*(self.nedos+1)
            self.atomdos.append(ATOMDOS(lines[nstart:nend]))
        
    def getenmin(self,line):
        sl = line.split()
        return float(sl[0])

    def getenmax(self,line):
        sl = line.split()
        return float(sl[1])
        
    def getnedos(self,line):
        sl = line.split()
        return int(sl[2])
        
    def getefermi(self,line):
        sl = line.split()
        return float(sl[3])
        
    def getnatoms(self,line):
        sl = line.split()
        return int(sl[0])

    def get_d_center(self,iatom):
        return self.atomdos[iatom].get_d_center() - self.efermi

    def get_d_center_avg(self):
        natom = len(self.atomdos)
        ed = 0.0
        for i in range(75,100):
            e = self.get_d_center(i)
#            print e
            ed = ed + e
        return ed / 25
            
f = open(sys.argv[1])
lines = f.readlines()
f.close()

doscar = DOSCAR(lines)

iatom = int(sys.argv[2])
ed = doscar.get_d_center(iatom)
print ed

