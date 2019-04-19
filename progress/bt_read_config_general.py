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

with open('confex.json') as f:
    data = json.load(f)

benchmarkFolder = './btio-pnetcdf-1.1.1'
outputFolder = './output'
benchmark = 'btio-pnetcdf-1.1.1'
specific_commands="512 512 512"
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


os.chdir('../')
arr = ["w","r"]
wT=[]
for i in arr:
    inputfile = "inputbt.data"
    os.remove(inputfile)
    with open(inputfile, "a") as file:
        file.write(i + "\n3\n3\n" +specific_commands+"\n"+outputFolder )                 
    
    mpi_hints=""
    for key in data["mpi"]:
        mpi_hints+=key
        mpi_hints+="="+data["mpi"][key]+";"
    
    mpi_hints=""    
    logging.debug("MPI parameters:" + mpi_hints)
    logging.debug(benchmark + " :" + specific_commands)
    log = open('../bt_stats.txt','a')
    out=subprocess.Popen(["./run.sh", nodes, ppn, mpi_hints,specific_commands], shell=False, stdout=subprocess.PIPE)
    output=out.stdout.read()
    logging.debug(output.decode('utf-8'))
#    print(output.decode('utf-8'))
    if i == "r":
		#Bandwidth
    	rB=re.findall("I/O bandwidth\s*:\s*([0-9]+\.[0-9]+)",output.decode('utf-8'))
    	#Data
    	rD=re.findall("Totail I/O amount\s*:\s*([0-9]+\.[0-9]+)",output.decode('utf-8'))
    	#time
    	rT=re.findall("Time in sec\s*:\s*([0-9]+\.[0-9]+)",output.decode('utf-8'))
    else:
		#Bandwidth
    	wB=re.findall("I/O bandwidth\s*:\s*([0-9]+\.[0-9]+)",output.decode('utf-8'))
    	#Data
    	wD=re.findall("Totail I/O amount\s*:\s*([0-9]+\.[0-9]+)",output.decode('utf-8'))
    	#time
    	wT=re.findall("Time in sec\s*:\s*([0-9]+\.[0-9]+)",output.decode('utf-8'))
    
#print(wT)

print(benchmark ,end = " ")
print(benchmark ,end = " ", file=log)
print(re.sub(r"\s","-",specific_commands), end = " ")
print(re.sub(r"\s","-",specific_commands), end = " ", file=log)

print("{0} {1} {2} {3} {4} {5}".format(rB[0],rD[0],rT[0],wB[0],wD[0],wT[0]), end = " ")
print("{0} {1} {2} {3} {4} {5}".format(rB[0],rD[0],rT[0],wB[0],wD[0],wT[0]), end = " ",file=log)
   # print("{0} {1} {2} {3} {4} {5} {6} {7}".format(readB[0],readD[0],readT[0],writeB[0],writeD[0],writeT[0],openT[0],closeT[0]), end = " ",file=log)
for hints in data["lfs"]["setstripe"]:
    print(data["lfs"]["setstripe"][hints],end=" ")
    print(data["lfs"]["setstripe"][hints],end=" ",file=log)

hints_array=mpi_hints.split(";")
for hints in hints_array:
    if(len(hints.split('=')) == 2): 
        print(hints.split("=")[1],end=" ")
        print(hints.split("=")[1],end=" ",file=log)

print()
print(file=log)
