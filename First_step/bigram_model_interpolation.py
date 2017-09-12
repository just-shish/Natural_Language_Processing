import nltk
from nltk import bigrams
from nltk.book import text1
import numpy as np
import pandas as pd
import csv

#Bigram Count and Unigram Count
model= {}
text = [x.lower() for x in text1]
bi = list(bigrams(text))
uni = nltk.FreqDist(text)
length = len(text)
for w1,w2 in bi:
    if w1 in model:
        if w2 in model[w1]:
            model[w1][w2]+=1
        else:
            model[w1][w2]=1
    else:
        model[w1] = {}
        model[w1][w2]=1

#Encode and Decode words to index for numpy array
encode = {i:w[0] for i,w in enumerate(uni.most_common())}
decode = {w[0]:i for i,w in enumerate(uni.most_common())}

#Lambda for smoothing using Interpolation(Jelinek-Mercer)
lamda = 0.9

#Smoothing Applied
mod = np.zeros(shape=(len(uni),len(uni)))
for i in range(len(uni)):
    for j in range(len(uni)):
        if encode[i] not in model or encode[j] not in model[encode[i]]:
            mod[i][j]= (1-lamda)*uni[encode[j]]/length
        else:
            mod[i][j]=lamda*(model[encode[i]][encode[j]])/(uni[encode[i]])+(1-lamda)*uni[encode[j]]/length

#Convert the numpy matrix to pandas dataframe
data = [w[0] for w in uni.most_common()]
df = pd.DataFrame(data=mod[:25,:25], index=data[:25], columns=data[:25])

#Write to File
with open('probs.csv', 'w') as csvfile:
    df.to_csv(csvfile)
print("Done")
