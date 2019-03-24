import json 
import os

def parse(filename):
    with open(filename) as json_data:
        data = json.load(json_data)
    return data

if __name__ == "__main__":
    print(parse("inputfile"))

#pd.DataFrame.from_dict(data).T

#print(pd.read_json("../inputfile"))
