# hncynic
The best Hacker News are written with a complete disregard for the linked article.
`hncynic` is an attempt at capturing this phenomenon by training a model to predict
Hacker News comments just from the submission title.

To do this, we throw title-comment pairs extracted from a Hacker News
[data dump](https://archive.org/details/14566367HackerNewsCommentsAndStoriesArchivedByGreyPanthersHacker)
at a [Transformer](http://jalammar.github.io/illustrated-transformer/) translation model.
Once the model is trained, we can then sample comments from the learned distribution.

## Examples
Here's a few random examples generated from the current front-page titles:
- *How to Build Culture Through Office Design*
  _"The most effective design for an office is a flat design - not a design," Mr. Wright said.

  I think it's better than the most productive design for a office, but I think it's a very good design for a office with the same amount of design experience that a typical office worker is comfortable with.

  I've been working at home for about 10 years, and I'm not sure how I feel about that, but I've seen a number of companies that do design work. The one that works is a design firm that does design work for a company with a large number of engineers.

  The problem with this is that it has not changed anything at all. The problem is that they're just doing what they're doing. _

## Instructions
1. [data](data/): Prepare the data and extract title-comment pairs from the HN data dump.
2. [train](train/): Train a Transformer translation model on the title-comment pairs using
   [TensorFlow](https://www.tensorflow.org/) and [OpenNMT-tf](https://github.com/OpenNMT/OpenNMT-tf).
3. [serve](serve/): Serve the model with TensorFlow serving.
4. [ui](ui/): Host a web interface for querying the model.
