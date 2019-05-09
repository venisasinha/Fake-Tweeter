# todo: scrape twiftter and put data in useful format
from twitterscraper.query import query_tweets_from_user
import re

"""
self.user = user.strip('\@')
self.fullname = fullname
self.id = id
self.url = urlw
self.timestamp = timestamp
self.text = text
self.replies = replies
self.retweets = retweets
self.likes = likes
self.html = html
"""


def get_tweets(user):
    """
    Scrape twitter to get tweets from user.
    """

    # Currently pulls 200. Can adjust number.
    list_of_tweets = query_tweets_from_user(user, 200)

    tweets = []

    # filter out retweets and direct quotations from other people
    for tweet in list_of_tweets:
        if tweet.user == user and "\u201c" not in tweet.text:
            # replace slanted apostrophes with normal ones
            tweets.append(re.sub(u"([‘’])", "'", tweet.text))

    return tweets
