import json
import shlex
import subprocess
import logging
from pprint import pprint
import re
import os

logging.basicConfig(level=logging.DEBUG)
#logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

with open('confex.json') as f:
    data = json.load(f)


os.chdir('./S3D-IO')
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
    #print(str(command))
    #logging.debug("Lustre parameters:"+ command)
    os.chdir('./output')
    subprocess.Popen(shlex.split(str(command)), shell=False)

mpi_hints=""
os.chdir('../')
for key in data["mpi"]:
    mpi_hints+=key
    mpi_hints+="="+data["mpi"][key]+";"


#logging.debug("MPI parameters:" + mpi_hints)
specific_commands="50 50 100 2 2 4 1"
log = open('../stats.txt','a')
out=subprocess.Popen(["./run.sh", mpi_hints,specific_commands], shell=False, stdout=subprocess.PIPE)
output=out.stdout.read()
#logging.debug(output.decode('utf-8'))
readB=re.findall("read  bandwidth\s*:\s*([0-9]+\.[0-9]+)",output.decode('utf-8'))
	#print(readB)
writeB=re.findall("write bandwidth\s*:\s*([0-9]+\.[0-9]+)",output.decode('utf-8'))
print("S3D-IO",end = " ")
print(specific_commands, end = " ")

for hints in data["lfs"]["setstripe"]:
        print(data["lfs"]["setstripe"][hints],end=" ")
    
print("{0} {1} ".format(readB[0], writeB[0]), end = "")

hints_array=mpi_hints.split(";")
for hints in hints_array:
    if(len(hints.split('=')) == 2): 
        print(hints.split("=")[1],end=" ")

