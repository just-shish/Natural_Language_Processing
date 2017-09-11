import nltk
import csv
from nltk import bigrams
from nltk.book import text1
import numpy as np
import pandas as pd
model= {}
mod = None
def dev_model():
    text = [x.lower() for x in text1]
    text = ['<s>']+text+['<\s>']
    bi = list(bigrams(text, pad_right=False, pad_left=False))
    uni = nltk.FreqDist(text)
    
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
    #print(uni['None'])
    '''for w1 in model:
        count = uni[str(w1)]#float(sum(model[w1].values()))
        for w2 in model[w1]:
            #print(w1,w2)
            model[w1][w2]=count
    '''
    print(len(uni))
    encode = {i:w[0] for i,w in enumerate(uni.most_common())}
    decode = {w[0]:i for i,w in enumerate(uni.most_common())}
    #print(encode[1],decode[encode[1]])
    mod = np.zeros(shape=(len(uni),len(uni)))
    for i in range(len(uni)):
        for j in range(len(uni)):
            if encode[i] not in model or encode[j] not in model[encode[i]]:
                mod[i][j]= 1/(len(uni)+uni[encode[i]])
            else:
                mod[i][j]=(model[encode[i]][encode[j]]+1)/(len(uni)+uni[encode[i]])
    data = [w[0] for w in uni.most_common()]
    df = pd.DataFrame(data=mod[:25,:25], index=data[:25], columns=data[:25])
    print(df[encode[1]])
    with open('probs.csv', 'w') as csvfile:
        df.to_csv(csvfile)
    print("Done")


dev_model() 
while True:
    one = input("1st word")
    two = input("2nd Word")
    print('Porb'+'is'+str(model[one][two]))

    
