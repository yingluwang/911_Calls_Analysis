# import pacakges
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

# read the data
df=pd.read_csv('911.csv')

# check the data set info, check the head
df.info()
df.head()

# top 5 zipcode/townships for 911 calls
df['zip'].value_counts().head(5)
df['twp'].value_counts().head(5)

# check the number of unique titles
df['title'].nunique()

# create another column called reason based on title column
df['Reason']=df['title'].apply(lambda r:r.split(':')[0] if any(x in r for x in ['EMS','Fire','Traffic']) else '')

# check the top reason
df['Reason'].value_counts()

# draw a bar chart for these reasons
sns.countplot(x=df['Reason'])

# convert the type of timeStamp column to DateTime
df['timeStamp']=pd.to_datetime(df['timeStamp'])

# create another three columns for 'Hour', 'Day of Week', 'Month'
df['Hour']=df['timeStamp'].apply(lambda t:t.hour)
df['Month']=df['timeStamp'].apply(lambda t:t.month)

dmap={0:'Mon',1:'Tue',2:'Wed',3:'Thu',4:'Fri',5:'Sat',6:'Sun'}
df['Day of Week']=df['timeStamp'].apply(lambda t:t.dayofweek).map(dmap)

# draw a bar chart based on Reason column
# compare the reasons reported by Month
ax=sns.countplot(df['Month'],hue=df['Reason'])
ax.set_ylim(0,8000)
ax.legend(loc='upper right',bbox_to_anchor=(1.27, 1.02))

# see missing months

byMonth=df.groupby('Month').count()
byMonth

# draw a line-plot for number of calls by Month
ax=byMonth['twp'].plot()
ax.set_ylim(7000,14000)
ax.set_xlim(1,12)

# draw a best-fit line for number of calls by Month
byMonth=byMonth.reset_index()

lm=sns.lmplot(x='Month',y='twp',data=byMonth)
axes=lm.axes
lmplot=axes[0,0].set_ylim(6000,15000)

# create a new DataFrame with  of Week as index anDayd Hour as column
new_df=df.set_index(['Day of Week','Hour']).groupby(['Day of Week','Hour']).count()['e'].unstack(level=-1)
new_df

# create a HeatMap using the new DataFrame
fig, ax= plt.subplots(figsize=(12,6))
sns.heatmap(new_df,cmap='rainbow')

# create a clusetermap using the new DataFrame
sns.clustermap(new_df,figsize=(12,6),cmap='PuBuGn')
