# NLP_MeTaxa
NLP-MeTaxa is a convolutional neural network (CNN) classifier for taxonomic assignments, trained with DNA fragments represented by word2vec embeddings.
The NLP-MeTaxa was evaluated on three datasets used in the first CAMI challenge, where the complexity is gradually ascendant among them, from the low until the high complexity dataset.

# Evaluation
  ## Installation
  - Download NLP_MeTaxa by 
    ```sh
      git clone https://github.com/padriba/NLP_MeTaxa.git
      ```
   - Installation has been tested in Linux based system with Python 3.6.7.
  
  ## NLP Vectorization
  To get a word2vec embedding representation for the metagenomic sample:
   - For the low comlexity datset:
   
      ```sh
        python ./NLP/vectorisation_low.py
      ```
     The result will be found in ./NLP/vectorisation_results/low/
    
   - For the medium comlexity datset:
   
      ```sh
        python ./NLP/vectorisation_medium.py
      ```
     The result will be found in ./NLP/vectorisation_results/medium/
     
   - For the high comlexity datset:
   
      ```sh
        python ./NLP/vectorisation_high.py
      ```
     The result will be found in ./NLP/vectorisation_results/high/
     
     
  ## Training CNN model
  ## Overall mertics
  ## Metrics by rank
