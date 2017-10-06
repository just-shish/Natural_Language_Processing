from nltk.tag.stanford import StanfordPOSTagger
import csv
import sklearn as sk
import pandas as pd

import tensorflow as tf

import numpy as np

english_postagger = StanfordPOSTagger(
    'C:/Users/ashis/Downloads/stanford-postagger-2014-08-27/models/english-bidirectional-distsim.tagger',
    'C:/Users/ashis/Downloads/stanford-postagger-2014-08-27/stanford-postagger.jar'
    )



tag_code = [1] # Tag numeric value counter

L = 15 #Constant no. of features
encoder = {} #Encoder dict for encoding tags to numeric value

def generate_num_features(tagged_input): # Function to generate features
    res=[]
    tags=[]
    for x,y in tagged_input:
        if y not in encoder:
            encoder[y]=tag_code[0]
            tag_code[0]+=1
        res.append(encoder[y])
        tags.append(y)
    return res + [0]*(L-len(res)),tags+['']*(L-len(res))

lab_encode = {'N':0,'R':1,'L':2} #dict to convert classes to one hot vector

def oneHotVector(label): # fucntion to convert labels to one hot vector
    res = [0.0]*3
    res[lab_encode[label]] = 1.0
    return res

#Load input file as dataframe
df = pd.read_csv('DialogueActs_Homework2.csv')  
print("Input File Loaded")

#Convert the sentence to tags and tags to numeric values
temp_df = df.apply(lambda r: generate_num_features(english_postagger.tag(r.sentence.split())),axis=1)
print("Features Generated")

#rename to remove space in label names for use
df = df.rename(columns={'annotator one':'annotator_one','annotator two':'annotator_two'})

Feat_df = pd.DataFrame(temp_df)
Feat_df[['num', 'feature']] = Feat_df[0].apply(pd.Series)

#Generate File with Numeric Features
Num_df = Feat_df['num'].apply(pd.Series)
Num_df['sentence'] = df['sentence']
Num_df['Labels'] = df['annotator_one']
with open('Num_Features.csv', 'w') as csvfile:
        Num_df.to_csv(csvfile)

#Generate File with Tagged Features
F_df = Feat_df['feature'].apply(pd.Series)
F_df['sentence'] = df['sentence']
F_df['Labels'] = df['annotator_one']
with open('Features.csv', 'w') as csvfile:
        F_df.to_csv(csvfile)
print("Features File Saved")

#one hot vector conversion
new_lab = df.apply(lambda r: oneHotVector(r.annotator_one),axis=1)

print("Data:"+str(Feat_df.shape) + " " + "Labels:" + str(new_lab.shape))

#convert both into numpy matrix for furthur calculation
data = np.matrix(Feat_df['num'].tolist()).astype(np.float32)

temp_lab =np.matrix(new_lab).astype(np.float32)
labels = np.squeeze(np.asarray(temp_lab))

#normalizing data for better results
data = data/len(encoder)

Train_X = data[:80]
Train_Y = labels[:80]

Valid_X = data[80:]
Valid_Y = labels[80:]
print("Data Prepared")

#Define a Tensorflow Graph
graph = tf.Graph()
with graph.as_default():
    #Constants
    tf_train_dataset  = tf.constant(Train_X)
    tf_train_labels = tf.constant(Train_Y)
    tf_valid_dataset = tf.constant(Valid_X)
    
    #Weights and Biases
    weights = tf.Variable(tf.truncated_normal([L,3]))
    biases = tf.Variable(tf.zeros([3]))
    
    logits = tf.matmul(tf_train_dataset,weights) + biases
    loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=tf_train_labels,logits = logits))
    
    optimizer = tf.train.GradientDescentOptimizer(0.5).minimize(loss)
    
    train_prediction = tf.nn.softmax(logits)
    valid_prediction = tf.nn.softmax(tf.matmul(tf_valid_dataset,weights) + biases)

#For accuracy calculations
def accuracy(prediction, labels):
     return (100.0 * np.sum(np.argmax(prediction,1)==np.argmax(labels,1))/ prediction.shape[0])

#Num of Iterations for Gradient Descent
num_steps=1000

#Define and start a Tensorflow Session
with tf.Session(graph=graph) as session:
    tf.global_variables_initializer().run()
    print('Graph Initialized')
    for step in range(num_steps):
        _,l_,predictions = session.run([optimizer,loss,train_prediction])
        if (step%100 == 0):
            print('Loss at step %d: %f' %(step, l_))
            print('Training accuracy is : %.1f%%' % accuracy(predictions,Train_Y))
            print('Validation accuracy is : %.1f%%' % accuracy(valid_prediction.eval(),Valid_Y))

print("Completed")



