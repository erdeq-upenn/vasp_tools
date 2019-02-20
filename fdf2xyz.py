#!/usr/bin/env python
# 
import sys
import math
from math import *
import re


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


reo_xyz = re.compile(r'\s*(?P<x>-?\d+.?\d+e?-?\d+)\s*' +\
                         r'(?P<y>-?\d+.?\d+e?-?\d+)\s*' +\
                         r'(?P<z>-?\d+.?\d+e?-?\d+)\s*' +\
                         r'\d+\s*\d+\s*(?P<atom>[a-z,A-Z]+)\s*', re.I)

reo_atomiccoord = \
    re.compile(r'%block AtomicCoordinatesAndAtomicSpecies\s*', re.I)


reo_outcell = re.compile(r'%block LatticeVectors\s*', re.I)
reo_vxyz = re.compile(r'\s*(?P<x>-?\d+.?\d+e?-?\d+)\s*' +\
                          r'(?P<y>-?\d+.?\d+e?-?\d+)\s*' +\
                          r'(?P<z>-?\d+.?\d+e?-?\d+)\s*', re.I)


_debug_ = True


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


class Fdf2xyz:
    def __init__(self, lines):
        self.lines = lines
        self.nline = 0

        self.AtomsRelax = []
        self.OutCell = []
        self.AtomsSuperCell = []

        while self.nline < len(lines):
            self.ParseAtomicCoord()
            self.ParseOutcell()
            self.nextlines()   
             
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

        
    def ParseAtomicCoord(self):
        bmatch = reo_atomiccoord.match(self.currentline())
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
        for i in range(ncell):
            zshift = self.OutCell[2][2]*i
            for atom in self.AtomsRelax:
                x,y,z = atom.x*self.OutCell[0][0], \
			atom.y*self.OutCell[1][1], \
			atom.z*self.OutCell[2][2]+zshift	
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
        print "lattice vector (x,y,z) : %20.16f\t%20.16f\t%20.16f" % \
            (self.OutCell[0][0], self.OutCell[1][1], self.OutCell[2][2])

        for atom in atoms:
            print atom

    def OutputFdf(self,atoms):
        species = {'c':1, 'h':2, 'o':3}
        for atom in atoms:
            print "%16.12f\t%16.12f\t%16.12f\t%d\t%s\t" % \
                (atom.x, atom.y, atom.z, species[atom.symbol], atom.symbol)

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
    siesta = Fdf2xyz(lines)
    siesta.MakeSuperCell(ncell)
    siesta.OutputSuperCell(format)
if __name__ == '__main__':
    main()
