# NLP-MeTaxa
NLP-MeTaxa is a multilayer perceptron (MLP) classifier for taxonomic assignments, trained with DNA fragments represented by word2vec embeddings.
The NLP-MeTaxa was evaluated on three datasets used in the first CAMI challenge, where the complexity is gradually ascendant among them, from the low until the high complexity dataset.
# Videos

The following videos show the main functions given by NLP-MeTaxa, tested in Windows and Linux environments. If you do not want to read the whole document you can simply watch  these videos.
- [Window environment](https://dl.dropbox.com/s/95w0jmux2ep3c0p/video_wind_last.mp4?dl=1)
- [Linux environment](https://dl.dropbox.com/s/8g6vnh67y5whlxm/video_linux_last.mp4?dl=1)

# Installation
   ## Docker image
   Pull the docker image
   
   ```sh
     docker pull padriba/nlp_metaxa:latest
   ```
   To launch NLP-MeTaxa
   ```sh
      # /input/folder/ : input foder, contains fasta files
      # /output/folder/ : output folder
      # print_tree : Print the NCBI taxnomy tree
      #               0 : dont print
      #               1 : print it
      docker run -v $(/input/folder/):/src/input -v $(/output/folder/):/src/output -t padriba/nlp_metaxa python3       
      /src/get_Taxa.py $(print_tree)

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

      docker run -v $(/input/folder/):/src/input -v $(/output/folder/):/src/output -t padriba/nlp_metaxa python3       
      /src/vectorisation.py
   ```
   The fasta files in the input directory must respect the following naming policy : Taxonomy_id.****.fna(fasta).
   This is because the vectorization result is going to be used to train the model, and we need labeled data to that

   
   
      
     
  ## Training MLP model
   - To train a new MPL model
    
       ```sh
         # /input/folder/vectorisation_resuls.csv : is the embedding CSV file created in the previous step
         # /output/folder/: the output folder
         # class number : the class number in the embedding CSV file
         # batch size
         # epochs
         
          docker run -v $(/input/folder/vectorisation_resuls.csv):/src/input/vectorisation_results.csv -v $(/output/folder/):/src/output -t padriba/nlp_metaxa python3       
        /src/train_feedforward.py $(class number) $(batch size) $(epochs)
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
     
