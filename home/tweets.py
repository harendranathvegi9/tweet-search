import datetime
import csv
from django.conf import settings

from home.utils import *

class Tweets:
    DEFAULT_TIMEFRAME = 90
    DATE_FORMAT = "%Y-%m-%d %H:%M"
    TIMEDELTA_DEFAULT_TIMEFRAME = datetime.timedelta(days=DEFAULT_TIMEFRAME)

    def __init__(self, query, query_count, start, end, export=None):
        self.query = query
        self.query_count = query_count
        self.start = start
        self.end = end
        self.export = export
        self.data = self.get_data()

    def get_data(self):
        
        g = get_gnip(False)

        if (self.start < datetime.datetime.now() - self.TIMEDELTA_DEFAULT_TIMEFRAME) and (self.start + self.TIMEDELTA_DEFAULT_TIMEFRAME > self.end):
            end = self.start + self.TIMEDELTA_DEFAULT_TIMEFRAME
        query_nrt = self.query

        # scrub tweet display query for no retweets
        not_rt = "-(is:retweet)"
        if (not_rt not in query_nrt):
            query_nrt = query_nrt.replace("is:retweet", "")
            query_nrt = "%s %s" % (query_nrt, not_rt)

        print "%s (%s)" % (query_nrt, self.query_count)

        if self.query_count > 500:
            g.paged = True

        tweets = g.query_api(query_nrt, self.query_count, use_case="tweets", start=self.start.strftime(self.DATE_FORMAT), end=self.end.strftime(self.DATE_FORMAT))

        return tweets
