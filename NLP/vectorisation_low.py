import os
import numpy as np
import re
from dna2vec.multi_k_model import MultiKModel
from Bio import SeqIO

def Save_Csv_File(vector,tax_id):
    fileoutput = open(outputfile,'a+')
       #print(vector)
    resutl = ','.join(str(e) for e in vector)
    fileoutput.write(tax_id+','+resutl)
    fileoutput.write('\n')

def get_Taxonomy_ID(se_record_id):
   
     with open('Dataset/NLP_DataSet/low/gsa_mapping.csv','r') as f:
          for line in f:
              #print (line)
              if se_record_id in line.split(','):
                   #print(line.split(','))
                   return line.split(',')[1].replace('\n','')
    
     
    

    
folder = 'Dataset/NLP_DataSet/nseq_low'
filepath = 'NLP/dna2vec-1-8_high.w2v'
outputfile = 'NLP/vectorisation_results/low/metagenomicreadsigntaures_8_mers.csv'

#delete the output files if they exist
if os.path.exists(outputfile):
    os.remove(outputfile)




mk_model = MultiKModel(filepath)
files = os.listdir(folder)
sumvect = np.zeros((100,),dtype=int)
for filename in files:
    filepath = os.path.join(folder, filename)
    #with open(filepath) as f:
    
    for seq_record in SeqIO.parse(filepath, "fasta"):
         #f1 = f.readlines()
         print(seq_record.id)
         sequence=re.sub('[^GATC]',"",str(seq_record.seq.ungap(' ')).upper()) # to delete errors from fasta file
         #for line in f1:
             #if  not line.startswith('>'):
         sumvect = np.zeros((100,),dtype=int)
                 #print(line)
                 #write in file
         step = 8
         for i in range(0, len(sequence), step):
             #print('seq '+sequence[i: i + step])
             sumvect = np.sum([sumvect,mk_model.vector(sequence[i: i + step])],axis=0)  
            
         #fileoutput.write(str(sumvect.tolist()))
         taxonomy_id = get_Taxonomy_ID(seq_record.id)
         Save_Csv_File(sumvect,taxonomy_id)


                     

