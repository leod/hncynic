#!/usr/bin/env python3

import sys
import json
import urllib
import html

import tweepy
from twitter import twitter_utils

HN_API_URL = 'https://hacker-news.firebaseio.com/v0/item/{}.json'
HNCYNIC_API_URL = 'https://hncynic.leod.org/gen?title={}'
MAX_TWEET_LEN = 280
TWEET_TBC = '…'

def get_hn_item_title(item_id):
  url = HN_API_URL.format(item_id)
  reply = json.load(urllib.request.urlopen(url))
  return reply['title']

def get_hncynic_comments_and_scores(title):
  url = HNCYNIC_API_URL.format(html.escape(title))
  return json.load(urllib.request.urlopen(url))

def score_comment(comment):
  score = 1

  if comment.endswith('@@'):
    score = 0

  return score

def best_hncynic_comment(comments_and_scores):
  assert len(comments_and_scores) > 0

  comments = [entry[0] for entry in comments_and_scores]
  return sorted(comments, key=score_comment)[-1]

def postprocess(comment):
  comment = comment.strip()
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
    
def tweet_text_for_comment(item_id, title, comment):
  return '"{}" @ https://news.ycombinator.com/item?id={}\n\n{}'.format(title, item_id, comment)

def send_tweet_thread(tweets, api):
  prev_id = None
  for tweet in tweets:
    status = api.update_status(tweet, in_reply_to_status_id=prev_id)
    prev_id = status.id

def generate_and_tweet(item_id, api):
  sys.stderr.write('Tweeting for item id: {}\n'.format(item_id))

  title = get_hn_item_title(item_id)
  sys.stderr.write('Received title: {}\n'.format(title))

  comments_and_scores = get_hncynic_comments_and_scores(title)
  sys.stderr.write('Generated comments: {}\n'.format(comments_and_scores))

  best_comment = best_hncynic_comment(comments_and_scores)
  sys.stderr.write('Best comment: {}\n'.format(best_comment))

  best_comment_pp = postprocess(best_comment)
  sys.stderr.write('Postprocessed: {}\n'.format(best_comment_pp))

  tweet_text = tweet_text_for_comment(item_id, title, best_comment_pp)
  sys.stderr.write('Tweet text: {}\n'.format(tweet_text))

  split_tweets = split_tweet(tweet_text)
  sys.stderr.write('Tweet thread: {}\n'.format(split_tweets))

  send_tweet_thread(split_tweets, api)
  sys.stderr.write('Done tweeting.\n')

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
  generate_and_tweet(20617325, api)

