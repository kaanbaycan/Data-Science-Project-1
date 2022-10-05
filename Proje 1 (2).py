#!/usr/bin/env python
# coding: utf-8

# In[1]:


#importing the libraries which will be used later

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import date, time
from datetime import datetime as dt


# In[2]:


#Getting the turnstile data from MTA

df1 = pd.read_csv("http://web.mta.info/developers/data/nyct/turnstile/turnstile_220507.txt")

df2 = pd.read_csv("http://web.mta.info/developers/data/nyct/turnstile/turnstile_220514.txt")

df3 = pd.read_csv("http://web.mta.info/developers/data/nyct/turnstile/turnstile_220521.txt")

df4 = pd.read_csv("http://web.mta.info/developers/data/nyct/turnstile/turnstile_220528.txt")

df5 = pd.read_csv("http://web.mta.info/developers/data/nyct/turnstile/turnstile_220604.txt")


# In[3]:


#After importing weekly data, we have to convert into one table so we use pd.concat function

dfmay = pd.concat([df1,df2, df3, df4, df5], ignore_index=True) 


# In[4]:


#Checking for null values as well as the Data types

dfmay.info()


# In[5]:


#Since we have 2 different columns as Date and Time, we are merging them into one datetime column 
#Using *datetime* library

datettimes = pd.to_datetime(dfmay["DATE"] + " " + dfmay["TIME"])


# In[6]:


#inserting the datetime column into the dataframe

dfmay.insert(loc = 11,column = "datetime", value = datettimes )


# In[7]:


#we have 3 different columns regarding the turnstiles so we merge them as well

turnstiles = dfmay["C/A"] + dfmay["UNIT"] + dfmay["SCP"]


# In[8]:


#inserting the turnstiles column into our dataframe

dfmay.insert(loc = 12,column = "turnstile", value = turnstiles )


# In[9]:


#Dropping irrelevant data from the datafram in order to enhance the efficiency

dfmay.drop(columns = ["C/A", "UNIT", "SCP", "DATE", "TIME", "DIVISION", "DESC", "LINENAME"], inplace = True)


# In[10]:


#checking the dataframe

dfmay.columns = dfmay.columns.str.strip()


# In[11]:


#again check for the datatypes since we have made some modifications regarding the dataframe

dfmay.info()


# In[12]:


#since the turnstile data increases cumulatively we have to take the difference between the rows by grouping them by stations

dfmay['net_entry']= dfmay.sort_values(['turnstile','datetime'],ascending = (False, True)).groupby(['turnstile'])['ENTRIES'].diff()
dfmay['net_exits']= dfmay.sort_values(['turnstile','datetime'],ascending = (False, True)).groupby(['turnstile'])['EXITS'].diff()


# In[13]:


#these columns are not essential since already calculated the net exit and entry in [12]

dfmay.drop(columns = ["ENTRIES", "EXITS"], inplace = True)


# In[ ]:





# In[14]:


#Another check for the net entries and exits for negative values

dfmay.describe()


# In[17]:


#Eliminating the negative values

dfmay = dfmay[dfmay['net_entry'] >= 0]
dfmay = dfmay[dfmay["net_exits"] >= 0]


# In[18]:


#Checking the values again

dfmay.describe()


# In[19]:


#let's find the total number of people enters and exits the station

dfmay.insert(loc = 5, column = "total", value = dfmay["net_entry"] + dfmay["net_exits"])


# In[20]:


#Whenever a column added we are checking for negative values in essence

dfmay.describe()


# In[21]:


#Here is the final version of our dataframe

dfmay


# In[ ]:




