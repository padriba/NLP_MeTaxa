# NLP_MeTaxa
NLP-MeTaxa is a multilayer perceptron (MLP) classifier for taxonomic assignments, trained with DNA fragments represented by word2vec embeddings.
The NLP-MeTaxa was evaluated on three datasets used in the first CAMI challenge, where the complexity is gradually ascendant among them, from the low until the high complexity dataset.

# Installation
   ## Docker image
   Pull the docker image
   
   ```sh
     docker pull padriba/nlp_metaxa:latest
   ```
   To launch NLP_MeTaxa
   ```sh
      # /input/folder/ : input foder, contains fasta files
      # /output/folder/ : output folder
      # print_tree : Print the NCBI taxnomy tree
      #               0 : dont print
      #               1 : print it
      docker run -v $(/input/folder/):/src/input -v $(/output/folder/):/src/output -t padriba/nlp_metaxa python3       
      /src/get_Taxa.py $(/input/folder/) $(/output/folder/) $(print_tree)

   ```
   The output folder will contain __*.tsv__  and __*.tree__ files.
   
   For each fasta file NLP_MeTaxa creates a tab-separated file with the following headers (id	taxa_id	lineage)
   
   - id : the sequence id
   - taxa_id: taxonomic identifier
   - lineage: corresponding lineage track as a hierarchically sorted list of parent taxids
      
   If the user chooses to print the NCBI taxnomy tree, NLP_MeTaxa will create for each fasta file a taxonomy tree
     
  ## NLP Vectorization
  To get a word2vec embedding representation :
   
  ```sh
     # input_file : the file to vectozise
     python ./embedding/vectorisation.py $(input_file)
   ```
   The result will be found in ./embedding/vectorisation_results/
    
   
   
      
     
  ## Training MLP model
   - To train the MPL model for the three datasets
    
       ```sh
          python ./MLP/train_feedfroward.py
        ```
        Models and weights are saved as .json files and .h5 respectively
        
  ## Metrics by rank
  
  - To asses NLP-MeTaxa performance across the different NCBI taxonomic ranks 
    *  First we need to creat a prediction file for the three datasets:
       ```sh
          python ./MLP/low_creat_predection.py
          python ./MLP/medium_creat_predection.py
          python ./MLP/high_creat_predection.py
        ```
       A file named fcl_$level$_prediction.txt will be found in ./MLP/
       
    * Then we creat a refrecence file from the CAMI dataset across the three different level
    
        ```sh
          python ./MLP/low_creat_ref.py
          python ./MLP/medium_creat_ref.py
          python ./MLP/high_creat_ref.py
        ```
        
        A file named reference_$level$.txt will be found in ./MLP/
        
     * Finally, launch the metrics for the three datasets, the taxonomic rank (superkingdom, phylum, class, order, family, genus, species) we want to measure is passed as parameter.
        ```sh
          python ./MLP/low_metrics.py species
          python ./MLP/medium_metrics.py genus
          python ./MLP/high_metrics.py superkingdom
        ```
     
