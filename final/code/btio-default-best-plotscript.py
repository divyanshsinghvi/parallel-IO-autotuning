import matplotlib.pyplot as plt
import pandas as pd

df= pd.read_csv("bt_default.txt",delimiter=" ")
df[['col1','col2','col3','col4' ]] = df.iloc[:,1].str.split('-',expand=True)
df['totalProcesses']= df['col4']

df[['totalProcesses']]= df[['totalProcesses']].astype(str)
df['config']=df['col1']+'-'+df['col2']+'-'+df['col3']

df_best= pd.read_csv("bt_best.txt",delimiter=" ")
df_best[['col1','col2','col3','col4']] = df_best.iloc[:,1].str.split('-',expand=True)
df_best['totalProcesses']= df_best['col4']

df_best[['totalProcesses']]= df_best[['totalProcesses']].astype(str)

print(df.shape)
df_best['config']=df_best['col1']+'-'+df_best['col2']+'-'+df_best['col3']

print(df_best.shape)
df = pd.merge(df,df_best,on=['config','totalProcesses'])
#print(list(df.columns.values))
df = df.sort_values(by=['config'])
#print(df.iloc[:,1]["200-200-400-4-4-4-1"])
fig, axarr = plt.subplots(4,constrained_layout=True)
i = 0
pd.set_option('display.max_columns', 500)
for f in sorted(set(df['totalProcesses'])):
#    print(df[df['totalProcesses']==f])
    k =  df[df['totalProcesses'] == f]
    k.plot.bar(x='config',y=[2,17,5,20],title=f,figsize=(15,10),legend=True,fontsize=10,ax=axarr[i])
    axarr[i].legend(["read_default","read_active","write_default","write_active"])
    axarr[i].tick_params(axis='x',labelrotation=0)
    i = i+1
#plt.show()
plt.savefig("btiodefaultvsbest.png")
