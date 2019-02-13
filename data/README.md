# Data
This directory contains some simple tools for analyzing and transforming the HN dump data.

## Steps
### Extract
Here, we extract only the top-level comments from the raw HN data dump and convert to
simple TSV for the processing steps that will follow.
For now, we ignore comments that are replies, since they would require additional modelling.
```
$ data/extract.py < 14m_hn_comments_sorted.json > top_level_hn_comments.tsv
```
The script also converts from HTML to Markdown using [html2text](https://pypi.org/project/html2text/).
Note that the entries in the JSON seem to come from different sources, with multiple formats.
For example, some entries use double newlines to represent paragraphs, while others use the HTML `<p>`.
`extract.py` tries to normalize the data a bit, but it is likely that there will be some remaining
inconsistencies.

I get 3330140 extracted title-comment pairs, with the following statistics printed by `extract.py`:
```
stories:        2461338
comments/story: 4.73
comments:       11633297
top-level:      3331502 (28.6376%)
ignored:        0.1507%
invalid:        0.2189%
deleted:        2.8940%
```

Some of the title-comment pairs may be contained multiple times, let's deduplicate:
```
$ sort -u -t$'\t' -k 3,3 -k 4,4 top_level_hn_comments.tsv > top_level_hn_comments.dedupe.tsv
$ wc -l top_level_hn_comments.tsv top_level_hn_comments.dedupe.tsv
  3331158 top_level_hn_comments.tsv
  3322178 top_level_hn_comments.dedupe.tsv
```
Indeed, it looks like a few (8980) title-comment pairs are duplicates in my case.

### Split
Split the data into train, test and dev. This is just so that we can see how the model performs
on unseen data during training (dev) and after training (test).

We have to be a bit careful here so that we don't get the same title in both train and dev/test.
The TSV format isn't very well suited for this, so I've written a stupid script for sampling.
Sort by title, then sample into train/dev/test, allocating 0.1% for dev and test data each:
```
$ sort -t$'\t' -k3,3 top_level_hn_comments.dedupe.tsv \
      | data/sample_train_dev_test.py --train data.train.tsv \
                                      --dev data.dev.tsv 0.1 \
                                      --test data.test.tsv 0.1
```

### Tokenize
Next, we normalize the data further. First, we note that a large number of comments contains links.
As a result of the conversion to Markdown, there are different ways of specifying links,
which `normalize_links.sh` tries to reduce just to plain-text URLs. Then, the we tokenize the
titles and comments and split from TSV into separate files for parallel line-aligned titles/comments.
```
$ data/tokenize_tsv.sh data.train
$ data/tokenize_tsv.sh data.dev
$ data/tokenize_tsv.sh data.test
```

### Learn BPE
Take some subset of the training data for learning BPE:
```
$ cat <(shuf data.train.tok.comments | head -n 500000) <(shuf data.train.tok.titles | head -n 500000) > bpetrain
```

Use [subword-nmt](https://github.com/rsennrich/subword-nmt.git) to learn BPE segmentation:
```
$ subword-nmt learn-bpe -s 24000 < bpetrain > bpecodes
```

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

As explained somewhat in `extract.py`, there will be some deviations from this layout.
