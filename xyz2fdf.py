import sys

class Atom:
    def __init__(self,symbol,x,y,z):
        self.symbol = symbol
        self.x = x
        self.y = y
        self.z = z

f = open(sys.argv[1])
lines = f.readlines()
f.close()

latt_vec = [[0,0,0],[0,0,0],[0,0,0]]
latt_scale = 1.0

#lattice vectors
line = lines[1]
sline = line.split()
latt_vec[0][0] = float(sline[0])
latt_vec[1][1] = float(sline[1])
latt_vec[2][2] = float(sline[2])

atoms = []
for n in range(2,len(lines)):
    line = lines[n]
    sline = line.split()
    symbol = sline[0].strip()
    if (symbol == "#"):
	continue
    
    x,y,z = float(sline[1]), float(sline[2]), float(sline[3])
    atoms.append(Atom(symbol,x,y,z))
    

print "NumberOfAtoms    ", len(atoms)
print "NumberOfSpecies  ", 4
print "%block ChemicalSpeciesLabel"
print " 1 29 Cu"
print " 2 50 Sn"
print " 3 30 Zn"
print " 4 34 Se"
print "%endblock ChemicalSpeciesLabel"
print "LatticeConstant  1.0 Ang"
print "%block LatticeVectors"
print "    %20.16f  %20.16f  %20.16f" % (latt_vec[0][0], latt_vec[0][1], latt_vec[0][2])
print "    %20.16f  %20.16f  %20.16f" % (latt_vec[1][0], latt_vec[1][1], latt_vec[1][2])
print "    %20.16f  %20.16f  %20.16f" % (latt_vec[2][0], latt_vec[2][1], latt_vec[2][2])
print "%endblock LatticeVectors"
print "AtomicCoordinatesFormat Ang"


print "%block AtomicCoordinatesAndAtomicSpecies"


for atom in atoms:
    index = 1
    if atom.symbol == "Cu":
        index = 1
    if atom.symbol == "Sn":
        index = 2
    if atom.symbol == "Zn":
        index = 3
    if atom.symbol == "Se":
        index = 4
    line = ('%16.12f\t%16.12f\t%16.12f\t%d\t%s') \
        % (atom.x,atom.y,atom.z,index,atom.symbol)
    print line


print "%endblock AtomicCoordinatesAndAtomicSpecies"

        
