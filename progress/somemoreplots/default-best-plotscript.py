import matplotlib.pyplot as plt
import pandas as pd
df= pd.read_csv("default.txt",delimiter=" ")
df['col1'] = df.iloc[:,1].str[:-2]
df_best= pd.read_csv("xgresult.txt",delimiter=" ")
df_best['col1'] = df.iloc[:,1].str[:-2]
df = pd.merge(df,df_best,on=['col1'])

#print(df.iloc[:,1]["200-200-400-4-4-4-1"])
i = 0
pd.set_option('display.max_columns', 500)
axis = df.plot.bar(x='col1',y=[5,17],title="default v/s optimized",figsize=(15,10),legend=True,fontsize=14)
axis.legend(["write_default","write_XGBoost"],fontsize=14)
axis.tick_params(axis='x',labelrotation=0, labelsize=11)
axis.tick_params(axis='y', labelsize=14)
i = i+1
plt.savefig("xgboosts3diodefaultvsbest.png")
