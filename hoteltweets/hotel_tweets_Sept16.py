#!/usr/bin/env python

from TwitterAPI import TwitterAPI
import time

from twitter_config_hwh import *

file_location = "output_follow.txt"


#-----------------------------------------------------------------------
# Create a term list - formatted as a dict, then a reverse dict (for later categorization), then flattened to a string of terms
# Not all steps strictly required here - will repeat in the processing file later
termlist = dict()
termlist['hilton'] = ['HiltonHotels', 'HiltonHHonors', 'HiltonWorldwide', 'Hilton']
termlist['marriott'] = ['Marriott', 'Mariott', 'Marriot', 'MarriottIntl']
termlist['starwood'] = ['sheraton', 'spg','starwood']

termlookup = {}
for ii in termlist.keys():
    for jj in termlist[ii]:
        termlookup[jj.lower()] = ii.lower()    # make sure whole dict is lower for searching

term_string = ", ".join(termlookup.keys())
FOLLOW_TERM = term_string    # Creates string for Twitter monitor - check: does case matter?
FOLLOW_list = FOLLOW_TERM.split()


#FOLLOW_TERM = "marriot, marriottintl, hiltonhhonors, mariott, hiltonworldwide, sheraton, hilton, starwood, marriott, spg, hiltonhotels"

#-------------------------------------------------------------
# Start the streaming capture

delay = 8 # seconds

while True:
    try:
        api = TwitterAPI(consumer_key, consumer_secret,
                         access_token_key, access_token_secret)
        r = api.request('statuses/filter', {'track':FOLLOW_TERM})
        with open(file_location, "a") as output:
            for item in r.get_iterator():
                output.write(str(item) + "\n")
                print(item['text'] if 'text' in item else item)
            delay = max(8, delay/2)
    except:
        print "Error"
        print time.ctime()
        print "Waiting " + str(delay) + " seconds"
        time.sleep(delay)
        delay *= 2
