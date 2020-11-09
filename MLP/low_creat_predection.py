import tensorflow as tf
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import random
import numpy as np
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
import csv
from ete3 import NCBITaxa






def precision(y_true, y_pred):
    true_positives = tf.keras.backend.sum(tf.keras.backend.round(tf.keras.backend.clip(y_true * y_pred, 0, 1)))
    predicted_positives = tf.keras.backend.sum(tf.keras.backend.round(tf.keras.backend.clip(y_pred, 0, 1)))
    precision = true_positives / (predicted_positives + tf.keras.backend.epsilon())
    return precision
def recall(y_true, y_pred):
    true_positives = tf.keras.backend.sum(tf.keras.backend.round(tf.keras.backend.clip(y_true * y_pred, 0, 1)))
    possible_positives = tf.keras.backend.sum(tf.keras.backend.round(tf.keras.backend.clip(y_true, 0, 1)))
    recall = true_positives / (possible_positives + tf.keras.backend.epsilon())
    return recall






dataset_val = pd.read_csv('MLP/metagenomics_signatures_1-8_CAMI_low_mean.csv')



X_val = dataset_val.iloc[:,1:101].values
y_val = dataset_val.iloc[:,0].values

#encoded_Y=encoder.transform(y_val)
#y_val = tf.keras.utils.to_categorical(encoded_Y,402)
X_val = X_val.astype('float32')

#file = 'model_cami_200.h5'
file = 'model_220.h5'
print(file)
#model = tf.keras.models.load_model(file)
model = tf.keras.models.load_model(file,custom_objects={'precision':precision,'recall':recall})
#scores= model.evaluate(X_val,y_val,verbose=1)
y_pred = model.predict_classes(X_val)

ncbi = NCBITaxa()


with open('MLP/mapping_reseq_mean_all') as file:
     reader = csv.reader(file)
     taxa_dict = {rows[1]:rows[0] for rows in reader}

print(len(y_pred))

fileoutput = open('MLP/fcl_low_prediction.txt','w+')
for i in range(len(y_pred)):
      lineage = ncbi.get_lineage(int(taxa_dict[str(y_pred[i])]))
      result=[ncbi.get_rank([taxid]) for taxid in lineage]
      fileoutput.write(str(result))
      fileoutput.write('\n')
   
fileoutput.close()

