# Script to batch submit many jobs to a PBS cluster.
#
# Submits NREPLICATES replicate jobs for each brancing probability PROBS

# Submits NREPLICATES jobs
NREPLICATES=400 #Number of per probability replicates
STEPS=200 #Number of steps the simulation will take (>= 1)
PROBS=(20 25 30 35 40) # Branching probability * 100 (0 <= $prob <= 100)
FILE_PREFIX="06132018" # Output filename FILE_PREFIX

for i in $(seq 1 $NREPLICATES); do
  for prob in ${PROBS[*]}; do
    FNAME="$FILE_PREFIX"_"$prob"_"$STEPS"_"$i"
    qsub -v file_prefix=$FNAME,p=$prob,steps=$STEPS submit
  done
done
