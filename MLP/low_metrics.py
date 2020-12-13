from sklearn.metrics import average_precision_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import accuracy_score
import ast
import statistics 
import numpy as np
import pandas as pd 
import tensorflow as tf
import sys

y_true = []
y_pred = []

with open('MLP/reference_low.txt','r') as f, open('MLP/fcl_low_prediction.txt','r') as f2:
   
    for line,line2 in zip(f,f2):
        vect = line.replace('[','')
        vect= vect.replace(']','')
        vect= vect.split(',')
        found = False

        vect2 = line2.replace('[','')
        vect2= vect2.replace(']','')
        vect2= vect2.split(',')

       
        for i in range(len(vect)):
           # print(vect[i].strip())
            dictionary = ast.literal_eval(vect[i].strip())
            for key, value in dictionary.items():
               if(value == sys.argv[1]):
                   y_true.append(key)
                   found = True
        if(found):
            foundpred = False
            for i in range(len(vect2)):
                dictionary = ast.literal_eval(vect2[i].strip())
                for key, value in dictionary.items():
                    if(value == sys.argv[1]):
                       y_pred.append(key)
                       foundpred = True
            if(not foundpred):
                 y_pred.append(0)

label = np.unique(y_true)
#print(y_true)
#print(y_pred)
#print(sys.argv[1])

#print(label)
recall=recall_score(y_true, y_pred,label, average='macro')
print("The average recall %s "% recall)

#recall_array = recall_score(y_true, y_pred ,average=None)
#print(recall_array)
#print("the standard deviation of average recall %s " % (statistics.stdev(recall_array)))

precision = precision_score(y_true, y_pred,label, average='macro')
print("The average precision %s " % precision)

#precision_array = precision_score(y_true, y_pred, average=None)
#print(precision_array)
#print("the standard deviation of average precision %s " % (statistics.stdev(precision_array)))

#accurancy = accuracy_score(y_true, y_pred)
#print("The accurancy score %s " % accurancy)


