import json
import shlex
import subprocess
import logging
from pprint import pprint
import re
import os
import sys, getopt

logging.basicConfig(filename='app.log', filemode='a', format='%(name)s - %(levelname)s - %(message)s',level=logging.DEBUG)


with open('confex.json') as f:
    data = json.load(f)


benchmarkFolder = './genericio'
outputFolder = './output'
benchmark = 'Generic-IO'
specific_commands="1024 2"
nodes = "2"
ppn = "8"
write = 0
try:
    opts, args = getopt.getopt(sys.argv[1:],"h:b:o:f:c:n:p:w:",["benchmark=","outputFolder=","benchmarkFolder=", "specificCommands=","nodes=","ppn=","write="])
except getopt.GetoptError:
    print('read_config_general.py -b <benchmark> -o <outputFolder> -f <benchmarkFolder> -c <specificCommands> -n <nodes> -p <ppn> -w <write>')
    sys.exit(2)
for opt, arg in opts:
    if opt == '-h':
        print('read_config_general.py -b <benchmark> -o <outputFolder> -f <benchmarkFolder> -c <specificCommands> -n <nodes> -p <ppn> -w <write>')
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
        ppn = str(arg)
    elif opt in ("-w", "--write"):
        write = arg
#print(benchmark + specific_commands + str(nodes) + str(ppn))
os.chdir(benchmarkFolder)
#out=subprocess.Popen(["lfs", "getstripe","-d", "."], shell=False, stdout=subprocess.PIPE) 

for key in data["lfs"]:
    command = "lfs " + key + "  "
    d =  data["lfs"][key]
    if 'filename' in d:
        command += d['filename']
    else: 
        command += "."
    if 'size' in d:
        command+= " -s " + str(d['size'])
    if 'count' in d:
        command+= " -c " + str(d['count'])
    #print(str(command))
    logging.debug("Lustre parameters:"+ command)
    os.chdir(outputFolder)
    subprocess.Popen(shlex.split(str(command)), shell=False)

mpi_hints=""
os.chdir('../')
for key in data["mpi"]:
    mpi_hints+=key
    mpi_hints+="="+data["mpi"][key]+";"
print(mpi_hints)
logging.debug("MPI parameters:" + mpi_hints)
logging.debug(benchmark + " :" + specific_commands)
log = open('../generic_stats.txt','a')
out=subprocess.Popen(["./run.sh", nodes, ppn, mpi_hints, write, specific_commands], shell=False, stdout=subprocess.PIPE)
output=out.stdout.read()
logging.debug(output.decode('utf-8'))
print(output.decode('utf-8'))

#Bandwidth
bandwidth=re.findall("read/write bandwidth\s*:\s*([0-9]+\.[0-9]+)",output.decode('utf-8')) 
time=re.findall("Time for read/write\s*:\s*([0-9]+\.[0-9]+)",output.decode('utf-8')) 
data=re.findall("total read/write amount\s*:\s*([0-9]+)",output.decode('utf-8')) 
print(benchmark ,end = " ")
print(benchmark ,end = " ", file=log)
print(re.sub(r"\s","-",specific_commands), end = " ")
print(re.sub(r"\s","-",specific_commands), end = " ", file=log)

print("{0} {1} {2}".format(bandwidth,time,data), end = " ")
print("{0} {1} {2}".format(bandwidth[-1],time[-1],data[-1]), end = " ",file=log)



print()
print(file=log)
