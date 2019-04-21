import matplotlib.pyplot as plt
import pandas as pd

df= pd.read_csv("default.txt",delimiter=" ")
df[['col1','col2','col3','col4','col5','col6','col7'  ]] = df.iloc[:,1].str.split('-',expand=True)
df[['col4','col5','col6']] = df[['col4','col5','col6']].astype(int)
df['totalProcesses']= df['col4']*df['col5']*df['col6']

df[['col4','col5','col6']] = df[['col4','col5','col6']].astype(str)
df[['totalProcesses']]= df[['totalProcesses']].astype(str)
df['totalProcesses']=df['col4']+'-'+df['col5']+'-'+df['col6']+'-'+df['totalProcesses']

df['config']=df['col1']+'-'+df['col2']+'-'+df['col3']

df_best= pd.read_csv("best.txt",delimiter=" ")
df_best[['col1','col2','col3','col4','col5','col6','col7'  ]] = df_best.iloc[:,1].str.split('-',expand=True)
df_best[['col4','col5','col6']] = df_best[['col4','col5','col6']].astype(int)
df_best['totalProcesses']= df_best['col4']*df_best['col5']*df_best['col6']

df_best[['col4','col5','col6']] = df_best[['col4','col5','col6']].astype(str)
df_best[['totalProcesses']]= df_best[['totalProcesses']].astype(str)
df_best['totalProcesses']=df_best['col4']+'-'+df_best['col5']+'-'+df_best['col6']+'-'+df_best['totalProcesses']

print(df.shape)
df_best['config']=df_best['col1']+'-'+df_best['col2']+'-'+df_best['col3']

print(df_best.shape)
df = pd.merge(df,df_best,on=['config','totalProcesses'])
#print(df.iloc[:,1]["200-200-400-4-4-4-1"])
fig, axarr = plt.subplots(4,constrained_layout=True)
i = 0
pd.set_option('display.max_columns', 500)
for f in sorted(set(df['totalProcesses'])):
    k =  df[df['totalProcesses'] == f]
    k.plot.bar(x='config',y=[2,21,5,24],title=f,figsize=(15,10),legend=True,fontsize=10,ax=axarr[i])
    axarr[i].legend(["read_default","read_active","write_default","write_active"])
    axarr[i].tick_params(axis='x',labelrotation=0)
    i = i+1
plt.savefig("s3diodefaultvsbest.png")
