# only works for cubic structure

import sys

class Atom:
    def __init__(self, symbol, xyz):
        self.symbol = symbol
        self.x = xyz[0]
        self.y = xyz[1]
        self.z = xyz[2]

    def __str__(self):
        line = ('%s\t%16.12f\t%16.12f\t%16.12f') \
               % (self.symbol, self.x, self.y, self.z)
        return line



ATOMS = ["Li", "Mn", "O"]
NATOMS = [0, 0, 0]

f = open(sys.argv[1])
lines = f.readlines()
f.close()

latt_scale = float(lines[1])
latt_vec = [[0,0,0], [0,0,0],[0,0,0]]

n = 0
for nline in range(2,5):
    line = lines[nline]
    sline = line.split()
    for i in range(3):        
        latt_vec[n][i] = float(sline[i])
    n = n + 1

line = lines[5]
sline = line.split()

for i in range(len(sline)):
    NATOMS[i] = int(sline[i])

nline = 7
ucell = []
for na in range(len(NATOMS)):
    for ia in range(NATOMS[na]):
        line = lines[nline]
        sline = line.split()
        xyz = [0,0,0]
        for i in range(3):
            xyz[i] = float(sline[i])
        ucell.append(Atom(ATOMS[na],xyz))
                     
        nline = nline + 1

#make supercell
scell = []
nx = int(sys.argv[2])
ny = int(sys.argv[3])
nz = int(sys.argv[4])

for ix in range(nx):
    for iy in range(ny):
        for iz in range(nz):
            for atom in ucell:
                x = ix+atom.x
                y = iy+atom.y
                z = iz+atom.z
                scell.append(Atom(atom.symbol,[x,y,z]))

#transform from fractional to cartesion
#for atom in scell:
#    x = atom.x * latt_vec[0][0]
#    y = atom.y * latt_vec[1][1]
#    z = atom.z * latt_vec[2][2]
#    atom.x = x
#    atom.y = y
#    atom.z = z
    
#output the atoms in xyz format
print len(scell)
print latt_vec[0][0]*nx, latt_vec[1][1]*ny, latt_vec[2][2]*nz, "Cubic,lattice vectors"
for atom in scell:
    print atom

