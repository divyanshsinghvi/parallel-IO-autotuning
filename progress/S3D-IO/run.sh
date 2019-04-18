#!/bin/bash

# remove data files
# declare arrays 
nodes=($1)
# prefix of all jobs for this question
jobPrefix="S3D-IO"
for node in ${nodes[*]}
do
   echo "No of nodes - ${node}"
   # assign name of job
   jobName="${jobPrefix}_${node}"
   echo ${jobName}
   
   export mpihints=$3
   export commnd=$4
   # run the job
   echo ${node}, $2
   output=$(qsub -N ${jobName} -l nodes=${node}:ppn=$2 -v mpihints -v commnd qsub.sh)
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

