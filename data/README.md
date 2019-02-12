# Data
This directory contains some simple tools for analyzing and transforming
the HN dump data.

## Steps
### Extract
Extract only the top-level comments from the raw HN data dump.
We ignore comments that are replies for now, since they would require additional modelling.
```
$ data/extract.py < 14m_hn_comments_sorted.json > top_level_hn_comments.tsv
```
I get 3330140 total comments. This script can probably be improved, since there are some comments
that it misses due to what it seems are inconsistent data layouts.

### Split
Split the data into train, test and dev.
```
$ data/split_train_dev_test.sh data < top_level_hn_comments.tsv
$ wc -l data.{train,dev,test}.tsv
   3326140 data.train.tsv
      2000 data.dev.tsv
      2000 data.test.tsv
   3330140 total
```

### Tokenize
(and split into separate files for aligned titles/comments)

### Learn BPE

### Apply BPE

## Format of the HN Data Dump
A brief look into the format of the raw HN data dump.

Each line is one JSON object. Each object has an ID, by which the lines are sorted.
This is the first line, representing a story, pretty-printed with `head -n1 14m_hn_comments_sorted.json | jq`:
```
{
  "body": {
    "kids": [
      487171,
      15,
      234509,
      454410,
      82729
    ],
    "descendants": 15,
    "url": "http://ycombinator.com",
    "title": "Y Combinator",
    "by": "pg",
    "score": 61,
    "time": 1160418111,
    "type": "story",
    "id": 1
  },
  "source": "firebase",
  "id": 1,
  "retrieved_at_ts": 1435938464
}
```

This is a comment:
```
{
  "body": {
    "kids": [
      455092
    ],
    "parent": 534,
    "text": "which ones are you thinking about? ",
    "id": 586,
    "time": 1172193356,
    "type": "comment",
    "by": "gustaf"
  },
  "source": "firebase",
  "id": 586,
  "retrieved_at_ts": 1435974128
}
```

