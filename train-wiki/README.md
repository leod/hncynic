# Wiki Train
Here, we train a model to predict Wikipedia article sections from the title.

When I trained a model on the Hacker News data (see [../train](../train)), I used an off-the-shelf Transformer translation model. In particular, the encoder and decoder had the same number of layers. In hindsight, this may not have been an ideal choice. For our task, intuitively, the decoder has a much more challenging task than the encoder, given that it has to generate long, cohesive text. Furthermore, compared to translation, we have less symmetry between encoding and decoding here, as there is no direct relation between input and output sequence lengths. In fact, it would probably be a good idea to simply encode the title into a fixed-size vector and drop the decoder-encoder attention. Alternatively, it would make sense to completely drop the title encoder, and instead train a pure language model on titles concatenated with the comments. This is for example done by the awesome [stackroboflow](https://stackroboflow.com) and OpenAI [recently used](https://openai.com/blog/better-language-models/) language models to perform well at NLP tasks without any task-specific training.

However, out of a mixture of laziness, curiosity and a lack of GPUs, I'll continue to use encoder-decoder models. To try to account for the asymmetry between titles and comments, I'll reduce the number of layers in the encoder and increase the size of the decoder. This OpenNMT model is defined in [my_transformer.py](my_transformer.py), using 3 encoder layers and 9 encoder layers (instead of 6 and 6 as in the default model). I have no idea yet if this is a good idea, but let's just go for it.

The steps are very similar to [training on HN data](../train) (other than some inconsistencies in the filenames...).

## Steps
### Data Preparation
See [../data-wiki](../data-wiki).

### Shuffle
```
paste ../data-wiki/train.pp.bpe.{titles,comments} | shuf > train.pp.bpe.shuf.titles-comments
cut -f1 < train.pp.bpe.shuf.titles-comments > train.pp.bpe.shuf.titles
cut -f2 < train.pp.bpe.shuf.titles-comments > train.pp.bpe.shuf.comments
```

## Vocabularies
```
onmt-build-vocab --save_vocab vocab.titles train.pp.bpe.shuf.titles
onmt-build-vocab --save_vocab vocab.comments train.pp.bpe.shuf.comments
```

## Train
See [opennmt_config.yml](opennmt_config.yml) for the OpenNMT config -- paths need to be adjusted.
I set the maximum sequence length to 512, which excludes 977865 (about 6%) of the 16593956 title-comment pairs (we could split these examples after 512 tokens instead, leave that for future work I guess).
