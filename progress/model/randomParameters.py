from modelparser import parse
from random import randint
import json
import os

def generateVectorConfig():
    data = parse(os.path.join(os.path.dirname(__file__), 'inputfile'))
    cat = parse(os.path.join(os.path.dirname(__file__), "paramcat"))
    z = []
    b = data["lfs"]["setstripe"]["size"]
    v = randint(0,len(b)-1)
    data["lfs"]["setstripe"]["size"] = b[v]

    if cat["lfs"]["setstripe"]["size"] == 'cat':
        z.append(v)
    else: 
        z.append(b[v])

    b = data["lfs"]["setstripe"]["count"]
    v = randint(0,len(b)-1)
    data["lfs"]["setstripe"]["count"] = b[v]
    
    if cat["lfs"]["setstripe"]["count"] == 'cat':
        z.append(v)
    else: 
        z.append(b[v])
    b = data["mpi"]["romio_ds_read"]
    v = randint(0,len(b)-1)
    data["mpi"]["romio_ds_read"] = b[v]
    if cat["mpi"]["romio_ds_read"] == 'cat':
        z.append(v)
    else: 
        z.append(b[v])
    b = data["mpi"]["romio_ds_write"]
    v = randint(0,len(b)-1)
    data["mpi"]["romio_ds_write"] = b[v]
    if cat["mpi"]["romio_ds_write"] == 'cat':
        z.append(v)
    else: 
        z.append(b[v])
    with open("confex.json","w") as fp:
        json.dump(data,fp)
    print(data)
    print z

if __name__ == "__main__":
    generateVectorConfig()
