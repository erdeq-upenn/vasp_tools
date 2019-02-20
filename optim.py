#!/usr/bin/env python
# Supercell generator 1.0
#
# 05/18/2010
#
#
import sys
import math
from math import *
import re

reo_xyz = \
    re.compile(r'\s*(?P<x>-?\d+.?\d+e?-?\d+)\s*(?P<y>-?\d+.?\d+e?-?\d+)\s*(?P<z>-?\d+.?\d+e?-?\d+)\s*\d+\s*\d+\s*(?P<atom>[a-z,A-z]+)\s*', re.I)

reo_outcell = re.compile(r'outcell: Unit cell vectors \(Ang\):\s*', re.I)

reo_vxyz = re.compile(r'\s*(?P<x>-?\d+.?\d+e?-?\d+)\s*' +\
                          r'(?P<y>-?\d+.?\d+e?-?\d+)\s*' +\
                          r'(?P<z>-?\d+.?\d+e?-?\d+)\s*', re.I)

reo_outcoor = re.compile(r'outcoor: Relaxed atomic coordinates \(Ang\):\s*', re.I)

class Atom:
    def __init__(self, symbol, x=0.0,y=0.0,z=0.0):
        self.symbol = symbol
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        line = ('%s\t%16.12f\t%16.12f\t%16.12f') \
               % (self.symbol, self.x, self.y, self.z)
        return line

class optim:
    def __init__(self, lines):
        self.atoms = []
        self.latt = []

        self.nline = 0
        while self.nline < len(lines):
            self.parsevectors(lines)
            self.parsexyz(lines)
            self.nline = self.nline + 1
    

    def parsexyz(self, lines):
        bmatch = reo_outcoor.match(lines[self.nline])
        if not bmatch:
            return
        while self.nline < len(lines):            
            self.nline = self.nline + 1   
            line = lines[self.nline]
            bmatch = reo_xyz.match(line)
            if bmatch:
                grp = bmatch.groupdict()
                x,y,z,sym = float(grp['x']),\
                    float(grp['y']),\
                    float(grp['z']),\
                    grp['atom']
                self.atoms.append(Atom(sym,x,y,z))
            else:
                print line
                break

    def parsevectors(self, lines):
        bmatch = reo_outcell.match(lines[self.nline])
        if not bmatch:
            return
        self.latt = []
        for i in range(3):
            self.nline = self.nline + 1
            line = lines[self.nline]
            bmatch = reo_vxyz.match(line)
            grp = bmatch.groupdict()
            x,y,z = float(grp['x']), float(grp['y']), float(grp['z'])
            self.latt.append([x,y,z])
                      
    def makesc(self,ncell):
        ucell = self.atoms
        natoms = len(ucell)
        for n in range(1,ncell):
            for m in range(natoms):
                atom = ucell[m]
                x = atom.x + self.latt[0][0]*n
                y = atom.y
                z = atom.z #+ self.latt[2][2]*n
                self.atoms.append(Atom(atom.symbol,x,y,z))

    def print_xsf(self):
        print "ATOMS"
        for atom in self.atoms:
            print atom
    
def main():
    filename = sys.argv[1]
    ncell = int(sys.argv[2])
    file = open(filename, 'r')
    lines = file.readlines()
    ucell = optim(lines)
    ucell.makesc(ncell)
    ucell.print_xsf()
    
if __name__ == '__main__':
    main()
