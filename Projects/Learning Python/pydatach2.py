# -*- coding: utf-8 -*-
"""
Created on Sun Aug 21 15:31:02 2016

@author: Holly
"""

# cd '~/learning2016/pydata'
path = "ch02/usagov_bitly_data2012-03-16-1331923249.txt"
open(path).readline()

import json
records = [json.loads(line) for line in open(path)]  # creates a list of dicts


# Counting time zones in pure python
# time_zones = [rec['tz'] for rec in records]  # unhappy when tz does not exist
time_zones = [rec['tz'] for rec in records if 'tz' in rec.keys()]   # don't need the .keys()?
tzcount = {}
for ii in time_zones:
    if ii in tzcount:
        tzcount[ii]+=1
    else:
        tzcount[ii]=1
        
# OR. . . 
from collections import defaultdict
tzcount = defaultdict(int)
for ii in time_zones:
    tzcount[ii]+=1

# sorting dicts    
tzlist = [(count,tz) for tz,count in tzcount.items()]   # set up a list of tuples
tzlist.sort(reverse=True)   # will sort by the first item in tuple
tzlist[0:10]        

# OR. . .         
from operator import itemgetter
for k, v in sorted(tzcount.items(), key=itemgetter(1), reverse=True)[0:10]:
    print k, v

#-----------------------------------------------------

# To pandas!

from pandas import DataFrame, Series
import pandas as pd
import numpy as np

frame = DataFrame(records)
frame['tz'].value_counts()[0:10]  # automatically sorts

# fill N/A
clean_tz = frame['tz'].fillna('Missing')
# fill blanks
clean_tz[clean_tz == ''] = 'Unknown'

clean_tz.value_counts()[:10]   # now see the Missing values - where were these before?

clean_tz.value_counts()[:10].plot(kind = 'barh',rot=0)

#------------------------------------------------------

# Parsing agent strings in frame['a']

# accessing columns
# frame.a == frame['a'] # almost - different NA handling

# use .split to split string on spaces and keep just first entry
resultl = [x.split()[0] for x in frame.a.dropna()]  # makes it a list - why would I want a series?
results = Series(resultl)
results.value_counts()[:10]

# difference between notnull and dropna? - one is a boolean, one does something. . .
cframe = frame[frame.a.notnull()]  # drop everything where 'a' is a null
OS = np.where(cframe['a'].str.contains('Windows'), 'Windows', 'Not Windows')  # ndarray
# OS.value_counts()   # unhappy - this is a ndarray, not pd.series. . . 
by_tz_os = cframe.groupby(['tz',OS])
agg_counts = by_tz_os.size().unstack().fillna(0)  # a dataframe with counts of Windows and Not Windows

# sorting. . . 
indexer = agg_counts.sum(1).argsort()
count_sub = agg_counts.take(indexer)[-10:]
count_sub.plot(kind='barh', stacked = True)
norm_count = count_sub.div(count_sub.sum(1), axis=0)
norm_count.plot(kind = 'barh', stacked=True)
