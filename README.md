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
- **How to Build Culture Through Office Design**
  *The only thing I like the most is the fact that the office is in the open floor, so the door is open and the floor would be open and if the doors closed, they could open and see how much room they are there.

It doesn't really matter, but I would be very happy to pay for my office space in my office for a couple of years. I'd be glad if I had a place where I could get in on that space. It'd be great to get in on that, though.

(Also, this article is from 2008. I was at a meeting where we went into the office with a bunch of engineers from a few companies in the open. They said "I'm the boss, you're the boss.")*

## Instructions
1. [data](data/): Prepare the data and extract title-comment pairs from the HN data dump.
2. [train](train/): Train a Transformer translation model on the title-comment pairs using
   [TensorFlow](https://www.tensorflow.org/) and [OpenNMT-tf](https://github.com/OpenNMT/OpenNMT-tf).
3. [serve](serve/): Serve the model with TensorFlow serving.
4. [ui](ui/): Host a web interface for querying the model.
