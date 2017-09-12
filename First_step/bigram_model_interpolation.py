import nltk
import csv
from nltk import bigrams
from nltk.book import text1
import numpy as np
import pandas as pd
model= {}
text = [x.lower() for x in text1]
#text = ['<s>']+text+['<\s>']
bi = list(bigrams(text, pad_right=False, pad_left=False))
uni = nltk.FreqDist(text)
length = len(text)
#print(uni)
for w1,w2 in bi:
    if w1 in model:
        if w2 in model[w1]:
            model[w1][w2]+=1
        else:
            model[w1][w2]=1
    else:
        model[w1] = {}
        model[w1][w2]=1
print(len(uni))
encode = {i:w[0] for i,w in enumerate(uni.most_common())}
decode = {w[0]:i for i,w in enumerate(uni.most_common())}
#print(encode[1],decode[encode[1]])
lamda = 0.9
mod = np.zeros(shape=(len(uni),len(uni)))
for i in range(len(uni)):
    for j in range(len(uni)):
        if encode[i] not in model or encode[j] not in model[encode[i]]:
            mod[i][j]= (1-lamda)*uni[encode[i]]/length
        else:
            mod[i][j]=lamda*(model[encode[i]][encode[j]])/(uni[encode[i]])+(1-lamda)*uni[encode[i]]/length

data = [w[0] for w in uni.most_common()]
df = pd.DataFrame(data=mod[:25,:25], index=data[:25], columns=data[:25])
print(df[encode[1]])
with open('probs.csv', 'w') as csvfile:
    df.to_csv(csvfile)
print("Done")
