# Train

## Data Preparation
See [../data](../data).

## Shuffle
```
paste ../data/data.train.bpe.{titles,comments} | shuf > data.train.bpe.shuf.titles-comments
cut -f1 < data.train.bpe.shuf.titles-comments > data.train.bpe.shuf.titles
cut -f2 < data.train.bpe.shuf.titles-comments > data.train.bpe.shuf.comments
```

## Vocabularies

## Train

## Evaluate
