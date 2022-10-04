#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import numpy 
df0=pd.read_table("http://web.mta.info/developers/data/nyct/turnstile/turnstile_220305.txt",delimiter=",")
df1=pd.read_table("http://web.mta.info/developers/data/nyct/turnstile/turnstile_220312.txt",delimiter=",")
df2=pd.read_table("http://web.mta.info/developers/data/nyct/turnstile/turnstile_220319.txt",delimiter=",")
df3=pd.read_table("http://web.mta.info/developers/data/nyct/turnstile/turnstile_220326.txt",delimiter=",")
df4=pd.read_table("http://web.mta.info/developers/data/nyct/turnstile/turnstile_220402.txt",delimiter=",")
df5=pd.read_table("http://web.mta.info/developers/data/nyct/turnstile/turnstile_220409.txt",delimiter=",")
df6=pd.read_table("http://web.mta.info/developers/data/nyct/turnstile/turnstile_220416.txt",delimiter=",")
df7=pd.read_table("http://web.mta.info/developers/data/nyct/turnstile/turnstile_220423.txt",delimiter=",")
df8=pd.read_table("http://web.mta.info/developers/data/nyct/turnstile/turnstile_220430.txt",delimiter=",")
df9=pd.read_table("http://web.mta.info/developers/data/nyct/turnstile/turnstile_220507.txt",delimiter=",")
df10=pd.read_table("http://web.mta.info/developers/data/nyct/turnstile/turnstile_220514.txt",delimiter=",")
df11=pd.read_table("http://web.mta.info/developers/data/nyct/turnstile/turnstile_220521.txt",delimiter=",")
df12=pd.read_table("http://web.mta.info/developers/data/nyct/turnstile/turnstile_220528.txt",delimiter=",")
df=pd.concat([df0,df1,df2,df3,df4,df5,df6,df7,df8,df9,df10,df11,df12],ignore_index=True)


# In[3]:


df


# In[ ]:





# In[4]:


df.rename(columns={'EXITS                                                               ':'EXITS'}, inplace=True)


# In[5]:


df


# In[6]:


df['day'] = pd.to_datetime(df['DATE']).dt.day_name()


# In[7]:


df


# In[8]:


df["TIMESTAMP"]=df["DATE"]+df["TIME"]


# In[9]:


df["TURNSTILE"] = df["C/A"]+df["UNIT"]+df["SCP"]


# In[10]:


df


# In[11]:


df["datetime"] = df["DATE"]+df["TIME"]


# In[ ]:





# In[12]:


df.drop(columns=["C/A","UNIT","SCP"],inplace=True)


# In[13]:



df["PREV_TIME"] = df.groupby(["TURNSTILE"]).TIME.shift(1)
df["PREV_EXITS"] = df.groupby(["TURNSTILE"]).EXITS.shift(1)
df["PREV_ENTRIES"] = df.groupby(["TURNSTILE"]).ENTRIES.shift(1)
df.head()


# In[14]:


df.dropna(subset=["PREV_ENTRIES"], axis=0, inplace=True)
df.head()


# In[15]:


df[df.duplicated(subset=["TURNSTILE","STATION","TIMESTAMP"])]


# In[16]:


df['net_entry']= df.sort_values(['TURNSTILE','DATE'],ascending = (False, True)).groupby(['TURNSTILE'])['ENTRIES'].diff()
df['net_exists']= df.sort_values(['TURNSTILE','DATE'],ascending = (False, True)).groupby(['TURNSTILE'])['EXITS'].diff()


# In[17]:


df


# In[18]:


df.describe()


# In[19]:


(df[(df["net_entry"] < 0) |(df['net_exists']<0)].groupby(['TURNSTILE'])).size()


# In[ ]:





# In[20]:


df.drop(['LINENAME','DESC', 'ENTRIES', 'EXITS', 'PREV_TIME', 'PREV_ENTRIES', 'PREV_EXITS'], axis=1 , inplace=True)


