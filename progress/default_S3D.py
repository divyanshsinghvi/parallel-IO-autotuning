import json
import shlex
import subprocess
import logging
from pprint import pprint
import re
import os
import sys, getopt

#logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(filename='app.log', filemode='a', format='%(name)s - %(levelname)s - %(message)s',level=logging.DEBUG)
#logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')


benchmarkFolder = './S3D-IO'
outputFolder = './output'
benchmark = 'S3D-IO'
specific_commands="50 50 100 2 2 4 1"
nodes = "2"
ppn = "8"
try:
    opts, args = getopt.getopt(sys.argv[1:],"h:b:o:f:c:n:p:",["benchmark=","outputFolder=","benchmarkFolder=", "specificCommands=","nodes=","ppn="])
except getopt.GetoptError:
    print('read_config_general.py -b <benchmark> -o <outputFolder> -f <benchmarkFolder> -c <specificCommands> -n <nodes> -p <ppn>')
    sys.exit(2)
for opt, arg in opts:
    if opt == '-h':
        print('read_config_general.py -b <benchmark> -o <outputFolder> -f <benchmarkFolder> -c <specificCommands> -n <nodes> -p <ppn>')
        sys.exit()
    elif opt in ("-b", "--benchmark"):
        benchmark = arg
    elif opt in ("-f", "--benchmarkFolder"):
        benchmarkFolder = arg
    elif opt in ("-o", "--outputFolder"):
        outputFolder = arg
    elif opt in ("-c", "--specificCommands"):
        specific_commands = arg
    elif opt in ("-n", "--nodes"):
        nodes = arg
    elif opt in ("-p", "--ppn"):
        ppn = arg
#print(benchmark + specific_commands + str(nodes) + str(ppn))
os.chdir(benchmarkFolder)
#out=subprocess.Popen(["lfs", "getstripe","-d", "."], shell=False, stdout=subprocess.PIPE) 


mpi_hints=""
mpi_hints="romio_cb_write=enable"


logging.debug("MPI parameters:" + mpi_hints)
logging.debug(benchmark + " :" + specific_commands)
log = open('../stats.txt','a')
out=subprocess.Popen(["./run.sh", nodes, ppn, mpi_hints,specific_commands], shell=False, stdout=subprocess.PIPE)
output=out.stdout.read()
logging.debug(output.decode('utf-8'))
#Bandwidth
readB=re.findall("read  bandwidth\s*:\s*([0-9]+\.[0-9]+)",output.decode('utf-8'))
writeB=re.findall("write bandwidth\s*:\s*([0-9]+\.[0-9]+)",output.decode('utf-8'))

#Data
readD=re.findall("total read  amount\s*:\s*([0-9]+\.[0-9]+)",output.decode('utf-8'))
writeD=re.findall("total write amount\s*:\s*([0-9]+\.[0-9]+)",output.decode('utf-8'))

#time
readT=re.findall("Time for read\s*:\s*([0-9]+\.[0-9]+)",output.decode('utf-8'))
writeT=re.findall("Time for write\s*:\s*([0-9]+\.[0-9]+)",output.decode('utf-8'))
openT=re.findall("Time for open\s*:\s*([0-9]+\.[0-9]+)",output.decode('utf-8'))
closeT=re.findall("Time for close\s*:\s*([0-9]+\.[0-9]+)",output.decode('utf-8'))

print(benchmark ,end = " ")
print(benchmark ,end = " ", file=log)
print(re.sub(r"\s","-",specific_commands), end = " ")
print(re.sub(r"\s","-",specific_commands), end = " ", file=log)

print("{0} {1} {2} {3} {4} {5} {6} {7}".format(readB[0],readD[0],readT[0],writeB[0],writeD[0],writeT[0],openT[0],closeT[0]), end = " ")
print("{0} {1} {2} {3} {4} {5} {6} {7}".format(readB[0],readD[0],readT[0],writeB[0],writeD[0],writeT[0],openT[0],closeT[0]), end = " ",file=log)

print()
print(file=log)
