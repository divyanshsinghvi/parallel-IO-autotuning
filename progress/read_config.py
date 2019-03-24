import json
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

os.chdir('S3D-IO')
subprocess.Popen(["./run.sh", mpi_hints], shell=True)



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
        command+= " -c " + d['count']
    print command
    subprocess.Popen([command], shell=True)
#pprint(data)

