# -*- coding: utf-8 -*-
"""
Created on Sat Aug 13 09:30:35 2016

@author: Holly
"""

# get started
# cd '~/Users/Holly/learning2016/Projects/Hotel Tweets'
import pandas
import re
import json


#---------------------------------------------------------------------------
# Create list of terms - as both a list and as a comma separated string
''' Original logic to create the search list as a list
full_term_list = ["HiltonHotels", "HiltonHHonors", "HiltonWorldwide", "Hilton", "Marriott", "MarriottIntl", "RenHotels", "sheratonhotels", "spg", "westin", "whotels", "starwood", "starwoodbuzz", "ihgrewardsclub", "HolidayInn", "hotelindigo", "crowneplaza", "hyatttweets", "#TravelBrilliantly", "#BeAWeekender", "#spglife", "#RDiscover", "#DiscoverIHG", "#gotmysweaton", "#ineedthatbreak"]
term_string = ", ".join(full_term_list)
term_string
'''

FOLLOW_TERM = "HiltonHotels, HiltonHHonors, HiltonWorldwide, Hilton, Marriott, MarriottIntl, RenHotels, sheraton, sheratonhotels, starwood, spg, westin, whotels" 
FOLLOW_list = FOLLOW_TERM.split()

termlist = dict()
termlist['hilton'] = ['HiltonHotels', 'HiltonHHonors', 'HiltonWorldwide', 'Hilton']
termlist['marriott'] = ['Marriott', 'Mariott', 'Marriot', 'MarriottIntl']
termlist['starwood'] = ['sheraton', 'spg','starwood']

termlookup = {}
for ii in termlist.keys():
    for jj in termlist[ii]:
        termlookup[jj.lower()] = ii.lower()    # make sure whole dict is lower for searching

term_string = ", ".join(termlookup.keys())
FOLLOW_TERM = term_string    # check - does case matter for Twitter?


# TO DO - create a lookup table to map the follow list to key terms


#--------------------------------------------------------------------------
# To do - eventually want to create the tweet processing as a function
# But how will I make my function append to the many outputs I want
# and/or should 
def tweetproc(line, termlookup):    # inputs line as a dict
    #print(line.keys()) 
    #print(line['text'])
    tweet = dict()
    tweet['text'] = line.get('text')
    tweet['username'] = line.get('user').get('screen_name')
    tweet['userloc'] = line.get('user').get('location')
    tweet['tweetloc'] = line.get('geo')
    tweet['time'] = line.get('created_at')
    tweet['lang'] = line.get('lang')
    tweet['id'] = line.get('id')
    tweet['hashtags'] = line.get('entities').get('hashtags')
    
    brands = []
    #print line.get('text').lower()
    for ii in termlookup.keys():
        if line.get('text').lower().find(ii) >= 0:
            brands.append(ii)
    tweet['brands'] = brands
    
    # tweet['err'] = line.get('fake')
    return tweet
    
   
    
    
    

#--------------------------------------------------------------------------
# Open the file
filename = 'output_follow2Aug16.txt'
fp = open(filename)

tweets = dict()
errorlines = []
for ii in range(100000):
    try:
        line = fp.readline()
        line = eval(line) # and now the line is a dict
        out = tweetproc(line, termlookup)
        tweets[ii] = out
    except:
        errorlines.append(ii)
    
    
# instead of dict of dicts, can I convert directly to dataframe?
# or consider a sql structure? 


#------------------------------------------
# hashtag aggs - better way to do this with a dataframe structure?

hashtags = dict()
for key, tweet in tweets.items():
    tweethash = tweet.get('hashtags')
    type(tweethash)
    for ii in tweethash:
        #type(ii)
        #print ii.get('text')
        if ii.get('text') in hashtags.keys():
            hashtags[ii.get('text')] += 1
        else:
            hashtags[ii.get('text')] = 1

#print hashtags

from operator import itemgetter
for k, v in sorted(hashtags.items(), key=itemgetter(1), reverse=True)[0:10]:
    print k, v

    



    
    
    