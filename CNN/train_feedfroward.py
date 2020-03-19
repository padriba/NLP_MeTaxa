import random
import pandas as pd
import tensorflow as tf
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.model_selection import train_test_split



class CustomSaver(tf.keras.callbacks.Callback):
   def on_epoch_end(self, epoch, logs={}):
            if(epoch % 10 == 0):
                model_json = self.model.to_json()
                with open("model_{}.json".format(epoch), "w") as json_file:
                  json_file.write(model_json)
                self.model.save_weights("model_weights_{}.h5".format(epoch))
                self.model.save("model_{}.h5".format(epoch))
                print("Saved model to disk")





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







dataset = pd.read_csv('/bettik/matouguib/vectorisation_results/new/reseq_mean_all/reseq_mean_all_l.csv')
#dataset_val = pd.read_csv('/bettik/matouguib/cami/fasta/results/metagenomics_signatures_1-8_CAMI_low_mean/output.csv')
dataset_val = pd.read_csv('/bettik/matouguib/cami/fasta/results/metagenomics_signatures_1-8_CAMI_MED_mean/output.csv')
X = dataset.iloc[:,1:101].values
y = dataset.iloc[:,0].values
order =list(range(0,len(y)))
random.shuffle(order)
X = X[order,:]
y = y[order]
X = X.astype('float32')
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)


X_val = dataset_val.iloc[:,1:101].values
y_val = dataset_val.iloc[:,0].values
order =list(range(0,len(y_val)))
random.shuffle(order)
X_val = X_val[order,:]
y_val = y_val[order]
X_val = X_val.astype('float32')

model= tf.keras.models.Sequential()
model.add(tf.keras.layers.Dense(units=2000,use_bias=False,input_shape= (100,),activity_regularizer=tf.keras.regularizers.l2(0.001))) #50
model.add(tf.keras.layers.BatchNormalization())
model.add(tf.keras.layers.Activation("relu"))
model.add(tf.keras.layers.Dropout(0.4))

model.add(tf.keras.layers.Dense(units=2000,use_bias=False,activity_regularizer=tf.keras.regularizers.l2(0.001))) #50
model.add(tf.keras.layers.BatchNormalization())
model.add(tf.keras.layers.Activation("relu"))
model.add(tf.keras.layers.Dropout(0.4))

model.add(tf.keras.layers.Dense(units=14879, activation='softmax')) #14879

optm = tf.keras.optimizers.Adam(learning_rate=0.0001, beta_1=0.9, beta_2=0.999, amsgrad=False)
model.compile(optimizer=optm,loss='sparse_categorical_crossentropy', metrics=['sparse_categorical_accuracy'])
saver = CustomSaver()

model.fit(X_train,y_train,validation_data=(X_test,y_test),callbacks=[saver],batch_size=10000,epochs=10000,verbose=1)
