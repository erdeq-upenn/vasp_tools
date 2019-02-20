# w is the second argv, POSCAR or CONTCAR is the 1 agv
import sys
import math

def get_latt_para(lines):
    vec = []
    for v in lines[1].split():
        vec.append(float(v))
    return vec
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
#def get_coo(lines,i):
#    vec = []
#    for v in lines[i].split():
#        vec.append(float(v))
#    return vec

def readlines(filename):
    f = open(filename)
    lines = f.readlines()
    f.close()
    return lines
def norm_vec(v):
	norm = math.sqrt(float(v[0]**2+v[1]**2+v[2]**2))
	return norm

def print_vec(v):
    print "%20.16f\t\t%20.16f\t\t%20.16f"% (v[0],v[1],v[2])
def print_vec2(v,x,y):
    print "%20.16f%20.16f%20.16f"% ((v[0]+w*x),(v[1]+w*y),v[2])

lines = readlines(sys.argv[1])
#print lines[0][0:-1]
para = get_latt_para(lines)
#print type(para)
#w=float(sys.argv[2])
a = get_latt_a(lines)
b = get_latt_b(lines)
c = get_latt_c(lines)
norm_of_a = norm_vec(a)
lp_a = norm_of_a*para[0]
print 'lattice parameter, a='+str(lp_a)
#print_vec(norm_of_a)
#print_vec(b)
#print_vec(c)
#x=float(sys.argv[2])
#y=float(sys.argv[3])
#print "*"*80
#print "*"*80

#for idle in range(5,len(lines)):
#		if idle in range(5,8):
#				print lines[idle][0:-1]
#		else:
#				if idle==11:
#						coo=get_coo(lines,idle)
#						print_vec2(coo[:],x,y)
#				elif idle==12:
#						coo=get_coo(lines,idle)
#						print_vec2(coo[:],x,y)
#				elif idle==13:
#						coo=get_coo(lines,idle)
#						print_vec2(coo[:],x,y)
#				else:	
#						print lines[idle][0:-1]
