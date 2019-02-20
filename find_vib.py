#!/usr/bin/env python
# 
import sys
import math
from string import *
from math import *
import re

#eV/K
#Kb = 8.617332E-5 
#meV/K
Kb = 8.617332E-2

def match_vib(line):
    if ( find(line, "2PiTHz") > 0 ):
	sl = line.split()
	if (sl[1] == "f"):	
	    print line
	    return float(sl[9]) 
    else:
        return -1.0

def sum(xs):
    s = 0
    for x in xs:
        s = s + x
    return s

def get_u(hw,T):
    x = exp(-1.0*hw/Kb/T)
    return hw*x/(1.0-x)

def get_ts(hw,T):
    x = exp(-1.0*hw/Kb/T)
    return -Kb*T*log(1.0-x) + hw*x/(1.0-x)
    
T = 298.15

f = open(sys.argv[1])
lines = f.readlines()
f.close()

zpe = []
u = []
ts = []
for line in lines:
    z0 = match_vib(line)
    if ( z0 > 0):
        zpe.append(z0)
        u.append(get_u(z0,T))
        ts.append(get_ts(z0,T))

print zpe
print "(meV) zpe = ", sum(zpe)/2, " U = ", sum(u), " ts = ", sum(ts)

