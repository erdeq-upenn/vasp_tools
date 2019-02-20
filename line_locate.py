#!/usr/bin/env python
import sys

fil = open(sys.argv[2])
str_wanted = sys.argv[1]

lines = fil.readlines()

nline = -1

for n in range(len(lines)):
    if str_wanted in lines[n]:
	nline = n

print nline