# In[21]:


df


# In[22]:


import seaborn as sns
sns.heatmap(df.corr(),annot=True,cmap='RdYlGn',linewidths=0.2)


# In[30]:


df['TRAFFIC'] = df['net_entry'] + df['net_exists']


# In[56]:



from matplotlib import pyplot as plt
week_day_traffic =pd.DataFrame(df.groupby('day')['TRAFFIC'].sum().sort_values(ascending=False).reset_index())
plt.figure(figsize =(12, 7))
plt.box(False)
plt.barh(week_day_traffic['day'],week_day_traffic['TRAFFIC'])

for index, value in enumerate(week_day_traffic['TRAFFIC']):
    plt.text(value, index, str(value))


# In[32]:


most_seven_station = pd.DataFrame(df.groupby('STATION')['TRAFFIC'].sum().sort_values(ascending=False).reset_index())
most_seven_station.head(7)


# In[33]:


most_crowded_hours = pd.DataFrame(df.groupby('TIME')['TRAFFIC'].sum().sort_values(ascending=False).reset_index())
most_crowded_hours.tail(15)


# In[34]:


top_seven = ('34 ST-PENN STA','86 ST','GRD CNTRL-42 ST','34 ST-HERALD SQ','125 ST','23 ST','14 ST-UNION SQ')


# In[35]:


top_seven_df = pd.DataFrame(df[df['STATION'].isin(top_seven)])
top_seven_df.sample(10)


# In[36]:


df_top7_daily = top_seven_df.groupby(["STATION","day"]).sum()
week_day_traffic_heatmap =df_top7_daily.groupby(['day','STATION'])['TRAFFIC'].sum().reset_index()
week_day_traffic_heatmap = week_day_traffic_heatmap.groupby(["STATION","day"]).TRAFFIC.mean().reset_index()
df_top7_heatmap = week_day_traffic_heatmap.pivot("day","STATION","TRAFFIC")
df_top7_heatmap = df_top7_heatmap.reindex(index = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"])

df_top7_heatmap.head(10)


# In[37]:


plt.figure(figsize=(15,8),dpi=200)
sns.heatmap(df_top7_heatmap,annot=True, linewidths=2, cmap="Oranges",cbar_kws={'label': 'Traffic'})
plt.title("Top 7 Busiest Stations / Day",weight="bold",c="red", fontsize=15)


# In[71]:


DF = df.groupby(['STATION'])['TRAFFIC'].sum().sort_values(ascending = False).head(5)
DF = pd.DataFrame(DF.reset_index())
DF


# In[74]:


plt.figure(figsize=(15,8))
plt.title('TOP 5 STATIONS ',family='CALIBRI',fontsize = 20,loc='CENTER',color='black');
sns.barplot(data = DF, y = DF.STATION, x = DF.TRAFFIC)
plt.show()


# In[48]:


# a sum of daily entires and exists for top 5 stations
top5_stations = (df.groupby(['STATION'])['TRAFFIC'].sum()
                   .reset_index()
                   .sort_values(by='TRAFFIC',ascending=False) 
                   .STATION.head())
top5_stations


# In[51]:


top5_stations_traffic =      df[df['STATION'].isin(top5_stations)].sort_values(by='TRAFFIC',ascending=False)
top5_stations_traffic.head()


# In[63]:


# plotting the top 5 busiest stations

sns.set(style="white", font_scale=1.4)
plt.figure(figsize=(16,6))

sns.barplot(x=top5_stations.index, y=top5_stations, color='royalblue')

plt.title('TOP 5 Busiest Stations', weight = 'bold', pad='30').set_fontsize('20')
plt.xlabel('Traffic', weight='bold', fontsize='20', labelpad=20)
plt.ylabel('STATION', weight='bold', fontsize='20', labelpad=20)

sns.despine()

plt.savefig('TOP 5 Busiest Stations ');


# In[ ]:




