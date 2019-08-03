import os
from Bio import SeqIO
from keras.models import model_from_json
import keras
from keras.models import Sequential
from keras.layers import *
import re
import sys
#sys.path.append('../NLP/dna2vec/multi_k_model')
sys.path.insert(1, '../NLP/dna2vec/')
from multi_k_model import MultiKModel
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from keras.utils import np_utils
from ete3 import NCBITaxa





inputfile = 'input.fasta'
filepath = '../NLP/dna2vec-1-8_high.w2v'
outputfile = 'output.txt'
output_tree = 'tree.txt'
ncbi = NCBITaxa()
tax_id_lst = []


dataset = pd.read_csv('../NLP/vectorisation_results/high/metagenomicreadsigntaures_8_mers.csv')
y = dataset.iloc[:, 0].values
encoder = LabelEncoder( )
encoder.fit(y)

#delete the output files if they exist
if os.path.exists(outputfile):
    os.remove(outputfile)
    
if os.path.exists(output_tree):
    os.remove(output_tree)

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


# load json and create model
json_file = open('../CNN/high_cnn_template.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights("../CNN/high_cnn_template.h5")
print("Loaded model from disk")
loaded_model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy',precision, recall,fbeta_score])

#NLP vectorization
mk_model = MultiKModel(filepath)

for seq_record in SeqIO.parse(inputfile, "fasta"):
    sequence=re.sub('[^GATC]',"",str(seq_record.seq.ungap(' ')).upper()) # to delete errors from fasta file
    sumvect = np.zeros((100,),dtype=int)
    step = 8
    for i in range(0, len(sequence), step):
        sumvect = np.sum([sumvect,mk_model.vector(sequence[i: i + step])],axis=0)  

    #Taxnomic class prediction
    X = sumvect.reshape(1,10,10,1)  
    y_results = loaded_model.predict_classes(X)
    y_results = encoder.inverse_transform(y_results)

    #save results
    output = open(outputfile,'a+')
    output.write(str(seq_record.id))
    output.write('\t')
    for i in range(len(y_results)):
        lineage = ncbi.get_lineage(y_results[i])
        result=[ncbi.get_rank([taxid]) for taxid in lineage]
        output.write(str(result))
        output.write('\n')
        tax_id_lst.append(y_results[i])
output.close()

#save NCBI taxonomy tree
output = open(output_tree,'w')
tree = ncbi.get_topology(tax_id_lst)
output.write(tree.get_ascii(attributes=["sci_name", "rank"]))
output.close()
    
    
