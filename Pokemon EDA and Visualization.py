
# coding: utf-8

# ### EDA and Visualization on Pokemon dataset

# ### EDA - Exploratory Data Analysis

# In[4]:


# Importing Libraries

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
get_ipython().run_line_magic('matplotlib', 'inline')


# In[6]:


# Importing Data

pokemons = pd.read_csv('pokemon.csv')


# In[8]:


#EDA on pokemons data

# random observations from our dataset.
pokemons.sample(7)


# In[11]:


pokemons.columns


# In[12]:


pokemons.info()


# In[13]:


# since 'Type 2' is almost half filled with NaN, we will drop the column 'Type 2'
# and rename 'Type 1' as just 'Type'

del pokemons['Type 2']
pokemons.rename(columns = {'Type 1' : 'Type'}, inplace = True)


# In[14]:


pokemons.head()


# In[15]:


# for statistics

pokemons.describe()


# In[16]:


len(pokemons.Name.unique())
# we got 800 different pokemons


# In[18]:


pokemons[pokemons.duplicated()]
# we don't have duplicated values in our data frame


# In[19]:


len(pokemons['Type'].unique())
# There are 18 different types of pokemons


# In[20]:


# how many pokemons are in each Type?

pokemons['Type'].value_counts()


# In[21]:


# How many pokemons are in each generatin?

pokemons['Generation'].value_counts()


# In[22]:


sns.countplot(x = 'Generation', data = pokemons, palette = 'nipy_spectral')
plt.title('Number of pokemons grouped by Generaion')


# In[25]:


# pokemons in each type

#pokemons['Type'].value_counts()
pokemons.Type.value_counts()


# In[28]:


plt.figure(figsize = (15, 5))
sns.countplot(pokemons.Type, palette = 'colorblind')


# In[30]:


# checking the distribution of stats with boxplot & violinplot:

sns.set_style('darkgrid')
plt.figure(figsize = (10,6))
sns.boxplot(data = pokemons.drop(['#', 'Total', 'Generation', 'Legendary'], axis = 1), fliersize = 3, palette = 'seismic')
plt.title('Boxplots for stats')

# we have some outlier for each stat


# In[32]:


plt.figure(figsize = (10, 6))
sns.violinplot(data = pokemons.drop(['#', 'Total', 'Generation', 'Legendary'], axis = 1), palette = 'rocket')
plt.title('Violinplot for stats')

#the stas have a similar distribution


# In[33]:


# let's visualize the pokemons grouped by type

pokemons.groupby('Type').sum()


# In[34]:


pokemons.groupby('Type').sum().HP


# In[35]:


pokemons['Type'].unique()


# In[36]:


# Type of pokemons and order them alphabetically in a list

list_types = pokemons['Type'].unique().tolist() # convert the array of types into a list
list_types.sort()  # sorting the list of strings alphabetically 
list_types


# In[39]:


# plotting the tatal of stats for each type of pokemon:

plt.style.use('ggplot')
plt.style.use('seaborn-darkgrid')

stats = pokemons[['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed']]
k = 1
m = 0
palette = ['magma', 'ocean', 'vlag', 'copper', 'mako', 'winter']
plt.figure(figsize = (17, 17))
for i in stats:
    plt.subplot(3, 2, k)
    k = k + 1
    sns.barplot(x = pokemons.groupby('Type').sum()[i], y = list_types, palette = palette[m])
    m = m + 1
    plt.title(str('Total of ' +i))


# In[41]:


# Time for some swarmplots!

k = 1
m = 0
plt.figure(figsize = (15,30))
for i in stats:
    plt.subplot(6, 1, k)
    k = k + 1
    sns.stripplot(x = pokemons.Type, y = pokemons[i], palette = 'Dark2')
    plt.title(str('Total of ')+i + str(' for each type'))


# In[47]:


# let's draw plots for each type separately

k = 1
plt.figure(figsize = (17,22))
for i in list_types:
    plt.subplot(6, 3, k)
    k = k + 1
    sns.barplot(x = pokemons[pokemons.Type == i].sum().drop(['#', 'Name', 'Type', 'Generation', 
                                                             'Legendary', 'Total']).values, 
                y = pokemons[pokemons.Type == i].sum().drop(['#', 'Name', 'Type', 'Generation',
                                                            'Legendary', 'Total']).index, palette = 'inferno')
    plt.title(i)
    plt.xlim(0, 8500)


# In[51]:


pok_melt = pd.melt(pokemons, id_vars = ['Name', 'Type', 'Legendary'], value_vars = ['HP', 'Defense', 'Attack', 
                                                                                    'Sp. Atk', 'Sp. Def', 'Speed'])
pok_melt.head()


# In[52]:


plt.figure(figsize = (17, 22))
k = 1
for i in list_types:
    plt.subplot(6, 3, k)
    k = k + 1
    sns.swarmplot(x = pok_melt.variable, y = pok_melt[pok_melt.Type==i].value, palette = 'gist_stern')
    plt.title(i)
    plt.xlabel('')


# In[54]:


