# otu_compare
This code is designed to test for chimeric OTUs after swarm clustering.

The .swarms file is the default inputfile type, with all the sequences belonging to an OTU listed on one row. Parsing of the files is done based on the assumption that the sequence identifiers contain the size=[0-9] attribute from the dereplication of the sequences.

In calling: python otu_comparison2.py file1 file2 file2, it will use file1 as reference and compare the OTUs to the OTUs in file2 and then to file3.

The output is in the form of three files: passed_OTUs, bad_seqs and chimeric_OTUs. Of these, passed_OTUs contain clusters of sequences that are not chimeric. The file bad_seqs contains a list of sequences that have been part of chimeric OTUs, and deemed chimeric sequences. The file chimeric OTUs is an intermediate file, listing chimeric OTUs before the chimeric sequences within the OTU are directed into bad_sequences.
