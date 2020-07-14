#!/usr/bin/env python
# coding: utf-8

# In[1]:


#import necessary packages: pandas, numpy, pyplot, and seaborn
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


# In[2]:


#import UDH kindergarten vaccination data csv into dataframe
ut_vax = pd.read_csv('utah_vax_by_school_district_2014.csv', header=0, names=['district', 'school', 'enrollment', 'num_exempt', 'num_fullvax', 'pct_fullvax', 'pct_MMR', 'pct_DTaP'])
ut_vax.district.astype('category');


# In[3]:


#create list of the largest districts in Utah, and create a dataframe containing the data for these districts
lg_dist = ['Alpine', 'Davis', 'Granite', 'Jordan', 'Canyons', 'Nebo', 'Weber', 'Washington', 'Salt Lake', 'Provo', 'Charter/private']
ut_vax_large = ut_vax[ut_vax.district.isin(lg_dist)]

ut_vax_large.head()


# In[4]:


#create a swarm plot that shows the distribution of MMR immunization rates for the largest school districts in Utah
plt.style.use('seaborn')
plt.figure(figsize=(15,5))
plt.axhline(y=93, color='darkred', linestyle=':')
chart1 = sns.swarmplot(x='district', y='pct_MMR', data=ut_vax_large, order=lg_dist)
chart1.set_xticklabels(chart1.get_xticklabels(), rotation=45, horizontalalignment='right')
chart1.set_title('Kindergarten MMR Vaccination Rates in Utah\'s Largest Districts')
chart1.set(xlabel='School District', ylabel='% of Students Vaccinated')
chart1.annotate('Minimum Herd Immunity Level', xy=[7.5, 93], xytext=(4.5, 75), arrowprops=dict(facecolor='grey', shrink=0.05));
plt.savefig('plot1.png', dpi=300, bbox_inches = "tight")


# In[5]:


#import csv containing NCES data for elementary schools in Utah.
ut_kinder = pd.read_csv('utah_k_schools.csv')

#to get names to match, drop 'Elementary' from vax table and 'School' from NCES table
ut_vax['name_short'] = ut_vax['school'].str.replace(r' Elementa.+', '')
ut_vax['name_short'] = ut_vax['name_short'].str.replace(r' Schoo.+', '')
ut_kinder['name_short'] = ut_kinder['school_name'].str.replace(r' Scho.+', '')
ut_kinder['district'] = ut_kinder['district'].str.replace(r' District', '')
ut_kinder['district'] = ut_kinder['district'].str.replace(r' City', '')


# In[6]:


#inner merge the UDH dataset with the NCES dataset
kinder_merge = pd.merge(ut_vax, ut_kinder, how='inner', on='name_short')
kinder_merge = kinder_merge.drop(['school', 'school_name'], axis=1)
kinder_merge[['free_lunch', 'reduced_lunch', 'students']]=kinder_merge[['free_lunch', 'reduced_lunch', 'students']].replace('?', np.nan)
kinder_merge['pct_freered'] = (kinder_merge['free_lunch'].astype(float) + kinder_merge['reduced_lunch'].astype(float))/kinder_merge['students'].astype(float) * 100

kinder_merge.head()


# In[7]:


#create box plot for immunization rate distributions based on locale
colordict = {'City: Midsize':'lightblue', 'City: Small':'lightblue', 'Suburb: Large':'lightgreen', 'Suburb: Small':'lightgreen', 'Town: Fringe':'pink', 'Town: Distant':'pink', 'Town: Remote':'pink', 'Rural: Fringe':'tan', 'Rural: Distant':'tan', 'Rural: Remote':'tan'}
plt.axhline(y=93, color='darkred', linestyle=':')
chart2 = sns.boxplot(x='locale', y='pct_MMR', data=kinder_merge, order=['City: Midsize', 'City: Small', 'Suburb: Large', 'Suburb: Small', 'Town: Fringe', 'Town: Distant', 'Town: Remote', 'Rural: Fringe', 'Rural: Distant', 'Rural: Remote'], palette=colordict, fliersize=2);
chart2.set_xticklabels(chart2.get_xticklabels(), rotation=45, horizontalalignment='right');
chart2.set(title='Kindergarten MMR Vaccination Rates by Locale', xlabel='', ylabel='% of Students with MMR Vaccine')
plt.savefig('plot2.png', dpi=300, bbox_inches = "tight")


# In[8]:


#scatter plot of pct_mmr vs pct_freered
colordict = {'City: Midsize':'lightblue', 'City: Small':'lightblue', 'Suburb: Large':'lightgreen', 'Suburb: Small':'lightgreen', 'Town: Fringe':'pink', 'Town: Distant':'pink', 'Town: Remote':'pink', 'Rural: Fringe':'tan', 'Rural: Distant':'tan', 'Rural: Remote':'tan'}
plt.axhline(y=93, color='darkred', linestyle=':')
chart3 = sns.scatterplot(x='pct_freered', y='pct_MMR', data=kinder_merge, marker='.', palette=colordict)
chart3.set(title='Utah Kindergarten MMR Vaccination Rates', xlabel='% Students on Free/Reduced Lunch', ylabel='% of Students with MMR Vaccine')
plt.savefig('plot3.png', dpi=300, bbox_inches = "tight")


# In[9]:


#create boolean column stating whether the classroom is herd immune (pct_MMR >= 93)
kinder_merge['herd_immune'] = kinder_merge.pct_MMR >= 93

#create the bins for the bar chart, and create an empty dataframe
hist_bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
chart4_data= pd.DataFrame()

#populate dataframe with a for loop
for i in range(len(hist_bins)-1):
    chart4_data.loc[i, 'b_range'] = hist_bins[i]
    chart4_data.loc[i, 't_range'] = hist_bins[i + 1]
    chart4_data.loc[i, 'label'] = str(hist_bins[i])+'% to '+str(hist_bins[i+1])+'%'
    chart4_data.loc[i, 'count_herd_imm'] = kinder_merge[(kinder_merge.pct_freered >= hist_bins[i]) & (kinder_merge.pct_freered <= hist_bins[i + 1]) & (kinder_merge.herd_immune == True)].name_short.count()
    chart4_data.loc[i, 'count_total'] = kinder_merge[(kinder_merge.pct_freered >= hist_bins[i]) & (kinder_merge.pct_freered <= hist_bins[i + 1])].name_short.count()
    chart4_data.loc[i, 'pct_herd_imm'] = chart4_data.loc[i, 'count_herd_imm'] / chart4_data.loc[i, 'count_total'] * 100


# In[10]:


#create bar plot showing the percentage of classrooms in each bin that are herd immune
chart4=sns.barplot(x='label', y='pct_herd_imm', data= chart4_data, palette='GnBu_d')
chart4.set_xticklabels(chart4.get_xticklabels(), rotation=45, horizontalalignment='right')
chart4.set(title='Utah Kindergarten Measles Herd Immunity Levels', xlabel='% of Students on Free/Reduced Lunch', ylabel='% of Classrooms at Herd Immunity')
plt.savefig('plot4.png', dpi=300, bbox_inches = "tight")


# In[11]:


len(kinder_merge[kinder_merge['herd_immune']==True])/len(kinder_merge)


# In[ ]:




