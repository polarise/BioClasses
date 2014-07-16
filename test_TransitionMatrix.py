#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from TransitionMatrix import *
from Sequence import *

def main( fn ):
	# initialise the TransitionMatrix
	TM = TransitionMatrix()
	# T.build( fn )
	# T.write( "euplotid_transition_matrix.pic" )
	TM.read( "euplotid_transition_matrix.pic" )
	# print len( T.transition_counts.keys() )
	# for k in T.transition_counts:
	# 	l = len( T.transition_counts[k].keys())
	# 	if l < 64:
	# 		print k, l
	# print T.transition_counts
	# print
	# print T.transition_probabilities
	# print
	# print T.probability( "AAA", "CCC" )
	# print
	# print T.probability( "AAA", "CCC", loglik=True )
	# print
	sequence = "ATCGGAAGAGGCAATTTCATAATAACATTTACACTAAGCTGAAGCCCAAGGAAATGAACTCCCATTTTAGCGATTATAATGAGACCAGGTATGAAGTCACTACTGGGTTTAATAGCAAGAAGATCAAACTTAAGGTTAGTACTAACACCGAAGGGGATGAACAGAGCAAGCCTATGAATAAGAGGACTTTTAAGAACGATATACTTGAGAAGGAGGAGGATCCCACTGGGAAGAAAACTGTGGTGTATAAGGATTTTATAGACTTTTGTAAAATTCATAAGGGGCAGATTTTTGGGTATAGAACTATCATGCCTCTTGAGTTTTATATTATGTCAAAATAGAACCGATTATGAGAGGGAGTTTATAAAAAGGGCTGAGAAGGAAGAGATTCAGAAGTTCTTTAATGAAGCATGAGTATCCATTGTGGCTAACTCAGCAATCGTTGAGACCTTTATCTTTGAAAAGGCTTTAATGTCTTTTCTACCAGAACACCTGTCTCAGGCTTTCTTCAAGGATTTACTGAATTGCAAAGAGCATGACAGGCCTGCTAATATCGTTGAGAAAGGCAAGAACGATAGTATTATTGGAAGTATTATCAAGATGAATAAAGAAGATGATTTATGGGATAATACTAAAAACAAAATTATTGATAAGACGCTCAAAGCGTCCTATATCGAGAGACACAAGGCTTTAG"
	s = Sequence( sequence )

	print TM.likelihood( s, loglik=True )
	print
	sys.exit( 0 )
	
	with open( "loglikelihood_frameshifted3.txt", 'w' ) as of:
		i = 0
		loglik = 0
		while i <= len( s ) - 6:
			C1 = s[i:i+3]
			C2 = s[i+3:i+6]
			loglik += TM.probability( C1, C2, loglik=True )
			print >> of, "%s\t%s" % ( i, loglik )
			i += 3

if __name__ == "__main__":
	try:
		fn = sys.argv[1]
	except IndexError:
		raise IOError( "Missing input FASTA file." )
	
	main( fn )