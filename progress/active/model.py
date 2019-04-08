## https://www.datacamp.com/community/tutorials/feature-selection-python  -- referred this blog

import pandas as pd
import numpy as np




###Loader
data = pd.read_csv('../stats.txt', delim_whitespace=True)
array = data.values

output_col = 2#int(output_col)
(n,m) = array.shape
print(array)                                                                           
X = array[:,0:m]
Y = array[:,output_col]
Y=Y.astype('int')

X=np.delete(X,output_col,1)

k=0
for i in range(0,m-1):
    if type(X[0][k]) == str:
        X=np.delete(X,k,1)
    #    print(X)
    else : 
        k=k+1
print(X)	

