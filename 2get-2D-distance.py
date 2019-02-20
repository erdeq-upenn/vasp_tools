import sys
import math
#define the function that gives the distance
#between two vectors (a,b)
###############################################################
def dist(v1,v2):
	distance=(v1[0]-v2[0])**2+(v1[1]-v2[1])**2+(v1[2]-v2[2])**2
	distance=math.sqrt(distance)
	return distance
#distance between I and J
def distIndex(i,j):
	v1=get_vec(lines,i)
	v2=get_vec(lines,j)
	distij=dist(v1,v2)
	return distij
###############################################################
#read the files into data
def readlines(filename):
	f=open(filename)
	lines=f.readlines()
	f.close()	
	return lines
################################################################	
#convert to vectors
def get_vec(lines,i):
	vec=[]
	for v in lines[i].split()[0:3]:
		vec.append(float(v))
	return vec	
#################################################
#finish definition
##    main    ##    
#   readlines
lines = readlines(sys.argv[1])
# finish read lines
##Index=
#for i in range(8,len(lines)-1):
#	distance=distIndex(i,i+1)
#	print i,'Distance between',i,'and',i+1,'is',distance
index1=int(sys.argv[2])
index2=int(sys.argv[3])
distance=distIndex(index1,index2)
print distance
