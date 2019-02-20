import sys
import os

if not os.path.exists(sys.argv[1]):
    exit()

f = open(sys.argv[1])

lines = f.readlines()
f.close()

toten_lines = ""
nline = 0
for i in range(len(lines)):
    if (lines[i].find("E-fermi") > 0):
     	nline = i
toten_lines = lines[nline]
#print nline
#print toten_lines
sline = toten_lines.split()
#print sline

#a = sys.argv[2]

print sline[2]

