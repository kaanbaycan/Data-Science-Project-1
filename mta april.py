#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
df0=pd.read_table("http://web.mta.info/developers/data/nyct/turnstile/turnstile_220402.txt",delimiter=",")
df1=pd.read_table("http://web.mta.info/developers/data/nyct/turnstile/turnstile_220409.txt",delimiter=",")
df2=pd.read_table("http://web.mta.info/developers/data/nyct/turnstile/turnstile_220416.txt",delimiter=",")
df3=pd.read_table("http://web.mta.info/developers/data/nyct/turnstile/turnstile_220423.txt",delimiter=",")
df4=pd.read_table("http://web.mta.info/developers/data/nyct/turnstile/turnstile_220430.txt",delimiter=",")
df=pd.concat([df0,df1,df2,df3,df4],ignore_index=True)
df


# In[3]:


df.columns


# In[4]:


# rather than : df.rename(columns={'EXITS                                                               ':'EXITS'}, inplace=True)

df.columns = df.columns.str.strip() #I guess better


# In[5]:


df['day'] = pd.to_datetime(df['DATE']).dt.day_name()


# In[6]:


df["TURNSTILE"] = df["C/A"]+df["UNIT"]+df["SCP"]


# In[7]:


df.drop(columns=["C/A","UNIT","SCP"],inplace=True)


# In[8]:


df.describe()


# In[9]:


import seaborn as sns
sns.heatmap(df.corr(),annot=True,cmap='RdYlGn',linewidths=0.2)


# In[17]:


df['net_entry']= df.sort_values(['TURNSTILE','DATE'],ascending = (False, True)).groupby(['TURNSTILE'])['ENTRIES'].diff()
df['net_exits']= df.sort_values(['TURNSTILE','DATE'],ascending = (False, True)).groupby(['TURNSTILE'])['EXITS'].diff()


# In[19]:


df['TRAFFIC'] = df['net_entry'] + df['net_exits']


# In[22]:


(df[(df["net_entry"] < 0) |(df['net_exits']<0)].groupby(['TURNSTILE'])).size()


# In[29]:


df_april=df.loc[(df["net_entry"] > 0) & (df['net_exits']>0)].reset_index(drop=True)


# In[30]:


from matplotlib import pyplot as plt
week_day_traffic =pd.DataFrame(df_april.groupby('day')['TRAFFIC'].sum().sort_values(ascending=False).reset_index())
plt.figure(figsize =(12, 7))
plt.box(False)
plt.barh(week_day_traffic['day'],week_day_traffic['TRAFFIC'])

for index, value in enumerate(week_day_traffic['TRAFFIC']):
    plt.text(value, index, str(value))


# In[32]:


most_seven_station = pd.DataFrame(df_april.groupby('STATION')['TRAFFIC'].sum().sort_values(ascending=False).reset_index())
most_seven_station.head(7)


# In[33]:


most_crowded_hours = pd.DataFrame(df_april.groupby('TIME')['TRAFFIC'].sum().sort_values(ascending=False).reset_index())
most_crowded_hours.tail(15)


# In[34]:


top_seven =("HUNTS POINT AV","86 ST"	,"34 ST-HERALD SQ","42 ST-PORT AUTH","QUEENS PLAZA","34 ST-PENN STA","GRD CNTRL-42 ST")


# In[35]:


top_seven_df = pd.DataFrame(df_april[df_april['STATION'].isin(top_seven)])
top_seven_df.sample(10)


# In[36]:



df_top7_daily = top_seven_df.groupby(["STATION","day"]).sum()
week_day_traffic_heatmap =df_top7_daily.groupby(['day','STATION'])['TRAFFIC'].sum().reset_index()
week_day_traffic_heatmap = week_day_traffic_heatmap.groupby(["STATION","day"]).TRAFFIC.mean().reset_index()
df_top7_heatmap = week_day_traffic_heatmap.pivot("day","STATION","TRAFFIC")
df_top7_heatmap = df_top7_heatmap.reindex(index = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"])


# In[37]:


df_top7_heatmap.head(10)


# In[38]:


plt.figure(figsize=(15,8),dpi=200)
sns.heatmap(df_top7_heatmap,annot=True, linewidths=2, cmap="Oranges",cbar_kws={'label': 'Traffic'})
plt.title("Top 7 Busiest Stations / Day",weight="bold",c="red", fontsize=15)


# In[43]:


DF = df_april.groupby(['STATION'])['TRAFFIC'].sum().sort_values(ascending = False).head(5)
DF = pd.DataFrame(DF.reset_index())
DF


# In[44]:


plt.figure(figsize=(15,8))
plt.title('TOP 5 STATIONS ',family='CALIBRI',fontsize = 20,loc='CENTER',color='black');
sns.barplot(data = DF, y = DF.STATION, x = DF.TRAFFIC)
plt.show()


# In[45]:


top5_stations = (df_april.groupby(['STATION'])['TRAFFIC'].sum()
                   .reset_index()
                   .sort_values(by='TRAFFIC',ascending=False) 
                   .STATION.head())
top5_stations


# In[46]:


top5_stations_traffic =df_april[df_april['STATION'].isin(top5_stations)].sort_values(by='TRAFFIC',ascending=False)
top5_stations_traffic.head()


# In[48]:


# plotting the top 5 busiest stations

sns.set(style="white", font_scale=1.4)
plt.figure(figsize=(16,6))

sns.barplot(x=top5_stations.index, y=top5_stations, color='royalblue')

plt.title('TOP 5 Busiest Stations in April', weight = 'bold', pad='30').set_fontsize('20')
plt.xlabel('Traffic', weight='bold', fontsize='20', labelpad=20)
plt.ylabel('STATION', weight='bold', fontsize='20', labelpad=20)

sns.despine()


# In[ ]:




