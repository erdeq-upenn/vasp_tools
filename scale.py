import sys

def readlines(filename):
    f = open(filename)
    lines = f.readlines()
    f.close()
    return lines

def get_latt_const(lines):
    return float(lines[1])

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

def scale(vec,a):
    for n in range(len(vec)):
        vec[n] = vec[n] * a

def print_vec(v):
    print "   %20.16f%20.16f%20.16f" % (v[0],v[1],v[2])

lines = readlines(sys.argv[1])
print lines[0][0:-1]
print "  1.00"
latt_const = get_latt_const(lines)
a = get_latt_a(lines)
b = get_latt_b(lines)
c = get_latt_c(lines)

scale(a,latt_const)
scale(b,latt_const)
scale(c,latt_const)

print_vec(a)
print_vec(b)
print_vec(c)

for line in lines[5:]:
    print line[0:-1]
        
