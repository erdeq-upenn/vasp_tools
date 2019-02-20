#!/bin/bash
# s - 0, p - 1, d - 2, f - 3
#
DOS=DOSCAR
#$l=0
#ltitle="$l" + "u"
nions=`head -n 1 $DOS | awk '{print $1}'`
nes=`head -n 6 $DOS | tail -n 1 | awk '{print $3}'`
efermi=`head -n 6 $DOS | tail -n 1 | awk '{print $4}'`

ncolu=`expr 1 + $2 \* 2 + 1`
ncold=`expr $ncolu + 1`





cat > dos_plot.cmd <<EOF
set term postscript enhanced color
set output "dos_$1_$2.eps"
plot "dos_$1.dat" using 1:$ncolu with lines title "spin up, l = $2, site = $1", \\
"dos_$1.dat" using 1:(-\$$ncold) with lines title "spin down, l = $2, site = $1"
EOF

gnuplot < dos_plot.cmd

