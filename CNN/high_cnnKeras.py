import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import tensorflow as tf
from keras.utils import np_utils
from keras.utils import to_categorical
from sklearn.preprocessing import LabelEncoder
dataset = pd.read_csv('../NLP/vectorisation_results/high/metagenomicreadsigntaures_8_mers.csv')
X = dataset.iloc[:, 1:101].values
y = dataset.iloc[:, 0].values
encoder = LabelEncoder( )
encoder.fit(y)
encoded_Y=encoder.transform(y)
y = np_utils.to_categorical(encoded_Y) 
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X = sc.fit_transform(X)
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)
X_train = X_train.reshape(X_train.shape[0], 10, 10, 1)
X_test = X_test.reshape(X_test.shape[0], 10, 10, 1)
input_shape = (10, 10, 1)
X_train = X_train.astype('float32')
X_test = X_test.astype('float32')
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
model= Sequential()
model.add(Conv2D(32, kernel_size=5, padding="same",input_shape=(10, 10, 1), activation = 'relu'))
model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
model.add(Conv2D(64, kernel_size=3, padding="same", activation = 'relu'))
model.add(Conv2D(128, kernel_size=3, padding="same", activation = 'relu'))
model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
model.add(Conv2D(256, kernel_size=2, padding="valid", activation = 'relu'))
model.add(MaxPooling2D(pool_size=(1, 1), strides=(2, 2)))
model.add(Flatten())
model.add(Dense(units=608, activation='relu'  ))
model.add(Dropout(0.1))
model.add(Dense(units=608, activation='relu'  ))
model.add(Dropout(0.1))
model.add(Dense(units=608, activation='relu'  ))
model.add(Dropout(0.3))
model.add(Dense(304,activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy',precision, recall,fbeta_score])
model.fit(X_train,y_train,batch_size=10000,nb_epoch=3000)
model_json = model.to_json()
with open("high_cnn.json", "w") as json_file:
    json_file.write(model_json)
#Brahim added this line
model.save_weights("high_cnn.h5")
print("Saved model to disk")
#score = model.evalute(X_test,y_test,verbose=0)
