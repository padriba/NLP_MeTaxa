import random
import pandas as pd
import tensorflow as tf
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.model_selection import train_test_split
import sys
from sklearn.preprocessing import LabelEncoder








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







dataset = pd.read_csv("input/vectorisation_results.csv")
class_number = int(sys.argv[1])
bs= int(sys.argv[2])
ep= int(sys.argv[3])
#dataset_val = pd.read_csv('/bettik/matouguib/cami/fasta/results/metagenomics_signatures_1-8_CAMI_low_mean/output.csv')
#dataset_val = pd.read_csv('/bettik/matouguib/cami/fasta/results/metagenomics_signatures_1-8_CAMI_MED_mean/output.csv')
X = dataset.iloc[:,1:101].values
y = dataset.iloc[:,0].values
order =list(range(0,len(y)))
random.shuffle(order)
X = X[order,:]
y = y[order]
X = X.astype('float32')

encoder = LabelEncoder()
encoder.fit(y)
encoded_Y=encoder.transform(y)
y = tf.keras.utils.to_categorical(encoded_Y,class_number)


#X_val = dataset_val.iloc[:,1:101].values
#y_val = dataset_val.iloc[:,0].values
#order =list(range(0,len(y_val)))
#random.shuffle(order)
#X_val = X_val[order,:]
#y_val = y_val[order]
#X_val = X_val.astype('float32')

#j = 700

model= tf.keras.models.Sequential()
model.add(tf.keras.layers.Dense(units=2000,use_bias=False,input_shape= (100,),activity_regularizer=tf.keras.regularizers.l2(0.001))) #50
model.add(tf.keras.layers.BatchNormalization())
model.add(tf.keras.layers.Activation("relu"))
model.add(tf.keras.layers.Dropout(0.4))

model.add(tf.keras.layers.Dense(units=2000,use_bias=False,activity_regularizer=tf.keras.regularizers.l2(0.001))) #50
model.add(tf.keras.layers.BatchNormalization())
model.add(tf.keras.layers.Activation("relu"))
model.add(tf.keras.layers.Dropout(0.4))

model.add(tf.keras.layers.Dense(units=class_number, activation='softmax')) #14879

optm = tf.keras.optimizers.Adam(learning_rate=0.0001, beta_1=0.9, beta_2=0.999, amsgrad=False)
model.compile(optimizer=optm,loss='categorical_crossentropy', metrics=['categorical_accuracy'])

#model = tf.keras.models.load_model('/src/output/model.h5',custom_objects={'precision':precision,'recall':recall})
model.fit(X,y,validation_split=0.33,batch_size=bs,epochs=ep,verbose=1)
model.save("output/model.h5")
print("Saved model to disk")
