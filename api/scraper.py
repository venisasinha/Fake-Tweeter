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
    list_of_tweets = query_tweets_from_user(user, 200)

    tweets = []

    for tweet in list_of_tweets:
        if tweet.user == user and "\u201c" not in tweet.text:
            tweets.append(re.sub(u"([‘’])", "'", tweet.text))

    return tweets
