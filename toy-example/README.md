This is a toy example of using NLP_MeTaxa

# launching a docker image

- Pull the docker image
```
  docker pull padriba/nlp_metaxa:latest
```
- Downolad the fasta file from this  [link](https://dl.dropbox.com/s/yfkrlns8qw9n788/example.fasta?dl=1)
- Create an ```input``` and ```output``` folders in your home directory, and copy ```example.fasta``` in the ```input``` folder

- To get both the taxonomic assignment and print the  NCBI Taxonomy Tree run the following command: 
  ```
   sudo docker run -v ~/input/:/src/input -v ~/output/:/src/output -t padriba/nlp_metaxa python3 /src/get_Taxa.py 1
  ```
  The output folder ```output ``` will contain ```example_taxa.tsv``` and ```example_taxa.tree``` files

- To get only the taxonomic assignment of sequences in input directory:
  ```
    sudo docker run -v ~/input/:/src/input -v ~/output/:/src/output -t padriba/nlp_metaxa python3 /src/get_Taxa.py 0
  ```
  The output folder ```output``` will contain a file named ```example_taxa.tsv```
  
  # launching NLP-MeTaxa from source
  
