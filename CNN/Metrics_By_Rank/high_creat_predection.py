import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import tensorflow as tf
from keras.utils import np_utils
from keras.utils import to_categorical
from sklearn.preprocessing import LabelEncoder
from keras.models import model_from_json

dataset = pd.read_csv('../NLP/vectorisation_results/high/metagenomicreadsigntaures_8_mers.csv')
X = dataset.iloc[:, 1:101].values
y = dataset.iloc[:, 0].values
encoder = LabelEncoder( )
encoder.fit(y)
encoded_Y=encoder.transform(y)
y = np_utils.to_categorical(encoded_Y)

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

sc = StandardScaler()
X = sc.fit_transform(X)
X = X.reshape(X.shape[0], 10, 10, 1)
input_shape = (10, 10, 1)

import keras
from keras.models import Sequential
from keras.layers import *

def precision(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
    precision = true_positives / (predicted_positives + K.epsilon())
    return precision


def recall(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    recall = true_positives / (possible_positives + K.epsilon())
    return recall


def fbeta_score(y_true, y_pred, beta=1):
    if beta < 0:
        raise ValueError('The lowest choosable beta is zero (only precision).')
    if K.sum(K.round(K.clip(y_true, 0, 1))) == 0:
        return 0

    p = precision(y_true, y_pred)
    r = recall(y_true, y_pred)
    bb = beta ** 2
    fbeta_score = (1 + bb) * (p * r) / (bb * p + r + K.epsilon())
    return fbeta_score


def fmeasure(y_true, y_pred):
    return fbeta_score(y_true, y_pred, beta=1)
# load json and create model
json_file = open('../high_cnn.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights("../high_cnn.h5")
print("Loaded model from disk")
loaded_model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy',precision, recall,fbeta_score])
score = loaded_model.evaluate(X, y, verbose=0)
print("%s: %.2f%%" % (loaded_model.metrics_names[1], score[1]*100))
print("%s: %.2f%%" % (loaded_model.metrics_names[2], score[2]*100))
print("%s: %.2f%%" % (loaded_model.metrics_names[3], score[3]*100))
print("%s: %.2f%%" % (loaded_model.metrics_names[4], score[4]*100))

df = pd.read_csv('../NLP/vectorisation_results/high/metagenomicreadsigntaures_8_mers.csv', header=None)
X = df.iloc[:, 1:101].values
y = df.iloc[:, 0].values
sc = StandardScaler()
X = sc.fit_transform(X)
x_to_pred = X.reshape(X.shape[0], 10, 10, 1)
print(len(x_to_pred))
y_results = loaded_model.predict_classes(x_to_pred)
print(len(y_results))
print(y_results)
#print(list(set(y_results)))
y_results = encoder.inverse_transform(y_results)
print(y_results)

##with open('/home/brahim/Data_sets/nCami_low/gsa_mapping_index.binning',mode='r') as file:
##     reader = csv.reader(file)
##     mydict = {rows[0]:rows[1] for rows in reader}
##     
from ete3 import NCBITaxa
ncbi = NCBITaxa()

fileoutput = open('results/high/cnn_prediction.txt','w+')
# show the inputs and predicted outputs
for i in range(len(y_results)):
	#print("X=%s, Predicted=%s" % (x_to_pred[i], y_results[i]))
	lineage = ncbi.get_lineage(y_results[i])
	
	result=[ncbi.get_rank([taxid]) for taxid in lineage]
	fileoutput.write(str(result))
	fileoutput.write('\n')
fileoutput.close()
	
        
#print(y_classes)



