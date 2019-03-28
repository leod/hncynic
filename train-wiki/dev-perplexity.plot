load '../train/train.plot' 

set yrange [:100]
set ylabel 'perplexity'
plot 'model.step-devperplexity' t 'dev perplexity' w lines ls 1
