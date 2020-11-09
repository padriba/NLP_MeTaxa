import pandas as pd
from ete3 import NCBITaxa
import csv
ncbi = NCBITaxa()



dataset = pd.read_csv('MLP/metagenomics_signatures_1-8_CAMI_low_mean.csv')


X = dataset.iloc[:, 1:101].values
y = dataset.iloc[:, 0].values

#with open('/home/brahim/Data_sets/nCami_low/gsa_mapping_index.binning',mode='r') as file:
#     reader = csv.reader(file)
#     mydict = {rows[0]:rows[1] for rows in reader}

print(len(y))
fileoutput = open('reference_low.txt','w+')
for i in range(len(y)):
    lineage = ncbi.get_lineage(y[i])
    result=[ncbi.get_rank([taxid]) for taxid in lineage]
    fileoutput.write(str(result))
    fileoutput.write('\n')
            
fileoutput.close()
