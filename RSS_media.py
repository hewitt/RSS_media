#!/usr/bin/env python3
import feedparser
import datetime, calendar
import time
import os, sys

DESTINATION_DIR = './'

#
# get the subscription list of dates of podcasts that we've downloaded
#
try:
    logfile = open( './subscriptions.txt', 'r')
except IOError:
    print("ERROR: Subscriptions file is missing!")
    sys.exit()
# read the log file
log = logfile.readlines()
# we'll maintain a dictionary of last download dates for each feed URL
log_history = {}
for line in log:
    feed = line.split(',')[0].rstrip('\n')
    try:
        txt_date = line.split(',')[1].rstrip('\n')
        # convert from the txt date representation to a
        #datetime object for later date comparisons
        log_history[ feed ] = datetime.datetime( *time.strptime( txt_date, "%d/%m/%y %H:%M" )[0:5] )
    except:
        # fill in missing dates with current datetime
        log_history[ feed ] = datetime.datetime.now()
        
# step through each feed in our subscription list
for feed, date in log_history.items():
    # a bit of sanity checking to the stdout
    print("Examining feed : " + feed)
    print("   last download was dated : " + date.strftime( "%d/%m/%y %H:%M" ))
    # parse the feed
    try:
        #print "Parsing the feed."
        parsed_feed = feedparser.parse( feed )
        # print parsed_feed
        # step through each entry in the feed
        for entry in parsed_feed['entries']:
            # get the date associated with each entry in the feed
            itemdate = datetime.datetime.utcfromtimestamp(calendar.timegm( entry.updated_parsed ))
            # yes ... some feeds date items including the seconds, so we'll fudge it and
            # only have an accuracy of +/- 1 minute
            delta = datetime.timedelta( minutes = 1 )
            if itemdate > date + delta:
                print("   found an item in the feed with date : " + itemdate.strftime( "%d/%m/%y %H:%M" ))
                # only get the first enclosure for each feed
                url = entry.enclosures[0].href
                local_filename = url.split( '/' )[-1].split( '?' )[0]
                try:
                    os.system( 'curl -s -L ' + entry.enclosures[0].href.split( '?' )[0] + ' > ' + DESTINATION_DIR + local_filename )
                    print('    curl -s -L ' + entry.enclosures[0].href.split( '?' )[0] + ' > ' + DESTINATION_DIR + local_filename)
                except:
                    print("ERROR: there was a problem running the curl command!")

                print
                # we may have got multiple downloads from a single feed, so we only
                # want the latest one to be stored in the log_history dictionary
                if itemdate > date:
                    # we want to keep track of the MOST RECENT downloaded item
                    if ( itemdate > log_history[feed] + delta ):
                        log_history[ feed ] = itemdate
    except:
        print("ERROR: there was a problem parsing one of the feeds")

# update the subscriptions file with the new download times
try:
	logfile = open( './subscriptions.txt', 'w')
except IOError:
    print("Log file missing.")
    sys.exit()
for feed, date in log_history.items():
    logfile.write( feed + "," + date.strftime( "%d/%m/%y %H:%M\n" ) )
logfile.close()
