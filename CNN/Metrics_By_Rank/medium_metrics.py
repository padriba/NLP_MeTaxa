from sklearn.metrics import average_precision_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import accuracy_score
import ast
import statistics 

y_true = []
y_pred = []


with open('results/medium/reference.txt','r') as f:
   
    for line in f:
        vect = line.replace('[','')
        vect= vect.replace(']','')
        vect= vect.split(',')
        found = False
       
        for i in range(len(vect)):
           # print(vect[i].strip())
            dictionary = ast.literal_eval(vect[i].strip())
            for key, value in dictionary.items():
               if(value == sys.argv[1]):
                   y_true.append(key)
                   found = True
        if(not found):
            y_true.append(0)

       

with open('results/medium/cnn_prediction.txt','r') as f:
    
    for line in f:
        vect = line.replace('[','')
        vect= vect.replace(']','')
        vect= vect.split(',')
        found = False
       
        for i in range(len(vect)):
           # print(vect[i].strip())
            dictionary = ast.literal_eval(vect[i].strip())
            for key, value in dictionary.items():
               if(value == sys.argv[1]):
                   y_pred.append(key)
                   found = True

        if(not found):
            #print(line)
            y_pred.append(0)
            
#print(y_true)
#print(y_pred)

recall=recall_score(y_true, y_pred, average='macro')
print("The average recall %s "% recall)

recall_array = recall_score(y_true, y_pred, average=None)
print(recall_array)
print("the standard deviation of average recall %s " % (statistics.stdev(recall_array)))

precision = precision_score(y_true, y_pred, average='macro')
print("The average precision %s " % precision)

precision_array = precision_score(y_true, y_pred, average=None)
print(precision_array)
print("the standard deviation of average precision %s " % (statistics.stdev(precision_array)))

accurancy = accuracy_score(y_true, y_pred)
print("The accurancy score %s " % accurancy)
    
