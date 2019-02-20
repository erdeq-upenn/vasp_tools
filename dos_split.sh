#!/bin/bash
#LORBIT=10,ISTART=1,ICHARG=11
#DOS=$0
DOS=DOSCAR
nions=`head -n 1 $DOS | awk '{print $1}'`
nes=`head -n 6 $DOS | tail -n 1 | awk '{print $3}'`
efermi=`head -n 6 $DOS | tail -n 1 | awk '{print $4}'`

head -n `expr $nes + 6` $DOS | tail -n $nes > dos_tot.dat

for ((i=1;i<=$nions;i++))
do

nstart=`expr $nes + 1`
j=`expr $i + 1`
nstart=`expr $nstart \* $j`
nstart=`expr $nstart + 5`
head -n $nstart $DOS | tail -n $nes > dos_$i.dat
done

