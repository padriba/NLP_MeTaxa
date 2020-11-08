# NLP-MeTaxa
NLP-MeTaxa is a multilayer perceptron (MLP) classifier for taxonomic assignments, trained with DNA fragments represented by word2vec embeddings.
The NLP-MeTaxa was evaluated on three datasets used in the first CAMI challenge, where the complexity is gradually ascendant among them, from the low until the high complexity dataset.
NLP-MeTaxa was trained on a large scale data from the NCBI RefSeq,more than 14,000 complete microbial genomes.
# Videos

The following videos show the main functions given by NLP-MeTaxa, tested in Windows, Linux and Mac environments. If you do not want to read the whole document you can simply watch  these videos.
- [Window environment](https://dl.dropbox.com/s/0ngkfnryijsyoo5/video_wind_very_last.mp4?dl=1)
- [Linux environment](https://dl.dropbox.com/s/95riudpatuygdst/video_linux_very_last.mp4?dl=1)
- [Mac OS environement](https://dl.dropbox.com/s/z5y3zpipeme65et/video_mac_very_last.mp4?dl=1)

# Installation
   ## Building from source
   1- Clone the ```NLP-MeTaxa``` repository: ```git clone https://github.com/padriba/NLP_MeTaxa.git``` \
   2- The required python version is ```3.6.9``` \
   3- Install Python dependencies: ```pip3 install -r requirements.txt```
   ## Docker image
   Pull the docker image
   
   ```sh
     docker pull padriba/nlp_metaxa:latest
   ```
   In the following, you find two commands, one for NLP_MeTaxa docker image and the other if you install NLP_MeTaxa from source.
   ## Taxonomic assignment
   
   To launch NLP-MeTaxa
   ```sh
      # /input/folder/ : input folder, contains fasta files
      # /output/folder/ : output folder
      # print_tree : Print the NCBI taxnomy tree
      #               0 : dont print
      #               1 : print it
docker run -v $(/input/folder/):/src/input -v $(/output/folder/):/src/output -t padriba/nlp_metaxa python3 /src/get_Taxa.py $(print_tree)

   ```
   ```sh
      cd NLP_MeTaxa
      mkdir input # the input folder, contains fasta files
      mkdir output # the output folder
      python3 get_Taxa.pyt $(print_tree) # print_tree : Print the NCBI taxnomy tree, 0 : dont print, 1 : print it
   ```
   
   The output folder will contain __*.tsv__  and __*.tree__ files.
   
   For each fasta file NLP-MeTaxa creates a tab-separated file with the following headers ``` id	taxa_id	lineage ```
   
   - id : the sequence id
   - taxa_id: taxonomic identifier
   - lineage: corresponding lineage track as a hierarchically sorted list of parent taxids
      
   If the user chooses to print the NCBI taxnomy tree, NLP-MeTaxa will create for each fasta file a taxonomy tree
     
  ## NLP Vectorization
  To get a word2vec embedding representation :
   
  ```sh
      # /input/folder/ : input foder, contains fasta files
      # /output/folder/ : output folder

      docker run -v $(/input/folder/):/src/input -v $(/output/folder/):/src/output -t padriba/nlp_metaxa python3 /src/vectorisation.py
   ```
   ```sh
      cd NLP_MeTaxa
      mkdir input # the input folder, contains fasta files
      mkdir output # the output folder
      python3 vectorisation.py
   ```
   
   The fasta files in the input directory must respect the following naming policy : Taxonomy_id.****.fna(fasta).
   This is because the vectorization result is going to be used to train the model, and we need labeled data.\
   The output folder will contain a file named ```vectorisation_results.csv```.

   
   
      
     
  ## Training a new MLP model
   - To train a new MPL model
    
       ```sh
         # /input/folder/vectorisation_resuls.csv : is the embedding CSV file created in the previous step
         # /output/folder/: the output folder
         # class number : the class number in the embedding CSV file
         # batch size
         # epochs
         
          docker run -v $(/input/folder/vectorisation_resuls.csv):/src/input/vectorisation_results.csv -v $(/output/folder/):/src/output -t padriba/nlp_metaxa python3  /src/train_feedforward.py $(class number) $(batch size) $(epochs)
        ```
      ```sh
         cd NLP_MeTaxa
         mkdir input # the input folder, copy in this folder vectorisation_resuls.csv, which is the embedding CSV file created in the previous step
         mkdir output # the output folder
         python3 train_feedforward.py $(class number) $(batch size) $(epochs) # class number : the class number in the embedding CSV file   
      ```
      The output folder will contain a file named ```model.h5``` .
      
   - Taxonomic classification with the new model    
      ```sh
      # /input/folder/ : input foder, contains fasta files
      # /output/folder/ : output folder
      # print_tree : Print the NCBI taxnomy tree
      #               0 : dont print
      #               1 : print it
      # /path/to/model/model.h5 : The model created in the previous step
      # /path/to/embedding/vectorisation_results.csv: the embedding CSV file
      docker run -v $(/input/folder/):/src/input -v $(/output/folder/):/src/output -v $(/path/to/model/model.h5):/src/model.h5 -v  $(/path/to/embedding/vectorisation_results.csv):/src/vectorisation_results.csv -t padriba/nlp_metaxa python3 /src/get_Taxa_custome.py $(print_tree)

     ``` 
     ```sh
         cd NLP_MeTaxa
         mv input/vectorisation_results.csv .
         mv output/model.h5 .
         #copy in input foder the fasta files to predict
         python3 get_Taxa_custome.py $(print_tree) # print_tree : Print the NCBI taxnomy tree, 0 : dont print, 1 : print it
     ```
     

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
     
