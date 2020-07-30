This is an example of using NLP_MeTaxa with three CAMI datasets
1. Download the three datasets:
    [low](https://openstack.cebitec.uni-bielefeld.de:8080/swift/v1/CAMI_I_LOW/gold_standard_low_single.fasta.gz), [medium](https://openstack.cebitec.uni-bielefeld.de:8080/swift/v1/CAMI_I_MEDIUM/CAMI_medium_GoldStandardAssembly.fasta.gz) and [high](https://openstack.cebitec.uni-bielefeld.de:8080/swift/v1/CAMI_I_HIGH/CAMI_high_GoldStandardAssembly.fasta.gz) complexity datasets.
    
2. Create an input directory for each dataset:
  ```
    $HOME/input/low/
    $HOME/input/medium/
    $HOME/input/high/
  ```
  
3. Copy the downloaded datasets in these directories.
4. Create an output directory: 
    ```
    $HOME/output/
    ```
5. Pull the docker image.

    ```sh
     docker pull padriba/nlp_metaxa:latest
   ```
6. To launch NLP_MeTaxa on the low-complexity dataset. If you want to print the NCBI taxonomy tree set ``` print_tree ``` parameter to ```1```. if you don't want to print it, set it to ```0```. 
     ```sh
      # print_tree : Print the NCBI taxnomy tree
      #               0 : dont print
      #               1 : print it
      docker run -v $HOME/input/low:/src/input -v $HOME/output:/src/output -t padriba/nlp_metaxa python3       
      /src/get_Taxa.py $(print_tree)

   ```
     You can do the same thing for the two other datasets, just change the input folder.
  
  7. Once the processing is done, there should be a ```low_taxa.tsv``` and ```low_taxa.tree``` (if you choose to print the NCBI taxonomy  tree) files in your ``` $HOME/output/ ``` directory. 
