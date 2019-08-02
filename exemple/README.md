- Input.fasta: contains 99 metagenomics DNA fragments

- After launching the script "script.py", NLP_MeTaxa predict a set of taxonomic_ids, but you need to transform this set to human-readable     
  format 
 - output files:
	* output.txt: in the first column there is the sequence id then a tabulation then a dictionary list where each element format                   {taxonomic_id, NCBI Rank}
	* tree.txt: tree for a given set of taxonomic_ids
