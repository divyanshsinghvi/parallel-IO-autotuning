#!/bin/bash

# remove data files

# declare arrays 
nodes=(1 2 4 8 16)
# prefix of all jobs for this question
jobPrefix="q1"

 for node in ${nodes[*]}
 do
    echo "No of nodes - ${node}"
    # assign name of job
    jobName="${jobPrefix}_${node}"
    echo ${jobName}

    # run the job
    output=$(qsub -N ${jobName} -l nodes=${node}:ppn=1 run.sh)

    # extract id of job
    id=$( echo $output  | cut -d '.' -f 1)
    outfile=${jobName}.o${id}
    echo "Waiting for formation of file"
    
    # wait for the job to be executed and file to be created
    while [ ! -f "$outfile" ]
    do
      continue
    done

    # append data to data file for plots
    echo "${outfile} finished"
    echo ${cat $outfile}
done

