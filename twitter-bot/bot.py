#!/usr/bin/env python3

import tweepy
from twitter import twitter_utils
import json
import urllib

HN_API_URL = 'https://hacker-news.firebaseio.com/v0/item/{}.json'
MAX_TWEET_LEN = 280
TWEET_TBC = '…'

def get_hn_item_title(item_id):
  url = HN_API_URL.format(item_id)
  reply = json.load(urllib.urlopen(url))
  return reply['title']

def postprocess(comment):
  comment = comment.trim()
  comment = comment.replace('x86 _ 64', 'x86_64') \
                   .replace(': (', ' :(') \
                   .replace(': )', ' :)') \
                   .replace(':(', ' :(') \
                   .replace(':)', ' :)') \
                   .replace('<NL> <NL>', '\n') \
                   .replace('<NL>', '\n') \
                   .replace('\\ -', '-') \
                   .replace('\\.', '.')
  return comment

def split_tweet(tweet, start_sep=TWEET_TBC, end_sep=TWEET_TBC):
  toks = tweet.split(' ')

  cur_tweet = ''
  prev_tok = None
  tweets = []
  for tok in toks:
    extended_tweet = cur_tweet
    if prev_tok is not None and prev_tok != '\n':
      extended_tweet += ' '
    extended_tweet += tok
    prev_tok = tok

    if twitter_utils.calc_expected_status_length(extended_tweet) + len(end_sep) > MAX_TWEET_LEN:
      tweets.append(cur_tweet + end_sep)
      cur_tweet = start_sep + tok
    else:
      cur_tweet = extended_tweet

  tweets.append(cur_tweet)
  return tweets
    
def comment_tweet(item_id, title, comment):
  return '"{}" (https://news.ycombinator.com/item?id={}\n{}'.format(title, item_id_comment)

if __name__ == '__main__':
  with open('status.json') as f:
    status = json.load(f)

  # Authenticate to Twitter
  auth = tweepy.OAuthHandler(status['consumer_key'], status['consumer_secret'])
  auth.set_access_token(status['access_key'], status['access_secret'])

  # Create API object
  api = tweepy.API(auth)
  api.verify_credentials()

  # Create a tweet
  print(api.update_status('Hello Tweepy'))

