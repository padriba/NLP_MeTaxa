import csv
import os
from Bio import SeqIO
import random
import sys
import numpy as np
import re
import datetime
import gensim
from gensim.models import word2vec



def get_random_str(main_str, substr_len):
    idx = random.randrange(0, len(main_str) - substr_len + 1)    # Randomly select an "idx" such that "idx + substr_len <= len(main_str)".
    return main_str[idx : (idx+substr_len)]



folder = 'input/'
files = os.listdir(folder)

dict_spec = {}

for filename in files:
  #if (j<=50000):
  #if(filename == 'GCF_900638825.1_E4438_hybrid_assembly_genomic.fna'):
    if(filename.split('.')[0] not in dict_spec):
         dict_spec[filename.split('.')[0]] = 1
    else:
        dict_spec[filename.split('.')[0]] += 1




outputfile = os.path.join('output','vectorisation_results.csv')

mk_model = gensim.models.KeyedVectors.load_word2vec_format('embedding/dna2vec_1-8_all.w2v', binary=False)
#mk_model = MultiKModel('embedding/dna2vec_1-8_all.w2v')



files = list()
for (dirpath, dirnames, filenames) in os.walk(folder):
      files += [os.path.join(dirpath, file) for file in filenames]


vectorized = dict()
corected_sequences = {}
results = {}

for file in files:
    #print(file)
     basename= os.path.basename(file) 
     if(dict_spec[basename.split('.')[0]]<1000):
        print(basename)
        co = 1000
        while co > 0 :
          #print(co)
          for seq_record in SeqIO.parse(file, "fasta"):
            if(co > 0):
              #if(seq_record.id in fastafiles_dict):
                #indice = fastafiles_dict[seq_record.id]
              #else:
                #indice = 0
                #fastafiles_dict[seq_record.id] = indice

              #rand,indice = getrandom(len(seq_record.seq),indice)
              #fastafiles_dict[seq_record.id] = indice
              if(seq_record.id in corected_sequences):
                  full_sequence = corected_sequences[seq_record.id]
              else:
                  full_sequence = re.sub('[^GATC]',"",str(seq_record.seq.ungap(' ')).upper()) 
                  corected_sequences[seq_record.id] = full_sequence

              if(len(full_sequence)>= 60000):
                    rand = random.randrange(10000, 60000)
              elif (len(full_sequence)>= 1000):
                   rand = random.randrange(999,len(full_sequence))
              else:
                   continue
              sequence_segment = get_random_str(full_sequence,rand)
              #sequence=re.sub('[^GATC]',"",str(sequence_segment.ungap(' ')).upper())
              sumvect = np.zeros((100,),dtype=int)
              kmer = 8
              step = 1
              word_co = 0
              for i in range(0, len(sequence_segment)-8+1, step):
                 v = vectorized.get(sequence_segment[i:i+kmer],None)
                 if v is None:
                    v= mk_model[sequence_segment[i: i + kmer]]
                    vectorized[sequence_segment[i:i+kmer]] = v
                 sumvect = np.sum([sumvect,v],axis=0)
                 word_co += 1
              sumvect = sumvect/word_co
              if(basename.split('.')[0] in results):
                 results[basename.split('.')[0]].append(sumvect)
              else:
                 results[basename.split('.')[0]] = [sumvect]

              co -= 1

            else:
              break
     else:
        print('###################################################### ',basename)
        for seq_record in SeqIO.parse(file, "fasta"):
              full_sequence = re.sub('[^GATC]',"",str(seq_record.seq.ungap(' ')).upper())    
              if(len(full_sequence)>= 60000):
                    rand = random.randrange(10000, 60000)
              elif (len(full_sequence)>= 1000):
                   rand = random.randrange(999,len(full_sequence))
              else:
                   #print('no sequence found for: ',basename)
                   continue
              sequence_segment = get_random_str(full_sequence,rand)
              #sequence=re.sub('[^GATC]',"",str(sequence_segment.ungap(' ')).upper())
              sumvect = np.zeros((100,),dtype=int)
              kmer = 8
              step = 1
              word_co = 0
              for i in range(0, len(sequence_segment)-8+1, step):
                 v = vectorized.get(sequence_segment[i:i+kmer],None)
                 if v is None:
                    v= mk_model[sequence_segment[i: i + kmer]]
                    vectorized[sequence_segment[i:i+kmer]] = v
                 sumvect = np.sum([sumvect,v],axis=0)
                 word_co += 1
              sumvect = sumvect/word_co
              if(basename.split('.')[0] in results):
                 results[basename.split('.')[0]].append(sumvect)
              else:
                 results[basename.split('.')[0]] = [sumvect]

         

print('save')
fileoutput = open(outputfile,'w')
for taxa_id in results:
    for i in range(0,len(results[taxa_id])):
        delimiter = ','.join(str(e) for e in results[taxa_id][i])
        fileoutput.write(taxa_id+','+delimiter)
        fileoutput.write('\n')
fileoutput.flush()
fileoutput.close()
print('end save')
