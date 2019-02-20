import sys
import math
#this function will convert ratio to cartisen coordinate
#get a_b_c lattic vectors
def get_latt_a(lines):
	vec=[]
	for v in lines[2].split():
		vec.append(float(v))
	return vec
def get_latt_b(lines):
	vec=[]
	for v in lines[3].split():
		vec.append(float(v))
	return vec
def get_latt_c(lines):
	vec=[]
	for v in lines[4].split():
		vec.append(float(v))
	return vec
def get_vec(lines,i):
	vec=[]
	for v in lines[i].split():
		vec.append(float(v))
	return vec
def ratioToCar(vec,a,b,c):
	car=[]
	for k in range(0,3):
			car.append(float(vec[0]*a[k]+vec[1]*b[k]+vec[2]*c[k]))
	return car 
def print_vec(v):
	print "%20.16f\t%20.16f\t%20.16f"% (v[0],v[1],v[2])
def tot_atoms(lines):
	vec=[]
	for v in lines[6].split():
			vec.append(float(v))
	return int(sum(vec))
#finish defining a,b,c
#define readlines
def readlines(filename):
	f=open(filename)
	lines=f.readlines()
	f.close()
	return lines
#finish readlines
#convert to vectors
#finish saving to vectors
#define convert ratio to cartisen
#####################################
lines = readlines(sys.argv[1])
a=get_latt_a(lines)
b=get_latt_b(lines)
c=get_latt_c(lines)
#w=get_vec(lines,8)
#ok=ratioToCar(w,a,b,c)
#print ok
#print w
for line in lines[0:8]:
		print line[0:-1]
w=tot_atoms(lines)+8
for i in range(8,len(lines)):
		if i<w:
			line=get_vec(lines,i)
			Car=ratioToCar(line,a,b,c)
			print_vec(Car)
			Car=[]
