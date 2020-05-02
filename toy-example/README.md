This is a toy example of using NLP_MeTaxa

- Pull the docker image
```
  docker pull padriba/nlp_metaxa:latest
```
- Clone the NLP_MeTaxa repository: ```git clone https://github.com/padriba/NLP_MeTaxa.git ``` in your home directory

  To print both the taxonomic assignment and the  NCBI Taxonomy Tree: 
  ```
   sudo docker run -v ~/NLP_MeTaxa/toy-example/input/:/src/input -v ~/NLP_MeTaxa/toy-example/output_tree/:/src/output -t    padriba/nlp_metaxa python3 /src/get_Taxa.py ~/NLP_MeTaxa/toy-example/input/ ~/NLP_MeTaxa/toy-example/output_tree/ 1
  ```
  The output folder ```output_tree ``` will contain ```example_taxa.tsv``` and ```example_taxa.tree``` files

- To print only the taxonomic assignment of sequences in input directory:
  ```
    sudo docker run -v ~/NLP_MeTaxa/toy-example/input/:/src/input -v ~/NLP_MeTaxa/toy-example/output_no_tree/:/src/output -t padriba/nlp_metaxa python3 /src/get_Taxa.py ~/NLP_MeTaxa/toy-example/input/ ~/NLP_MeTaxa/toy-example/output_no_tree/ 0
  ```
  The output folder ```output_no_tree``` will contain a file named ```example_taxa.tsv```
