import json
import shlex
import subprocess
import logging
from pprint import pprint
import re
import os
import glob
import sys, getopt

logging.basicConfig(filename='app.log', filemode='a', format='%(name)s - %(levelname)s - %(message)s',level=logging.DEBUG)


with open('confex.json') as f:
    data = json.load(f)


benchmarkFolder = './genericio'
outputFolder = './output'
benchmark = 'Generic-IO'
specific_commands="1024 2"
mpi_hints=os.getcwd()+"/genericio/romhint"
nodes = "2"
ppn = "8"
write = "0"
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
os.chdir(benchmarkFolder)

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
mpi_hints_l=""
os.remove("romhint")
with open("romhint","a") as mpihint:
    for key in data["mpi"]:
        mpi_hints_l+=key
        mpi_hints_l+="="+data["mpi"][key]+";"
        mpihint.write(key+" "+str(data["mpi"][key])+"\n")

logging.debug("MPI parameters:" + mpi_hints)
logging.debug(benchmark + " :" + specific_commands)
log = open('../generic_stats.txt','a')
out=subprocess.Popen(["./run.sh", nodes, ppn, mpi_hints, "1", specific_commands], shell=False, stdout=subprocess.PIPE)
output=out.stdout.read()
logging.debug(output.decode('utf-8'))
#print(output.decode('utf-8'))
out2=subprocess.Popen(["./run.sh", nodes, ppn, mpi_hints, "0", specific_commands], shell=False, stdout=subprocess.PIPE)
output2=out2.stdout.read()
logging.debug(output2.decode('utf-8'))

#print(output2.decode('utf-8'))
#Bandwidth
bandwidth_write=re.findall("read/write bandwidth\s*:\s*([0-9]+\.[0-9]+)",output.decode('utf-8')) 
time_write=re.findall("Time for read/write\s*:\s*([0-9]+\.[0-9]+)",output.decode('utf-8')) 
readD_write=re.findall("total read/write amount\s*:\s*([0-9]+)",output.decode('utf-8')) 

bandwidth_read=re.findall("read/write bandwidth\s*:\s*([0-9]+\.[0-9]+)",output2.decode('utf-8')) 
time_read=re.findall("Time for read/write\s*:\s*([0-9]+\.[0-9]+)",output2.decode('utf-8')) 
readD_read=re.findall("total read/write amount\s*:\s*([0-9]+)",output2.decode('utf-8')) 
print(benchmark ,end = " ")
print(benchmark ,end = " ", file=log)
print(re.sub(r"\s","-",specific_commands), end = " ")
print(re.sub(r"\s","-",specific_commands), end = " ", file=log)

print("{0} {1} {2} {3} {4} {5} {6} {7}".format(write,nodes,bandwidth_write[-1],time_write[-1],readD_write[-1], bandwidth_read[0], time_read[0], readD_read[0]), end = " ")
print("{0} {1} {2} {3} {4} {5} {6} {7}".format(write,nodes,bandwidth_write[-1],time_write[-1],readD_write[-1], bandwidth_read[0], time_read[0], readD_read[0]), end = " ",file=log)

for hints in data["lfs"]["setstripe"]:
        print(data["lfs"]["setstripe"][hints],end=" ")
        print(data["lfs"]["setstripe"][hints],end=" ",file=log)

hints_array=mpi_hints_l.split(";")
for hints in hints_array:
    if(len(hints.split('=')) == 2):
        print(hints.split("=")[1],end=" ")
        print(hints.split("=")[1],end=" ",file=log)
for fl in glob.glob("./output/out*"):
    os.remove(fl)


print()
print(file=log)
