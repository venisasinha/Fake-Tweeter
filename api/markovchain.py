import random
from typing import DefaultDict

import pandas as pd
from numpy.random.mtrand import choice


def split_tweets(tweets):
    """
    Turn list of Tweets into flat list of words. Additionally, keep track of
    word counts and start/end words for future reference
    :param tweets: list of strings representing tweets
    :return: list of words from tweets, start words & probabilities, end words & probabilities
    """
    words = []
    start_words = DefaultDict(int)
    end_words = DefaultDict(int)
    word_counts = DefaultDict(int)

    for tweet in tweets:
        # Split space-seperated words into list
        split_tweet = tweet.split(" ")

        # iterate through each word
        for i, word in enumerate(split_tweet):

            # want to remove extraneous punctuation aside from twitter handles (@)
            if "@" not in word:
                # word = re.sub(r"[^\w\s]", "", word)
                pass
            # len(word) == 1 or isalpha(word[1:]) and

            # remove tweets that are images or direct links
            if "pic.twitter" not in word and "http" not in word:
                # add word to our list
                words.append(word)

                # increment count occurances of that word
                word_counts[word] += 1

                # if the first word in a tweet
                if i is 0:
                    start_words[word] += 1

                # if potentially last word in a tweet/sentence, add to posisble end words
                if len(word) > 1 and word[-1] in [".", "!", "?"]:
                    end_words[word] += 1

    # convert to normal dictionary so we dont accidentally create more keys
    end_words = dict(end_words)

    # hold the list of start words w/ weighting applied
    weighted_start_words = []

    # give higher-frequency words more chance to be picked by random choice function
    for key, value in start_words.items():
        weighted_start_words.extend([key] * value)

    # convert counts of end words to  P(end word | word)
    for key, value in end_words.items():
        end_words[key] = end_words[key] / word_counts[key]

    return words, weighted_start_words, end_words


def populate_transition_matrix(words):
    """
    Build markov model.
    :param words: list of all words in tweets (ordered)
    :return: transition matrix of probabilities
    """

    # create pandas dataframe
    dict_df = pd.DataFrame(columns=["first", "second", "count"])
    # all of the words
    dict_df["first"] = words
    # all of the words shifted backwards by 1 such that each word in a row was adjacent in original tweet
    dict_df["second"] = words[1:] + ["placeholderword"]

    # count number of each first/second pair and put into count column, then remove duplicates
    dict_df['count'] = dict_df.groupby(['first', 'second'])['first', 'second'].transform('count')
    dict_df = dict_df.drop_duplicates(inplace=False)

    # turn into matrix
    t_mat = dict_df.pivot(index="first", columns="second", values="count")
    # convert counts to probabilities
    s = t_mat.sum(axis=1)
    return t_mat.apply(lambda x: x / s)


def generate_tweets(t_mat, start_words, end_words, num_tweets=15):
    """
    Generate tweets based on markov model
    :param t_mat: transition matrix
    :param start_words: potential starting words
    :param end_words: potential ending words
    :param num_tweets: number of tweets you want to generate
    :return: list of generated tweets
    """
    tweets = []
    # ends, _ = end_words.items()

    for i in range(num_tweets):
        # choose random word based on weighted list of potential start words
        w = random.choice(start_words)

        # initialize tweet list with chosen word
        tweet = [w]

        # arbitrary length cap; 15 worked well for tweet length
        while len(tweet) < 15:

            # get random "next" word based on weighted probabilites in transition matrix
            w = choice(a=list(t_mat.columns), p=t_mat.iloc[t_mat.index == w].fillna(0).values[0])
            tweet.append(w)

            # if it's an end word, we might want to stop now
            if w in end_words:
                # if we have a reasonable number of words already, randomly choose to stop based on P(end word | word)
                if len(tweet) > 3 and random.randrange(100) / 100 < end_words[w]:
                    print(w)
                    # if so, then we are done with this tweet
                    break

        t = ""
        # turn from list to string
        for word in tweet:
            t += str(word) + " "

        # remove last space
        t = t[:-1]

        # if last character in tweet isn't already punctuation, add a period
        if t[-1] not in [".", "!", "?"]:
            t += "."

        # add to list of tweets and capitalize first letter if not already
        tweets.append(t.capitalize())

    return tweets
