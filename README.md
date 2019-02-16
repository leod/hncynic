# hncynic
The best Hacker News are written with a complete disregard for the linked article.
`hncynic` is an attempt at capturing this phenomenon by training a model to predict
Hacker News comments just from the submission title.

To do this, we train a [Transformer](http://jalammar.github.io/illustrated-transformer/)
translation model on title-comment pairs extracted from a Hacker News
[data dump](https://archive.org/details/14566367HackerNewsCommentsAndStoriesArchivedByGreyPanthersHacker).
Once the model is trained, we can then sample comments from the learned distribution.

## Examples

## Instructions
1. [data](data/): Prepare the data and extract title-comment pairs from the HN data dump.
2. [train](train/): Train a Transformer translation model on the title-comment pairs using
   [TensorFlow](https://www.tensorflow.org/) and [OpenNMT-tf](https://github.com/OpenNMT/OpenNMT-tf).
3. [serve](serve/): Serve the model with TensorFlow serving.
4. [ui](ui/): Host a web interface for querying the model.
