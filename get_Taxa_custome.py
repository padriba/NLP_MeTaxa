import sys
import os
import pandas as pd
from Bio import SeqIO
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder
import re
import numpy as np
from embedding.dna2vec.multi_k_model import MultiKModel
from ete3 import NCBITaxa
import csv
import time


start_time = time.time()
output_path = 'output/'
draw_tree = sys.argv[1]

def get_Taxonomy_IDs(y_results):
    taxonomy_ids = encoder.inverse_transform(y_results)

    return taxonomy_ids


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


dataset = pd.read_csv("vectorisation_results.csv")
y = dataset.iloc[:,0].values
encoder = LabelEncoder()
encoder.fit(y)
encoded_Y=encoder.transform(y)


os.environ["TF_XLA_FLAGS"] = "--tf_xla_auto_jit=2 --tf_xla_cpu_global_jit"
#file = 'model_cami_2700.h5'
#file = 'model_220.h5'
file = 'model.h5'
model = tf.keras.models.load_model(file,custom_objects={'precision':precision,'recall':recall})

mk_model = MultiKModel('embedding/dna2vec_1-8_all.w2v')
ncbi = NCBITaxa()




files = list()
for (dirpath, dirnames, filenames) in os.walk('input/'):
    files += [os.path.join(dirpath, file) for file in filenames]


print('Start processing.....')
for file in files:
    
    #print(file)
    basename= os.path.basename(file)
    print(basename)
    file_out_put = os.path.join(output_path,basename.split('.')[0])+'_taxa.tsv'
    file_exists = os.path.isfile(file_out_put)
    #delete the file exits
    if(file_exists):
       os.remove(file_out_put)
    tax_id_lst = []
    for seq_record in SeqIO.parse(file, "fasta"):
           #print(seq_record.id)
           full_sequence = re.sub('[^GATC]',"",str(seq_record.seq.ungap(' ')).upper()) 
           sumvect = np.zeros((100,),dtype=int)
           kmer = 8
           step = 1
           word_co = 0
           for i in range(0, len(full_sequence)-8+1, step):
                 sumvect = np.sum([sumvect,mk_model.vector(full_sequence[i: i + kmer])],axis=0)
                 word_co += 1
           sumvect = sumvect/word_co
           #predection
           X = np.array([sumvect])
           y_results = model.predict_classes(X)
           #y_results = encoder.inverse_transform(y_results)
            
           y_results = get_Taxonomy_IDs(y_results)

          #save results
           file_exists = os.path.isfile(file_out_put)
           with open(file_out_put,'a') as fop: 
              writer = csv.DictWriter(fop, delimiter='\t', lineterminator='\n',fieldnames=['id','taxa_id','lineage'])
              if not file_exists:
                  writer.writeheader()
           
              
              for i in range(len(y_results)):
                 lineage = ncbi.get_lineage(y_results[i])
                 result=[ncbi.get_rank([taxid]) for taxid in lineage]
              row = {}
              row['id']= seq_record.id
              row['taxa_id']= y_results
              row['lineage'] = str(result)
              writer.writerow(row)
              tax_id_lst.append(y_results[i])
              fop.close()


    print(tax_id_lst)
    #save NCBI taxonomy tree
    if(int(draw_tree) == 1):
        file_out_put_tree = os.path.join(output_path,basename.split('.')[0])+'_taxa.tree'
        output = open(file_out_put_tree,'w')
        tree = ncbi.get_topology(tax_id_lst) 
        output.write(tree.get_ascii(attributes=["sci_name", "rank"]))
        output.close()   
print('End processing.....')           
print("--- Processing time: %s seconds ---" % (time.time() - start_time))
