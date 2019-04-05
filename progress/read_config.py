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
    print(str(command))
    #logging.debug("Lustre parameters:"+ command)
    os.chdir('./output')
    subprocess.Popen(shlex.split(str(command)), shell=False)

mpi_hints=""
os.chdir('../')
for key in data["mpi"]:
    mpi_hints+=key
    mpi_hints+="="+data["mpi"][key]+";"


logging.debug("MPI parameters:" + mpi_hints)
log = open('../stats.txt','a')
out=subprocess.Popen(["./run.sh", mpi_hints], shell=False, stdout=subprocess.PIPE)
output=out.stdout.read()
#logging.debug(output)
readB=re.findall("read  bandwidth\s*:\s*([0-9]+\.[0-9]+)",output)
	#print(readB)
writeB=re.findall("write bandwidth\s*:\s*([0-9]+\.[0-9]+)",output)
print("{0} {1}".format(readB[0], writeB[0]))

