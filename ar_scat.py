#!/usr/bin/env python
# 
import sys
import math
from math import *
import re

reo_xyz = re.compile(r'\s*(?P<x>-?\d+.?\d+e?-?\d+)\s*' +\
                         r'(?P<y>-?\d+.?\d+e?-?\d+)\s*' +\
                         r'(?P<z>-?\d+.?\d+e?-?\d+)\s*' +\
                         r'\d+\s*\d+\s*(?P<atom>[a-z,A-Z]+)\s*', re.I)

reo_outcoor_fractional = \
    re.compile(r'outcoor: Relaxed atomic coordinates \(fractional\):\s*', re.I)

reo_outcoor_ang = \
    re.compile(r'outcoor: Relaxed atomic coordinates \(Ang\):\s*', re.I)

reo_outcell = re.compile(r'outcell: Unit cell vectors \(Ang\):\s*', re.I)
reo_vxyz = re.compile(r'\s*(?P<x>-?\d+.?\d+e?-?\d+)\s*' +\
                          r'(?P<y>-?\d+.?\d+e?-?\d+)\s*' +\
                          r'(?P<z>-?\d+.?\d+e?-?\d+)\s*', re.I)


_debug_ = False


AtomSymbol = [ 'x','h','he','li','be','b','c','n','o','f','ne', \
     'na','mg','al','si','p','s','cl','ar','k','ca','sc','ti', \
     'v','cr','mn','fe','co','ni','cu','zn','ga','ge','as','se', \
     'br','kr','rb','sr','y','zr','nb','mo','tc','ru','rh','pd', \
     'ag','cd','in','sn','sb','te','i','xe','cs','ba','la','ce', \
     'pr','nd','pm','sm','eu','gd','tb','dy','ho','er','tm','yb', \
     'lu','hf','ta','w ','re','os','ir','pt','au','hg','tl','pb', \
     'bi','po','at','fr','rn','ra','ac','th','pa','u','np','pu', \
     'am','cm','bk','cf','es','fm','md','no','lr' ]

AtomName = [ 'dummy','hydrogen','helium','lithium','beryllium',           \
             'boron','carbon','nitrogen','oxygen','fluorine','neon',      \
             'sodium','magnesium','aluminum','silicon','phosphorus',      \
             'sulfur','chlorine','argon', \
             'potassium','calcium','scandium','titanium','vanadium',      \
             'chromium','manganese','iron','cobalt','nickel',             \
             'copper','zinc','gallium','germanium','arsenic',             \
             'selenium','bromine','krypton', \
             'rubidium','strontium','yttrium','zirconium','niobium',      \
             'molybdenum','technetium','ruthenium','rhodium',             \
             'palladium','silver','cadmium','indium','tin',               \
             'antimony','tellurium','iodine','xenon', \
             'cesium','barium','lanthanum','cerium','praseodymium',       \
             'neodymium','polonium','samarium','europium','gadolinium',   \
             'terbium','dysprosium','holmium','erbium','thulium',         \
             'ytterbium','lutetium','hafnium','tantalum','tungsten',      \
             'rhenium','osmium','iridium','platinum','gold','mercury',    \
             'thallium','lead','bismuth','polonium','astatine','radon', \
             'francium','radium','actinium','thorium','protoactinium',    \
             'uranium','neptunium','plutonium','americium','curium',      \
             'berkelium','californium','einsteinium','fermium',           \
             'mendelevium','nobelium','lawrencium' ]

class Atom:
    def __init__(self, symbol, x,y,z):
        sym = symbol
        if (isinstance(sym,str)):
            sym = sym.lower()
            self.symbol = sym
            self.no = AtomSymbol.index(sym)
        elif (isinstance(sym,int)):
            self.symbol = AtomSymbol[sym]
            self.no = sym
        else:
            print "Wrong arguments"
        
        self.x = x
        self.y = y
        self.z = z
        
        self.formatstr = '%s\t%16.12f\t%16.12f\t%16.12f'

    def __str__(self):
        line = (self.formatstr) \
            % (self.symbol, self.x,self.y, self.z)
        return line    

