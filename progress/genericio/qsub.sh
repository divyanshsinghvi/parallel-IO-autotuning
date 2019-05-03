#! /bin/bash
#PBS -q courses
#PBS -l walltime=00:30:00 
#merge output and error into a single job_name.number_of_job_in_queue.
#PBS -j oe
#export fabric infiniband related variables
export I_MPI_FABRICS=shm:tmi:tcp
export I_MPI_DEVICE=rdma:OpenIB-cma
#change directory to where the job has been submitted from
cd $PBS_O_WORKDIR
#source paths
source /opt/software/intel/initpaths intel64

echo $PBS_NODEFILE
#sort hostnames
sort $PBS_NODEFILE > hostfile
#run the job on required number of cores
#mpirun -machinefile hostfile ./mpi/GenericIOBenchmarkWrite output/out.gio $commnd
echo $path
echo $commnd
#export MPICH_MPIIO_HINTS=$mpihints
mpirun -machinefile hostfile -env ROMIO_HINTS=$romhint $path output/out.gio $commnd
echo $PBS_JOBID
echo $PBS_JOBNAME

