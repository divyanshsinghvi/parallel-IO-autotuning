import json
from pprint import pprint

with open('config.json') as f:
    data = json.load(f)

print(data["mpi"])

mpi_hints=""

for key in data["mpi"]:
    mpi_hints+=key
    mpi_hints+="="+data["mpi"][key]+";"


print(mpi_hints)


for key in data["lfs"]:
    command = key + "  "
    d =  data["lfs"][key]
    if 'filename' in d:
        command += d['filename']
    if 'size' in d:
        command+= " -s " + d['size']
    if 'count' in d:
        command+= " -c " + d['count']
    print command
#pprint(data)

