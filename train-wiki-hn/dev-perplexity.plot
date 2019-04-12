load '../train/train.plot' 

set yrange [:60]
set ylabel 'perplexity'

plot 'model.step-devperplexity' t 'hn dev perplexity' w lines ls 1, \
     'model-2.step-devperplexity' t 'hn dev perplexity 2' w lines ls 2, \
     'model-3.step-devperplexity' u ($1+197000):2 t 'hn dev perplexity 3' w lines ls 3
