# hncynic
The best Hacker News comments are written with a complete disregard for the linked article.
`hncynic` is an attempt at capturing this phenomenon by training a model to predict
Hacker News comments just from the submission title.

To do this, we throw title-comment pairs extracted from a Hacker News
[data dump](https://archive.org/details/14566367HackerNewsCommentsAndStoriesArchivedByGreyPanthersHacker)
at a [Transformer](http://jalammar.github.io/illustrated-transformer/) encoder-decoder model.
Once the model is trained, we can then sample comments from the learned distribution.

The generated comments are fun, but... quite bad. While the comments often manage to be related
to the title, the model tends to generate meaningless or contradictory sentences.
HN comments are pretty long, so it is my understanding that the 3M training examples
are not enough to train the model well.


## Examples
Here's a few examples generated from recent front-page titles:
- **Ask HN: Is it practical to create a software-controlled model rocket?**

  1. > I think this is a great idea. However if your project is going to have a lot of bugs and issues (or a lot of other problems), your solution will probably be to use a custom version of your system (that would be a bit of a nightmare).
     >
     > If the system is just a bit of a "problem" and the problem is fixed, you will probably end up with lots of bugs.
  
  2. > It seems the biggest challenge with the SpaceX is that the technology is not as mature as it seems.
     >
     > If you can build a small rocket in less than two hours, it can be very hard to build a small rocket. I have a feeling that it would be difficult.
     >
     > But if the project is small enough that the engineering team has a lot of experience, I would suggest getting a small space launch and getting a large enough space launch to be a real product and not a "real" project. 
     
- **Is it creepy when brands pester you on social media?**
  1. > I think this is the most ridiculous headline on the front page of HN right now. 
  2. > "If you are a woman, you should be able to get a job that's as attractive as you think."
     >
     > I can't think of any examples of this. I don't see any of the examples in this article, but it's an interesting example.      
     > 
     > "What if you're a woman?"-- Mark Twain 
  
- **How to Build Culture Through Office Design**
  1. > > "If you want to be more creative you need to work on your own."
     >
     > That's the point. You need to be creative and make sure you are the person you work with. And that's what most people do in the office. 
     
  2. > The only thing I like the most is the fact that the office is in the open floor, so the door is open and the floor would be open and if the doors closed, they could open and see how much room they are there.
     >
     > It doesn't really matter, but I would be very happy to pay for my office space in my office for a couple of years. I'd be glad if I had a place where I could get in on that space. It'd be great to get in on that, though.
     >
     > (Also, this article is from 2008. I was at a meeting where we went into the office with a bunch of engineers from a few companies in the open. They said "I'm the boss, you're the boss.")

If you want to get a better understanding of how bad the generated comments are, please look at
[examples/README.md](examples/README.md) for completely unfiltered samples.

## Instructions
1. [data](data/): Prepare the data and extract title-comment pairs from the HN data dump.
2. [train](train/): Train a Transformer translation model on the title-comment pairs using
   [TensorFlow](https://www.tensorflow.org/) and [OpenNMT-tf](https://github.com/OpenNMT/OpenNMT-tf).
3. [serve](serve/): Serve the model with TensorFlow serving.
4. [ui](ui/): Host a web interface for querying the model.

## Future Work
The generated comments are fun to look at, but definitely still quite derpy. For example,
many comments contradict themselves within just a few words. It is my understanding that
there is not enough training data to generate cohesive comments of this length. The model does
learn to produce long comments, but it does not know what to fill them with, so it often
resorts to e.g. making multiple (contradicting) trivial statements about some subject.
Also, when a title deviates from the usual Hacker News discussion topics, the generated comments
may ramble about some general topic that is completely irrelevant to the title. For example,
the first model I trained really likes to talk about ways of getting a job.

To address these issues, it would be nice to see what would happen by including additional 
training data from other domains, such as Reddit comments or Wikipedia articles. Another idea
would be to start from a pre-trained model such as [BERT](https://github.com/google-research/bert.git)
and continue training from there on the comment prediction task.

Other than that, it could be interesting to include comments that are replies in the training
data as well. This could for example be done by giving the parent comment to the encoder.
Not only would we be able to generate full comment pages, but we would also be using a larger
portion of the data.
