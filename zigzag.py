#x is normal to the plane.
#y is running from left to right.
#z is running from bottom to top.

import sys
import math
from atom import Atom

def print_xyz_cart(atoms):
    print len(atoms)
    print " "
    for atom in atoms:
        print atom

def print_poscar(atoms,a,b,c):
    species = ["Ge", "H"]
    nspecies = [0, 0]

    for atom in atoms:
        index = species.index(atom.symbol)
        ncnt = nspecies[index] + 1
        nspecies[index] = ncnt

    print "comment"
    print "1.00"
    print "%16.12f\t%16.12f\t%16.12f" % ( a,0.0,0.0)
    print "%16.12f\t%16.12f\t%16.12f" % ( 0.0,b,0.0)
    print "%16.12f\t%16.12f\t%16.12f" % ( 0.0,0.0,c)
    print "Ge H"
    print nspecies[0], nspecies[1]
    print "Direct"
    for atom in atoms:
        if (atom.symbol == "Ge"):
            print "%16.12f\t%16.12f\t%16.12f" % ( atom.x/a,atom.y/b,atom.z/c)
    for atom in atoms:
        if (atom.symbol == "H"):
            print "%16.12f\t%16.12f\t%16.12f" % ( atom.x/a,atom.y/b,atom.z/c)
    

def print_siesta(atoms,a,b,c):
    print "SystemName  MoS2"
    print "SystemLabel MoS2"
    print "NumberOfAtoms  ", len(atoms)
    print "NumberOfSpecies 3"
    print "%block ChemicalSpeciesLabel"
    print "1 42 Mo"
    print "2 16 S"
    print "3 1  H"
    print "%endblock ChemicalSpeciesLabel"
    print "LatticeConstant 1.0 Ang"
    print "%block LatticeVectors"
    print "%16.12f\t%16.12f\t%16.12f" % ( a,0.0,0.0)
    print "%16.12f\t%16.12f\t%16.12f" % ( 0.0,b,0.0)
    print "%16.12f\t%16.12f\t%16.12f" % ( 0.0,0.0,c)
    print "%endblock LatticeVectors"
    print "AtomicCoordinatesFormat Fractional"
    print "%block AtomicCoordinatesAndAtomicSpecies"
    for atom in atoms:
        isp = 0
        if (atom.symbol == "Mo"):
            isp = 1
        if (atom.symbol == "S"):
            isp = 2
        if (atom.symbol == "H"):
            isp = 3
        print "%16.12f\t%16.12f\t%16.12f\t%d\t%s" % ( atom.x/a,atom.y/b,atom.z/c,isp,atom.symbol)
    print "%endblock AtomicCoordinatesAndAtomicSpecies"
    
def center(atoms):
    ymin = 100000
    ymax = -100000
    for atom in atoms:
        if atom.y > ymax:
            ymax = atom.y
        if atom.y < ymin:
            ymin = atom.y

    ymid = (ymin+ymax)/2.0
    for atom in atoms:
        atom.y = atom.y - ymid


def passivate(atoms):
    a0 = atoms[0]
    a_0 = atoms[-3]
    atoms.append(Atom("H", 0, a0.y-1.2, a0.z))
    atoms.append(Atom("H", 0, a_0.y+1.2, a_0.z))
#    atoms.append(Atom("H", a_1.x, a_1.y+1.2, a_1.z))
             
d = 3.97469
a = d/math.sqrt(3.0)
Si_Si = a

yshift = a*3.0/2.0

unit0 = [
    Atom("Ge", -0.36645, 0.0, 0.0),
    Atom("Ge",  0.36645, a/2.0, a*math.sqrt(3.0)/2.0),
    Atom("H", -1.917, 0.0, 0.0),
    Atom("H",  1.917, a/2.0, a*math.sqrt(3.0)/2.0)
    ]
unit1 = [
    Atom("Ge", -0.36645, 0.0, a*math.sqrt(3.0)/2.0),
    Atom("Ge", 0.36645, a/2.0, 0.0),
    Atom("H", -1.917, 0.0, a*math.sqrt(3.0)/2.0),
    Atom("H", 1.917, a/2.0, 0.0)
    ]
nwidth = int(sys.argv[1])
nz = int(sys.argv[2])

uatoms = []

for n in range(nwidth):
    yoff = n*yshift
    if (n % 2 == 0):
        for atom in unit0:
            x = atom.x
            y = atom.y + yoff
            z = atom.z
            uatoms.append(Atom(atom.symbol,x,y,z))
    if (n%2 == 1):
        for atom in unit1:
            x = atom.x
            y = atom.y + yoff
            z = atom.z
            uatoms.append(Atom(atom.symbol,x,y,z))
            
passivate(uatoms)

satoms = []
for n in range(nz):
    for atom in uatoms:
        x = atom.x
        y = atom.y
        z = atom.z + n*d
        satoms.append(Atom(atom.symbol,x,y,z))

center(satoms)
#print_xyz_cart(satoms)
lx = 15.0
ly = nwidth*3.0*a/2.0 + 15.0
lz = d*nz
print_poscar(satoms,lx,ly,lz)
#print_siesta(satoms,lx,ly,lz)
