# w is the second argv, POSCAR or CONTCAR is the 1 agv
import sys
import random
def get_latt_a(lines):
    vec = []
    for v in lines[2].split():
        vec.append(float(v))
    return vec

def get_latt_b(lines):
    vec = []
    for v in lines[3].split():
        vec.append(float(v))
    return vec

def get_latt_c(lines):
    vec = []
    for v in lines[4].split():
        vec.append(float(v))
    return vec
def get_coo(lines,i):
    vec = []
    for v in lines[i].split():
        vec.append(float(v))
    return vec

def get_int(lines,i):
    vec = []
    for v in lines[i].split():
        vec.append(int(v))
    return vec

def readlines(filename):
    f = open(filename)
    lines = f.readlines()
    f.close()
    return lines
def random_vec(a,b,c):
	vran=[random.uniform(0,a),random.uniform(0,b), random.uniform(-c/2+1,c/2+1)]
	return vran

def print_vec(v):
    print "%20.16f\t\t%20.16f\t\t%20.16f"% (v[0],v[1],v[2])
def print_int(v):
    print "  %d  %d"% (v[0],nadatom)

lines = readlines(sys.argv[1])
nadatom=int(sys.argv [2])
print lines[0][0:-2]
print 1.0000000000000000
#w=float(sys.argv[2])
a = get_latt_a(lines)
b = get_latt_b(lines)
c = get_latt_c(lines)
#c2=c[2]
#d=[c[0],c[1],(c[2]+w)]
#print_vec(a)
#print_vec(b)
#print_vec(c)
for idle in range(2,6):
	print lines[idle][0:-2]
NN=get_int(lines,6)
print_int(NN)
NC=NN[0]
NN[1]=nadatom
print lines[7][0:-2]
#__________________________________
vran=random_vec(a[0],b[1],2)
#_________________________________
#for idle in range(8,NC+8):
#	print lines[idle][0:-1]
for idle in range(8,NC+8):
	coo=get_coo(lines,idle)
	print_vec(coo)	
for idle in range(0,nadatom):
	vran=random_vec(a[0],b[1],2)
	print_vec(vran)

