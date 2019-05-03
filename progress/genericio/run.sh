#!/bin/bash

# remove data files
# declare arrays
echo "Format is <nodes> <ppn <mpihint> <read=0/write=1> <if write rows seed>"
nodes=($1)
# prefix of all jobs for this question
jobPrefix="Generic-IO"
for node in ${nodes[*]}
do
   echo "No of nodes - ${node}"
   # assign name of job
   jobName="${jobPrefix}_${node}"
   echo ${jobName}
   z=$3
   bar=${z//;/:}
   export mpihints="*:"$bar"cb_nodes=2"
   echo "*:"$bar"cb_nodes=2"
   export commnd=$5
   export write=$4
   # run the job
   echo ${node}, $2, $write
   if [ "$write" -eq 0 ]; then
       export path="./mpi/GenericIOBenchmarkRead"
       export commnd=""
       output=$(qsub -N ${jobName} -l nodes=${node}:ppn=$2 -v mpihints -v path -v commnd qsub.sh)
   else
       export path="./mpi/GenericIOBenchmarkWrite"
       output=$(qsub -N ${jobName} -l nodes=${node}:ppn=$2 -v mpihints -v path -v commnd qsub.sh)
       
   fi
   # extract id of job
   id=$( echo $output  | awk -F. '{print $1}')
   outfile=${jobName}.o${id}
   echo "Running the job"
   while [ ! -f "$outfile" ]
   do 
	continue
   done
   # append data to data file for plots
   echo "${outfile} finished" 
   out=$(cat $outfile)
   echo "$out"
   rm "$outfile"
done