class Relax:
    def __init__(self, lines):
        self.lines = lines
        self.nline = 0
        
        self.AtomsRelax = []
        self.OutCell = []
        self.AtomsSuperCell = []
        
        while self.nline < len(lines):
            self.ParseOutcoor()
            self.ParseOutcell()
            self.nextlines()   

        self.npos = len(self.AtomsRelax)*5

    def addcarbonyl(self,n1,n2):
        c1 = self.AtomsSuperCell[n1-1]
        c2 = self.AtomsSuperCell[n2-1]        
        pp = 0.75
        a1 = Atom("O",c1.x+pp*(c2.x-c1.x), \
                      c1.y+1.20,\
                      c1.z+pp*(c2.z-c1.z))
        a2 = Atom("O",c2.x+pp*(c1.x-c2.x), \
                      c2.y-1.20,\
                      c2.z+pp*(c1.z-c2.z))
	c1.y = c1.y + 0.6
	c2.y = c2.y - 0.6
        self.AtomsSuperCell.insert(self.npos, a1)
        self.AtomsSuperCell.insert(self.npos, a2)
        
    def adddefects(self,posfil):
        file = open(posfil,'r')
        lines = file.readlines()
        for line in lines:
            sline = line.split()
            if (len(sline) < 2):
                continue
            n1 = int(sline[0])
            n2 = int(sline[1])

            self.addcarbonyl(n1,n2)

             
    def ParseOutcell(self):
        bmatch = reo_outcell.match(self.currentline())
        if not bmatch:
            return
        self.OutCell = []
        while self.nline < len(self.lines):
            self.nextlines()
            bmatch = reo_vxyz.match(self.currentline())
            if bmatch:
                grp = bmatch.groupdict()
                x,y,z = \
                    float(grp['x']), \
                    float(grp['y']), \
                    float(grp['z'])
                self.OutCell.append([x,y,z])
            else:
                break
            
        if _debug_:
            print "Outcell"
            print self.OutCell

        
    def ParseOutcoor(self):
        bmatch = reo_outcoor_ang.match(self.currentline())
        if not bmatch:
            return

        while self.nline < len(self.lines):
            self.nextlines()
            bmatch = reo_xyz.match(self.currentline())
            if bmatch:
                grp = bmatch.groupdict()
                x,y,z,symbol = \
                    float(grp['x']), \
                    float(grp['y']), \
                    float(grp['z']), \
                    grp['atom']
                self.AtomsRelax.append(Atom(symbol,x,y,z))
            else:
                break
    

    def currentline(self):
        return self.lines[self.nline]

    def nextlines(self, n=1):
        self.nline = self.nline + n

    def MakeSuperCell(self, ncell):
        self.ncell = ncell
        for i in range(ncell):
            zshift = self.OutCell[2][2]*i
            for atom in self.AtomsRelax:
                x,y,z = atom.x,atom.y,atom.z+zshift
                self.AtomsSuperCell.append(Atom(atom.symbol,x,y,z))
        
    def GetAtomsSuperCell(self):
        return self.AtomsSuperCell        

    def GetAtomsRelax(self):
        return self.AtomsRelax

    def OutputXsf(self,atoms):
        print "ATOMS"
        for atom in atoms:
            print atom
    
    def OutputXyz(self,atoms):
        print len(atoms)
        print "relaxed structure"
        for atom in atoms:
            print atom

    def OutputFdf(self,atoms):
        species = {'c':1, 'h':2, 'o':3}
        print "NumberOfAtoms    ", len(atoms)
        print "NumberOfSpecies  ", len(species)
        print "%block ChemicalSpeciesLabel"
        print "1    6    C"
        print "2    1    H"
        print "3    8    O"
        print "%endblock ChemicalSpeciesLabel"
        print "LatticeConstant   1.0 Ang"
        print "%block LatticeVectors"
        print "%16.12f\t%16.12f\t%16.12f" % \
            (self.OutCell[0][0], self.OutCell[0][1], self.OutCell[0][2])
        print "%16.12f\t%16.12f\t%16.12f" % \
            (self.OutCell[1][0], self.OutCell[1][1]+5.0, self.OutCell[1][2])
        print "%16.12f\t%16.12f\t%16.12f" % \
            (self.OutCell[2][0], self.OutCell[2][1], self.OutCell[2][2]*self.ncell)
        print "%endblock LatticeVectors"
        print "AtomicCoordinatesFormat Ang"
        print "%block AtomicCoordinatesAndAtomicSpecies"
        for atom in atoms:
            print "%16.12f\t%16.12f\t%16.12f\t%d\t%s\t" % \
                (atom.x, atom.y, atom.z, species[atom.symbol], atom.symbol)
        print "%endblock AtomicCoordinatesAndAtomicSpecies"

    def OutputSuperCell(self,format='xsf'):
        lformat = format.lower()
        if 'xsf' == lformat:
            self.OutputXsf(self.AtomsSuperCell)
        elif 'xyz' == lformat:
            self.OutputXyz(self.AtomsSuperCell)        
        elif 'fdf' == lformat:
            self.OutputFdf(self.AtomsSuperCell)
            
    def OutputAtomsRelax(self,format='xsf'):
        lformat = format.lower()
        if 'xsf' == lformat:
            self.OutputXsf(self.AtomsRelax)
        elif 'xyz' == lformat:
            self.OutputXyz(self.AtomsRelax)
        elif 'fdf' == lformat:
            self.OutputFdf(self.AtomsRelax)

def main():
    filename = sys.argv[1]
    ncell = int(sys.argv[2])
    format = sys.argv[3]
    file = open(filename, 'r')
    lines = file.readlines()
    siesta = Relax(lines)
    siesta.MakeSuperCell(ncell)
    siesta.adddefects("O.pos")
    siesta.OutputSuperCell(format)
if __name__ == '__main__':
    main()
