import graph;
real fermi = -1.5907;
int ne = 0;
int nup = 1;
int ndn = 2;
size(600,300);
file filename = input("dos_tot.dat").line();
real[][] A = filename.dimension(0,0);
A = transpose(A);
real[] x = A[ne]-fermi;
real[] yu = A[nup];
real[] yd = -A[ndn];

picture pup, pdn;
guide g;
//spin up
g = graph(pup,x,yu);
filldraw(pup, g--cycle,red);
draw(pup,g,red,Label("Spin $\uparrow$ TDOS"));
//legend
add(pup,legend(pup), point(pup,NW), SE, UnFill);

add(pup);

//spin down
g = graph(pdn,x,yd);
filldraw(pdn,g--cycle,blue);
draw(pdn,g,blue,Label("Spin $\downarrow$ TDOS"));
//legend
add(pdn,legend(pdn), point(pdn,SW), NE, UnFill);

add(pdn);



//fermi level
//draw((0,min(yd))--(0,max(yu)),cyan);
xequals(0,cyan+Dotted);

xaxis("Energy (eV)", BottomTop, LeftTicks(Step=2));
yaxis("Density of States (arb. units)", LeftRight, RightTicks(Step=2));
