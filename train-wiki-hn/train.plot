load '../train/train.plot' 

plot '../train-wiki/model.step-trainlossavg10' t 'wikipedia train loss' w lines ls 3, \
     'model.step-trainlossavg10' t 'hn train loss' w lines ls 3 dt 4
