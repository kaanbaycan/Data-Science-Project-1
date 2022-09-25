#!/usr/bin/env python
# coding: utf-8

# In[15]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# In[3]:


df1 = pd.read_csv("turnstile_220514 (1).csv")

df2 = pd.read_csv("turnstile_220514 (2).csv")

df3 = pd.read_csv("turnstile_220514 (3).csv")

df4 = pd.read_csv("turnstile_220514 (5).csv")

df5 = pd.read_csv("turnstile_220514 (6).csv")

df6 = pd.read_csv("turnstile_220514 (7).csv")

df7 = pd.read_csv("turnstile_220514 (8).csv")


# In[9]:


dfbig = pd.concat([df1,df2, df3, df4, df5,df6,df7], ignore_index=True) 


# In[10]:


dfbig.drop(["UNIT","SCP", "C/A"] ,axis=1, inplace= True)


# In[11]:


station_entries = dfbig.STATION.value_counts()
yeni = station_entries.head(50)


# In[12]:


plt.figure(figsize=[20,10])
plt.barh(yeni.index, yeni)


# In[13]:


dfbig.info()


# In[14]:


plt.boxplot(yeni)


# In[75]:


sns.set_theme(font = "Times New Roman", font_scale = 3, palette = "deep")
sns.set_color_codes(palette = "colorblind")


# In[76]:


plt.figure(figsize=[20,30])
sns.barplot(x = yeni, y = yeni.index, orient ="h", palette = "bright",)


# In[ ]:




