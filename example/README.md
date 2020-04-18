This is an example of using NLP_MeTaxa with three CAMI datasets
1. Download the three datasets:
    [low](https://drive.google.com/open?id=1-0uaypF4TaWNELcvZ05DiKJyjZVkDT-a), [medium](https://drive.google.com/open?id=1-8VenrEdSc7D1sAKrFdht1XR_hZIC7Lr) and [high](https://drive.google.com/open?id=1-9AKKjRA-ca-CjwFz2tSV9a_-mk_nTGs) complexity datasets.
    
2. Create an input directory for each dataset:
  ```
    $USER_HOME$/input/low/
    $USER_HOME$/input/medium/
    $USER_HOME$/input/high/
  ```
  
3. Copy the downloaded datasets in these directories.
4. Create an output directory: 
    ```
    $USER_HOME$/output/
    ```
5. Pull the docker image.

    ```sh
     docker pull padriba/nlp_metaxa:latest
   ```
6. To launch NLP_MeTaxa on the low-compelexity dataset. If you want to print the NCBI taxnomy tree set ``` print_tree ``` parameter to ```1```. if you dont want to print it, set it to ```0```. 
     ```sh
      # print_tree : Print the NCBI taxnomy tree
      #               0 : dont print
      #               1 : print it
      docker run -v $USER_HOME$/input/low/:/src/input -v $USER_HOME$/output/:/src/output -t padriba/nlp_metaxa python3       
      /src/get_Taxa.py $USER_HOME$/input/low/ $USER_HOME$/output/ $(print_tree)

   ```
     You can do the same think for the two others datasets, just change the input folder.
  
  7. Once the processing is done, there should be a ```low_taxa.tsv``` and ```low_taxa.tree``` (if you choose to print the NCBI taxnomy tree) files in your ``` $USER_HOME$/output/ ``` directory. 
