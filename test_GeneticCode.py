#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from GeneticCode import *
from Sequence import *

def main():	
	G = GeneticCode( "genetic_codes/euplotid_genetic_code.txt" )
	G.build_CAI_table( "/home/paul/bioinf/Translational_Frameshifting/2_Euplotes_data/E.crassus_CDS.fasta" )
	#G.build_CAI_table( "a_fasta.fa" )
	#G.write_CAI_table( "euplotid_CAI_table.txt" )
	#G.write_CAI_table( "test_CAI_table.txt" )
	#G.read_CAI_table( "euplotid_CAI_table.txt" )
	#print G
	s = Sequence( "TAGAGATACACTGACTTACTTTCAAATACTATAAAACGGAATAGCCTAAGAATGAAATAAAGTAAAACATGACCATCAGGAGAAAGTTGAACAACTAGAGAGGGAGAATATTAAGCTTTATGCCCAATTAAAAAAGCTTGCAAAAAGTGAAAGAAATCTAATGAAGAAACTAGACGAAAGAGACCGGGAGATAACCAATCTAAAAGATACAAACATGAGGTTCAATTACAAACTCAATAGAGCACTCTATGCTAATGAAGAGCTGCAAAATAAAGTAACTGAATCTGACTACAAACTTCAACAAAAAAGAGATGAATTTATGAAAGACATAGAGCAAACTAACCAAATCC" )
	#s = Sequence( "TCAAACCGAGACTTACTAAAGTTGATCATCATAAGACTC" )
	s.set_genetic_code( G )
	s.estimate_CAI()
	s.as_codons = True
	print s
	print s.CAI_score
	s.truncate()
	s.build_tree()
	print s.tree
	s.estimate_frameshift_CAI()
	for fs in s.frameshift_sequences:
		print s.frameshift_sequences[fs].repr_as_row()
	
if __name__ == "__main__":
	main()