import csv
import os
from Bio import SeqIO
import random
import sys
from dna2vec.multi_k_model import MultiKModel
import numpy as np
import re
import datetime






#cami_id = {}



def get_random_str(main_str, substr_len):
    idx = random.randrange(0, len(main_str) - substr_len + 1)    # Randomly select an "idx" such that "idx + substr_len <= len(main_str)".
    return main_str[idx : (idx+substr_len)]

def getrandom(seqlen,indice):
  #print("seqlen",seqlen)
  intervale = interval_dict[indice]
  if(seqlen > intervale[0] and seqlen > intervale[1]):
    indice +=1
    rand = random.randint(intervale[0],intervale[1])
    return rand,indice
  elif(seqlen >= intervale[0] and seqlen <= intervale[1]):
    indice = 0
    rand = random.randint(intervale[0],seqlen)
    return rand,indice
  else:
    indice = 0
    return getrandom(seqlen,indice)



#with open('/bettik/matouguib/cami/fasta/results/metagenomics_signatures_1-8_CAMI.csv') as file:
#    reader = csv.reader(file)
#    for row in reader:
#       cami_id[row[0]] = row[0]

#file.close()
#print(len(cami_id))

co = 3500
start = 20
step = 1000
indice = 0
##build iterval
interval_dict = {}
corected_sequences = {}
i=0
results = {}

#print("build iterval--> start")
#while co >= 0 :
#   endinterval = start + step
#   interval_dict[i] = [start,endinterval]
#   start = endinterval
#   co -= 1
#   i +=1

#print("build iterval--> end")

fastafiles_dict = {}
outputfile = 'vectorisation_results/vectorisation_results.csv'
#outputfile = 'metagenomics_signatures_1-8_CAMI_from_genome_means.csv'
mk_model = MultiKModel('dna2vec_1-8_all.w2v')


files = list()
for (dirpath, dirnames, filenames) in os.walk(sys.argv[1]):
    files += [os.path.join(dirpath, file) for file in filenames]
k = 1


for file in files:    
    #print(file)
    basename= os.path.basename(file)
    for seq_record in SeqIO.parse(file, "fasta"):
           print(seq_record.id)
           full_sequence = re.sub('[^GATC]',"",str(seq_record.seq.ungap(' ')).upper()) 
           sumvect = np.zeros((100,),dtype=int)
           kmer = 8
           step = 1
           word_co = 0
           for i in range(0, len(full_sequence)-8+1, step):
                 sumvect = np.sum([sumvect,mk_model.vector(full_sequence[i: i + kmer])],axis=0)
                 word_co += 1
           sumvect = sumvect/word_co
           if(seq_record.id in results):
                results[seq_record.id].append(sumvect)
           else:
                results[seq_record.id] = [sumvect]     
     
  

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
