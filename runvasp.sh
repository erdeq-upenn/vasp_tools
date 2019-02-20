NPROCS=`wc -l < $PBS_NODEFILE`

ulimit -s unlimited
#ulimit -l unlimited
#echo "t">t.test
MPIRUN="mpirun -np $NPROCS -machinefile $PBS_NODEFILE --mca btl sm,self"

#VASP="/home/junwenli/software/vasp/vasp.5.3/vasp"
VASP="/opt/pkg/vasp/5.3-icc/vasp"

$MPIRUN $VASP > vasp.out.$1
cp OUTCAR OUTCAR.$1
cp CONTCAR CONTCAR.$1
