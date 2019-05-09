import random
from typing import DefaultDict

import pandas as pd
from numpy.random.mtrand import choice


def split_tweets(tweets):
    words = []
    start_words = DefaultDict(int)
    end_words = DefaultDict(int)
    word_counts = DefaultDict(int)

    # TODO: getting rid of e.g. world! for some reason
    for tweet in tweets:
        split_tweet = tweet.split(" ")
        for i, word in enumerate(split_tweet):
            if "@" not in word:
                # word = re.sub(r"[^\w\s]", "", word)
                pass
            # len(word) == 1 or isalpha(word[1:]) and
            if "pic.twitter" not in word and "http" not in word:
                words.append(word)
                word_counts[word] += 1

                if i is 0:
                    start_words[word] += 1

                if len(word) > 1 and word[-1] in [".", "!", "?"]:
                    end_words[word] += 1

    end_words = dict(end_words)

    weighted_start_words = []

    for key, value in start_words.items():
        weighted_start_words.extend([key] * value)

    for key, value in end_words.items():
        end_words[key] = end_words[key] / word_counts[key]

    return words, weighted_start_words, end_words


def populate_transition_matrix(words):
    dict_df = pd.DataFrame(columns=["first", "second", "count"])
    dict_df["first"] = words
    dict_df["second"] = words[1:] + ["theend"]

    # count number of each first/second pair and put into count column, then remove duplicates
    dict_df['count'] = dict_df.groupby(by=['first', 'second'])['first', 'second'].transform('count').copy()

    dict_df = dict_df.drop_duplicates(inplace=False)

    # turn into matrix
    t_mat = dict_df.pivot(index="first", columns="second", values="count")
    sums = t_mat.sum(axis=1)
    t_mat = t_mat.apply(lambda x: x / sums)

    return t_mat


def generate_tweets(t_mat, start_words, end_words, num_tweets=15):
    tweets = []
    # ends, _ = end_words.items()

    end_words["theend"] = 1

    for i in range(num_tweets):
        word = random.choice(start_words)

        tweet = [word]
        while len(tweet) < 15:
            next_word = choice(a=list(t_mat.columns), p=t_mat.iloc[t_mat.index == word].fillna(0).values[0])

            if next_word in end_words:
                if len(tweet) > 4 and random.randrange(100) / 100 < end_words[next_word]:
                    print(next_word)
                    if next_word != "endword":
                        tweet.append(next_word)
                    break
            else:
                tweet.append(next_word)

            word = next_word

        tweet = ' '.join(tweet)
        if tweet[-1] not in [".", "!", "?"]:
            tweet = tweet + "."
        tweet = tweet.capitalize()
        tweets.append(tweet)

    return tweets
