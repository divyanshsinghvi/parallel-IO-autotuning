import pandas as pd
import json 
import os

with open('../inputfile') as json_data:
    data = json.load(json_data)

print(data)

#pd.DataFrame.from_dict(data).T

#print(pd.read_json("../inputfile"))
