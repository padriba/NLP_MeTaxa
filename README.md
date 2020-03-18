# NLP_MeTaxa
NLP-MeTaxa is a multilayer perceptron (MLP) classifier for taxonomic assignments, trained with DNA fragments represented by word2vec embeddings.
The NLP-MeTaxa was evaluated on three datasets used in the first CAMI challenge, where the complexity is gradually ascendant among them, from the low until the high complexity dataset.

# Evaluation
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
   
   For each fasta files NLP_MeTaxa creates a tab-separated file with the headers (id	taxa_id	lineage)
   
   - id : the sequence id
   - taxa_id: taxonomic identifier
   - lineage: corresponding lineage track as a hierarchically sorted list of parent taxids
      
   If the user chooses to print the NCBI taxnomy tree, NLP_MeTaxa will create for each fasta files a taxonomy tree
   
  - Because of the existence of large files stored using Git Large File Storage (GLFS), you need first to install LFS package       before cloning the project. For example for Linux based system :
    ```sh
      sudo apt-get install git-lfs
      git lfs install
      ```
  - Download NLP_MeTaxa by 
    ```sh
      git clone https://github.com/padriba/NLP_MeTaxa.git
      ```
   - Installation has been tested in Linux based system with Python 3.6.7.
  
  ## NLP Vectorization
  To get a word2vec embedding representation for the metagenomic sample:
   - For the low comlexity dataset:
   
      ```sh
        python ./NLP/vectorisation_low.py
      ```
     The result will be found in ./NLP/vectorisation_results/low/
    
   - For the medium comlexity dataset:
   
      ```sh
        python ./NLP/vectorisation_medium.py
      ```
     The result will be found in ./NLP/vectorisation_results/medium/
     
   - For the high comlexity dataset:
   
      ```sh
        python ./NLP/vectorisation_high.py
      ```
     The result will be found in ./NLP/vectorisation_results/high/
     
  ## Training CNN model
   - Data generated from the previous step are used to train the CNN mlodel
   - To train the CNN model for the three datasets
    
       ```sh
          python ./CNN/low_cnnKeras.py
          python ./CNN/medium_cnnKeras.py
          python ./CNN/high_cnnKeras.py
        ```
        Models and weights are saved as .json files and .h5 respectively
  ## Crossvalidation      
   - To launch a crossvalidation for the three datasets
   
       ```sh
          python ./CNN/low_crossvalidation.py
          python ./CNN/medium_crossvalidation.py
          python ./CNN/high_crossvalidation.py
        ```
  ## Metrics by rank
  
  - To asses NLP-MeTaxa performance across the different NCBI taxonomic ranks 
    *  First we need to creat a prediction file for the three datasets:
       ```sh
          python ./CNN/Metrics_By_Rank/low_creat_predection.py
          python ./CNN/Metrics_By_Rank/medium_creat_predection.py
          python ./CNN/Metrics_By_Rank/high_creat_predection.py
        ```
       A file named cnn_prediction.txt will be found in ./CNN/Metrics_By_Rank/results/
       
    * Then we creat a refrecence file from the CAMI dataset across the three different level
    
        ```sh
          python ./CNN/Metrics_By_Rank/low_creat_ref.py
          python ./CNN/Metrics_By_Rank/medium_creat_ref.py
          python ./CNN/Metrics_By_Rank/high_creat_ref.py
        ```
        
        A file named reference.txt will be found in ./CNN/Metrics_By_Rank/results/
        
     * Finally, launch the metrics for the three datasets, the taxonomic rank (superkingdom, phylum, class, order, family, genus, species) we want to measure is passed as parameter.
        ```sh
          python ./CNN/Metrics_By_Rank/low_metrics.py species
          python ./CNN/Metrics_By_Rank/medium_metrics.py genus
          python ./CNN/Metrics_By_Rank/high_metrics.py superkingdom
        ```
     
