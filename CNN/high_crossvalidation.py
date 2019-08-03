import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import tensorflow as tf
from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.model_selection import cross_val_score
from sklearn.datasets import make_classification
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
X = X.reshape(X.shape[0],10,10,1)
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
8963837

def fmeasure(y_true, y_pred):
    return fbeta_score(y_true, y_pred, beta=1)
def create_model():
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
  return model
neural_network = KerasClassifier(build_fn=create_model, 
                                 epochs=2500, 
                                 batch_size=10000, 
                                 verbose=0)
scores = cross_val_score(neural_network, X, y, cv=5)
print(scores)
