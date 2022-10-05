#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import date, time
from datetime import datetime as dt


# In[2]:


df1 = pd.read_csv("http://web.mta.info/developers/data/nyct/turnstile/turnstile_220507.txt")

df2 = pd.read_csv("http://web.mta.info/developers/data/nyct/turnstile/turnstile_220514.txt")

df3 = pd.read_csv("http://web.mta.info/developers/data/nyct/turnstile/turnstile_220521.txt")

df4 = pd.read_csv("http://web.mta.info/developers/data/nyct/turnstile/turnstile_220528.txt")

df5 = pd.read_csv("http://web.mta.info/developers/data/nyct/turnstile/turnstile_220604.txt")


# In[3]:


dfmay = pd.concat([df1,df2, df3, df4, df5], ignore_index=True) 


# In[4]:


dfmay.info()


# In[5]:


dfmay["DATE"]+" "+ dfmay["TIME"]


# In[6]:


datettimes = pd.to_datetime(dfmay["DATE"] + " " + dfmay["TIME"])


# In[7]:


dfmay.insert(loc = 11,column = "datetime", value = datettimes )


# In[8]:


turnstiles = dfmay["C/A"] + dfmay["UNIT"] + dfmay["SCP"]


# In[9]:


dfmay.insert(loc = 12,column = "turnstile", value = turnstiles )


# In[10]:


dfmay.drop(columns = ["C/A", "UNIT", "SCP", "DATE", "TIME"], inplace = True)


# In[11]:


dfmay.info()


# In[12]:


dfmay.rename(columns = lambda x: x.strip(), inplace = True)


# In[13]:


dfmay.insert(loc = 8,column= "density",value = dfmay["ENTRIES"] + dfmay["EXITS"])


# In[14]:


dfmay.info()


# In[15]:


dfmay['datetime'].dt.dayofweek


# In[16]:


dfmay['day'] = dfmay['datetime'].dt.day_name()


# In[20]:


dfmay.info()


# In[52]:


densities = dfmay.groupby('STATION').density.sum()


# In[77]:


densities.sort_values(ascending = False, inplace = True)


# In[78]:


densities.head(20)


# In[79]:


dens = densities.head(30)


# In[80]:


plt.figure(figsize=(20,10))
plt.barh(y = dens.index, width = dens,)


# In[ ]:




