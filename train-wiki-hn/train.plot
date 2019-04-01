load '../train/train.plot' 

plot '../train-wiki/model.step-trainlossavg10' t 'wikipedia train loss' w lines ls 3, \
     'model.step-trainlossavg10' t 'hn train loss' w lines ls 3 dt 4, \
     '../train-wiki/model.step-devloss' t 'wikipedia dev loss' w lines ls 2, \
     'model.step-devloss' t 'hn dev loss' w lines ls 2 dt 4
