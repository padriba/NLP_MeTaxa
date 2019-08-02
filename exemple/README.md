Input.fasta: 99 metagenomics DNA fragments

After launching the script "script.py", NLP_MeTaxa predict a set of taxonomic_ids, but we need to transform this list to human-readable format:

output: two files
		1- output.txt: in the first column there is the sequence id then a tabulation then a dictionary list where each element format {taxonomic_id, NCBI Rank}
		2- tree.txt: tree for a given set of taxonomic_ids
