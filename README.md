#RSS_media

A python script that

* takes a "subscriptions.txt" file of RSS feeds (and last-downloaded dates), such as

    http://downloads.bbc.co.uk/podcasts/radio4/fricomedy/rss.xml,20/02/21 12:00

* downloads associated enclosure media (e.g. mp3 files) dated later than the above dates (e.g. 20th Feb 2021)
* rewrites the "subscription.txt" with the current date

Useful if run as a cronjob to provide files to something like 'mpd'. 
