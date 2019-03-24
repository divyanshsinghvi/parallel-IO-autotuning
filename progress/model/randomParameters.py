from modelparser import parse
from random import randint
import json

def generateVectorConfig():
    data = parse()
    b = data["lfs"]["setstripe"]["size"]
    data["lfs"]["setstripe"]["size"] = b[randint(0,len(b)-1)]
    b = data["lfs"]["setstripe"]["count"]
    data["lfs"]["setstripe"]["count"] = b[randint(0,len(b)-1)]
    b = data["mpi"]["romio_ds_read"]
    data["mpi"]["romio_ds_read"] = b[randint(0,len(b)-1)]
    b = data["mpi"]["romio_ds_write"]
    data["mpi"]["romio_ds_write"] = b[randint(0,len(b)-1)]
    with open("confex.json","w") as fp:
        json.dump(data,fp)
    print(data)

if __name__ == "__main__":
    generateVectorConfig()
