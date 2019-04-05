import json
import shlex
import subprocess
from pprint import pprint
import os

with open('confex.json') as f:
    data = json.load(f)


mpi_hints=""

for key in data["mpi"]:
    mpi_hints+=key
    mpi_hints+="="+data["mpi"][key]+";"


print(mpi_hints)
os.chdir('./S3D-IO')
subprocess.Popen(["./run.sh", mpi_hints], shell=False)



for key in data["lfs"]:
    command = "lfs " + key + "  "
    d =  data["lfs"][key]
    if 'filename' in d:
        command += d['filename']
    else: 
	command += "."
    if 'size' in d:
        command+= " -s " + d['size']
    if 'count' in d:
        command+= " -c " + str(d['count'])
    print(command)
    os.chdir('./output')
    print(os.getcwd())
    subprocess.Popen(shlex.split(command), shell=False)
#pprint(data)

