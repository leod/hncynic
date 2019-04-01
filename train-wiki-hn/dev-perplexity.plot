load '../train/train.plot' 

set yrange [:60]
set ylabel 'perplexity'

plot '../train-wiki/model.step-devperplexity' t 'wiki dev perplexity' w lines ls 2, \
     'model.step-devperplexity' t 'hn dev perplexity' w lines ls 2 dt '-' 
