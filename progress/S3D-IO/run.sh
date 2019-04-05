#!/bin/bash

# remove data files

# declare arrays 
nodes=(2 )
# prefix of all jobs for this question
jobPrefix="q1"
echo "I am in bash script "
echo $1
 for node in ${nodes[*]}
 do
    echo "No of nodes - ${node}"
    # assign name of job
    jobName="${jobPrefix}_${node}"
    echo ${jobName}
    
    export mpihints=$1
    export commnd="100 100 200 2 2 4 1"
    # run the job
    output=$(qsub -N ${jobName} -l nodes=${node}:ppn=8 -v mpihints -v commnd qsub.sh)

    # extract id of job
    id=$( echo $output  | cut -d '.' -f 1)
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
    rm  output/*
done