# what if we calculate the mean for each stat and we plot it, In this case the small number of some pokemons of 
# different types will not affect the analysis

# MEAN of stats grouped by pokemon's type

df = pd.DataFrame()
for i in stats:
    df[i] = pokemons.groupby('Type').describe()[i]['mean']
df


# In[56]:


plt.figure(figsize = (16, 20))
k = 1
m = 0
for i in stats:
    plt.subplot(3, 2, k)
    k = k + 1
    sns.barplot(x = df[i], y = df.index, palette = palette[m])
    m = m+1
    plt.title(str('Mean of total ') + i +str(' for each type'))
    plt.xlabel(i)


# In[57]:


k = 1
plt.figure(figsize = (16, 25))
for i in list_types:
    plt.subplot(6, 3, k)
    k = k + 1
    sns.barplot(x = df.loc[i, :].values, y=df.loc[i, :].index, palette = 'Paired')
    plt.title(i)
    plt.xlim(0, 130)
    plt.ylabel('Mean')


# In[61]:


# Copmaring initial total stas and the mean of tatal stats

plt.figure(figsize = (15, 5))
sns.barplot(x = pokemons.groupby('Type').sum().Total.sort_values(ascending = False).index,
            y = pokemons.groupby('Type').sum().Total.sort_values(ascending = False), palette = 'cool')
plt.title('Total of all stats for each type of pokemons')

# top 3 Water, Noraml and Grass


# In[60]:


# Now mean

plt.figure(figsize = (15, 5))
sns.barplot(x = pokemons.groupby('Type').mean().Total.sort_values(ascending = False).index,
            y = pokemons.groupby('Type').mean().Total.sort_values(ascending = False), palette = 'cool')
plt.title('Mean of the total of all stats for each type of pokemons')

# top 3 Dragon, Steel and Flying 
# plotting the mean of the values shows greater insight of data 


# In[62]:


# Whata is the best stats for each type?

best_stats = []
for i in list_types:
    best_stats.append(df.loc[i, :].sort_values(ascending = False).index[0])


# In[65]:


m = 0
for k in best_stats:
    print('Best stat of type ', list_types[m], ' is ', k)
    m = m + 1


# In[66]:


# list al the Mega pokemons

pokemons[pokemons.Name.str.contains('Mega')]


# In[67]:


# Lets fix the Mega pokemons names i.e VenusaurMega Venusaur -> Mega Venusaur

mega_pokemons = ['Mega' + poke.split('Mega')[1] for poke in pokemons[pokemons.Name.str.contains('Mega')].Name]
mega_pokemons


# In[69]:


pokemons = pokemons.replace(to_replace = pokemons[pokemons.Name.str.contains('Mega')].Name.values, value = mega_pokemons)
pokemons.head()


# In[71]:


# Which is the best pokemons for each type? based on each state

for n in list_types:
    print(str('TYPE ')+n.upper())
    for i in stats:
        name = pokemons[(pokemons.Type == n)].sort_values(by = i, ascending = False).Name.values[0]
        print(str('Best ')+i+(' pokemons is ')+name)
    print('******************************************')


# In[72]:


# ploting numbers of pokemons for each generation

sns.countplot(x = 'Generation', data = pokemons, palette = 'seismic')
plt.title('Number of pokemons grouped by Generation')
plt.ylabel('Number of pokemons')


# In[73]:


pokemons.groupby('Generation').sum()


# In[75]:


plt.figure(figsize = (15, 15))
k = 1
for i in stats:
    plt.subplot(3,2,k)
    x = sns.swarmplot(x = 'Generation', y = i, data = pokemons, palette = 'plasma')
    k = k + 1
    plt.title(i+str(' for each generation'))


# In[76]:


plt.figure(figsize = (15, 15))
k = 1
for i in stats:
    plt.subplot(3,2,k)
    sns.boxplot(y = pokemons[i], x=pokemons.Generation)
    k = k + 1
    plt.title(i+str(' for each generation'))


# In[84]:


# How many legendary pokemons are in total?

print('Number of Legendary pokemons ',len(pokemons[pokemons.Legendary == True]))
print('Percentage of Legendary pokemons', (len(pokemons[pokemons.Legendary == True])/len(pokemons))*100)
# there are 65 Legendary pokemons
# 8.125% pokemons are Legendary


# In[85]:


pokemons.groupby('Generation').sum().Legendary
#Generation 3, 5 & 4 have most legendary pokemons


# In[88]:


sns.barplot(x = pokemons.groupby('Generation').sum().Legendary.index,
            y = pokemons.groupby('Generation').sum().Legendary.values, palette= 'CMRmap')


# In[89]:


# How many Legendary pokemons are in each type?

pokemons.groupby('Type').sum().Legendary.sort_values(ascending = False)


# In[90]:


plt.figure(figsize = (15,10))
sns.barplot(x = pokemons.groupby('Type').sum().Legendary.sort_values(ascending = False).index,
            y = pokemons.groupby('Type').sum().Legendary.sort_values(ascending = False).values, palette = 'Paired')


# In[ ]:


# How the stats of Legendary pokemons compared to the otheres?

# In [49]

