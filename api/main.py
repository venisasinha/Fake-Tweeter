from typing import DefaultDict

from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS

from markovchain import split_tweets, populate_transition_matrix, generate_tweets
from scraper import get_tweets

app = Flask(__name__)
CORS(app)

api = Api(app)


def make_word_cloud(words):
    stop_words = ["a", "able", "about", "across", "after", "all", "almost", "also", "am", "among", "an", "and", "any",
                  "are", "as",
                  "at", "be", "because", "been", "but", "by", "can", "cannot", "could", "dear", "did", "do", "does",
                  "either",
                  "else", "ever", "every", "for", "from", "get", "got", "had", "has", "have", "he", "her", "hers",
                  "him", "his",
                  "how", "however", "i", "if", "in", "into", "is", "it", "its", "just", "least", "let", "like",
                  "likely", "may",
                  "me", "might", "most", "must", "my", "neither", "no", "nor", "not", "of", "off", "often", "on",
                  "only", "or",
                  "other", "our", "own", "rather", "said", "say", "says", "she", "should", "since", "so", "some",
                  "than", "that",
                  "the", "their", "them", "then", "there", "these", "they", "this", "tis", "to", "too", "twas", "us",
                  "wants", "was",
                  "we", "were", "what", "when", "where", "which", "while", "who", "whom", "why", "will", "with",
                  "would", "yet",
                  "you", "your"]

    word_counts = DefaultDict(int)

    for word in words:
        if word.lower() not in stop_words:
            word_counts[word.lower()] += 1

    common_words = []

    for key, value in word_counts.items():
        if 2 < value < 15 and key != ".":
            common_words.append({"text": key, "weight": value})

    return common_words


class FakeTweets(Resource):
    def get(self, twitter_id):
        try:
            print("Getting tweets...")
            tweets = get_tweets(twitter_id)

            words, start_words, end_words = split_tweets(tweets)

            common_word_counts = make_word_cloud(words)

            print("Generating fake tweets...")
            t_mat = populate_transition_matrix(words)

            tweets = generate_tweets(t_mat, start_words, end_words)

            return {'tweets': tweets,
                    "word_counts": common_word_counts,
                    "num_tweets": words.count(".") + words.count("!") + words.count("?")}
        except:
            print("hooosdff")
            return {'tweets': ["No tweets found!"] * 15,
                    "word_counts": {},
                    "num_tweets": 0}


api.add_resource(FakeTweets, '/<string:twitter_id>')

if __name__ == '__main__':
    app.run(debug=True)
