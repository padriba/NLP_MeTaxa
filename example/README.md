This is an example on how to use NLP_MeTaxa using the three CAMI datasets
1. Download the three datasets:
    [Low complexity dataset](https://drive.google.com/open?id=1y_7NfwLbb5Gu_F6D2kR3T9ma7pRSusdr) .
    [Medium complexity dataset](https://drive.google.com/open?id=1dBhelGLAm_zKB0s1m2rAO3UJqDqXkGJV) .
    [High complexity dataset](https://drive.google.com/open?id=1KhPt1rpzCTvoiPqQBZ31xoB1a89G51xD) .
    
2. Creat in your home an input directory for each dataset:
  ```
    $USER_HOME$/input/low/
    $USER_HOME$/input/medium/
    $USER_HOME$/input/high/
  ```
  
3. copy the downloaded datasets in these directories
4. creat an output directory: 
    ```
    $USER_HOME$/output/
    ```
5. pull the docker image

    ```sh
     docker pull padriba/nlp_metaxa:latest
   ```
6. To launch NLP_MeTaxa on the low-compelexity dataset
     ```sh
      # print_tree : Print the NCBI taxnomy tree
      #               0 : dont print
      #               1 : print it
      docker run -v $USER_HOME$/input/low/:/src/input -v $USER_HOME$/output/:/src/output -t padriba/nlp_metaxa python3       
      /src/get_Taxa.py $USER_HOME$/input/low/ $USER_HOME$/output/ $(print_tree)

   ```
  you can do the same think for the two others datasets, just change the input folder.
  
  7. 
