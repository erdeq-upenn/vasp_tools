from string import *
import sys
import math

AtomSymbol = [ 'x','h','he','li','be','b','c','n','o','f','ne', \
     'na','mg','al','si','p','s','cl','ar','k','ca','sc','ti', \
     'v','cr','mn','fe','co','ni','cu','zn','ga','ge','as','se', \
     'br','kr','rb','sr','y','zr','nb','mo','tc','ru','rh','pd', \
     'ag','cd','in','sn','sb','te','i','xe','cs','ba','la','ce', \
     'pr','nd','pm','sm','eu','gd','tb','dy','ho','er','tm','yb', \
     'lu','hf','ta','w ','re','os','ir','pt','au','hg','tl','pb', \
     'bi','po','at','fr','rn','ra','ac','th','pa','u','np','pu', \
     'am','cm','bk','cf','es','fm','md','no','lr' ]

class Atom:
    def __init__(self, symbol, x=0.0,y=0.0,z=0.0):
        self.symbol = symbol
        self.x = x
        self.y = y
        self.z = z
        self.setAtomNo()
        self.index = 0
        if self.symbol == "C":
            self.index = 1
        if self.symbol == "H":
            self.index = 2

    def setAtomNo(self):
        self.atomno = AtomSymbol.index(lower(self.symbol))

    def __str__(self):
        line = ('  %16.12f\t%16.12f\t%16.12f\t%d\t%s') \
               % (self.x, self.y, self.z, self.index, self.symbol)
        return line


def distance(a1,a2):
    x = a1.x - a2.x
    y = a1.y - a2.y
    z = a1.z - a2.z
    s = x*x + y*y + z*z
    return math.sqrt(s)

def output_siesta(atoms):
    print "NumberOfAtoms    ", len(atoms)
    print "NumberOfSpecies  2"
    print "%block ChemicalSpeciesLabel"
    print " 1    6    C"
    print " 2    1    H"
    print "%endblock ChemicalSpeciesLabel"
    print "LatticeConstant    1.0 Ang"
    print "%block LatticeVectors"
    print "  40.00    0.00    0.00"
    print "   0.00   40.00    0.00"
    print "   0.00    0.00   16.50"
    print "%endblock LatticeVectors"
    print "AtomicCoordinatesFormat Ang"
    print "%block AtomicCoordinatesAndAtomicSpecies"
    for atom in atoms:
        print atom
    print "%endblock AtomicCoordinatesAndAtomicSpecies"


def output_xyz(atoms):
    print len(atoms)
    print ""
    for atom in atoms:
        print atom.symbol, atom.x, atom.y, atom.z

pfile = open(sys.argv[1])
lines = pfile.readlines()
pfile.close()

atoms = []

nstart = 15
for n in range(nstart, nstart+512):
    line = lines[n]
    sline = line.split()
    x = float(sline[0])
    y = float(sline[1])
    z = float(sline[2])
    symbol = sline[4]
    if symbol == "C":
        atom = Atom(symbol,x,y,z)
        atoms.append(atom)


bonds = []

nlen = len(atoms)
for n1 in range(nlen):
    a1 = atoms[n1]
    bonds.append([])
    bonds[-1].append(n1)
    for n2 in range(nlen):
        if n1 == n2:
            continue
        a2 = atoms[n2]
        dis = distance(a1,a2)
        
        if (dis < 1.48):
            bonds[-1].append(n2)

for b in bonds:
    if len(b) == 3:
        a0 = atoms[b[0]]
        a1 = atoms[b[1]]
        a2 = atoms[b[2]]
        x = (a2.x - a0.x) + (a1.x - a0.x)
        y = (a2.y - a0.y) + (a1.y - a0.y)
        z = (a2.z - a0.z) + (a1.z - a0.z)
        x = -0.8*x + a0.x
        y = -0.8*y + a0.y
        z = -0.8*z + a0.z
        atoms.append(Atom("H",x,y,z))
    
    if len(b) == 2:
        n0 = b[0]
        n1 = b[1]
        b1 = bonds[n1]
        nn = []
        for n in b1[1:]:
            if n == n0:
                continue
            nn.append(n)
        
        n2 = nn[0]
        n3 = nn[1]
        
        a0 = atoms[n0]
        a1 = atoms[n1]
        a2 = atoms[n2]
        a3 = atoms[n3]
        
        scale = 0.7
        
        x = -scale*(a3.x - a1.x) + a0.x
        y = -scale*(a3.y - a1.y) + a0.y
        z = -scale*(a3.z - a1.z) + a0.z
        
        atoms.append(Atom("H",x,y,z))
        
        x = -scale*(a2.x - a1.x) + a0.x
        y = -scale*(a2.y - a1.y) + a0.y
        z = -scale*(a2.z - a1.z) + a0.z
        
        atoms.append(Atom("H",x,y,z))


output_siesta(atoms)
#output_xyz(atoms)
    
#for atom in atoms:
#    print atom
    
