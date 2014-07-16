#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from TransitionMatrix import *
from Sequence import *
import numpy
import matplotlib.pyplot as pylab
import math

def f( x ):
	return -x*math.log( 64 )/3

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
	sequence = """ACTCCTTACATAAGATGCTATACTCCCTTCAGATTATCAGCAATAAATCTCAAAATTCTG
AAAATGAATGGTTGGCTAAGTTCTTAATGATTGGAGGATATCAACACCTCTTCTCAACAC
TCTTAAAAATTGATCCTTCAAAGATCATCTCAAACCTCTCATTTAAATCTGTGGATATTC
TAGTGAGGTTGATTTGTATCTCAATGGAGAAGCATGACCAAATCTCAGAAATCGAAGGTG
CTCCTAATCTTCTCGAGATCTACAGAGAGCATTCTATTGTAGCTATAGATAAAATACTGA
GAATTATCCATCAAATCACTCTGAACTCTATCAGTGATTGTAAAAAGAGAGGTGATTCTT
ATGATGACTTGTTCTACAAGAACAAGAAACTTGAACAACAAAGTATGCGACTCCTATCTT
ACTACGAAAAATCCAAGAGTGACAATGAACAGGAGGAACAAAATACTTATTCTCGCAAAA
TCAATGAGCTGAATAAGAAGTTTGATGAAGGAGGAAAGTTCATTCTTCTCTCTTTCAAGT
TGTTCTACTACCTTGACTGTTTCAACAATGAGACCTGTATCCAACAGTTTATTGAGTTCC
CGGATCTTACAAGTCTTCTAAGAAATATCCTCTTTGTGACAGACAACGTCTACCTCAGAA
ATAATTTTGGAGATAGCCTGAAGGAAGTCTGTGCTAATGTGCAAAATGAGTTACAGATGT
TTTTGGAGTTCAAGAAGATGATCATGCTCAAACTTATTTATGACATGGATGAGGTCGCTT
CTGAAAACCAAACAAGAGCTTATAAAGCTAACGAGATAGTCCAAAATATCCTCTCTGGCA
CAAGAACATACCAACTTGAGAGAATGAACATTGACTTTGAAGAGATCTTGAAAAGAAACG
TCAAAATTATTTTTGAAAAAGAAACTATTGAAAAGAGCTCAAACGAGTTTGACCATATTA
TCTTTGGAGCTATGGGCCATACCAAGTTGATCATTCAGCAATTCCCTAGGTA"""

	sequence = sequence.replace( "\n", "" )
	s = Sequence( sequence )
	s.truncate()
	s.set_transition_matrix( TM )
	s.build_tree()
	print s.tree
	s.estimate_likelihood()
	s.estimate_frameshift_likelihood()
	for fs in s.frameshift_sequences:
		print fs, s.frameshift_sequences[fs].likelihood

	# print TM.likelihood( s, loglik=True )
	# print
	# sys.exit( 0 )
	#
	# with open( "loglikelihood_frameshifted3.txt", 'w' ) as of:
	# 	i = 0
	# 	loglik = 0
	# 	while i <= len( s ) - 6:
	# 		C1 = s[i:i+3]
	# 		C2 = s[i+3:i+6]
	# 		loglik += TM.probability( C1, C2, loglik=True )
	# 		print >> of, "%s\t%s" % ( i, loglik )
	# 		i += 3
	
	print 
	s.get_most_likely_frameshift()
	print "Most likely frameshift:\n%s" % s.most_likely_frameshift
	print
	print "Least likely frameshift:\n%s" % s.least_likely_frameshift
	print
	
	likelihood_values = [ s.frameshift_sequences[fs].likelihood for fs in s.frameshift_sequences ]
	print "Likelihood range: %s to %s" % ( min( likelihood_values ), max( likelihood_values ))
	print
	# print "All frameshifts:"
	# for fs in s.frameshift_sequences:
	# 	print s.frameshift_sequences[fs]
	# 	print
	
	x = numpy.linspace( 1, s.length, len( s.graded_likelihood ) )
	pylab.plot( x, map( lambda w: w[1] - f( w[0] ), zip( x, s.graded_likelihood )))
	# pylab.plot( x, f( x ), '--' )
	for fs in s.frameshift_sequences:
		F = s.frameshift_sequences[fs]
		y = numpy.linspace( 1, F.length, len( F.graded_likelihood ))
		pylab.plot( y, map( lambda w: w[1] - f( w[0] ), zip( y, F.graded_likelihood )))
	
	# draw all the frameshift sites
	most_likely_signals = s.most_likely_frameshift.signals
	ymin, ymax = pylab.ylim()
	i = 0
	for frame,position in s.most_likely_frameshift.path:
		if position >= 0:
			pylab.axvline( x=position+1 ) # 0-based to 1-based
			pylab.annotate( most_likely_signals[i], xy=( position+1, ymax - 4 ), rotation=90 )
			i += 1

	pylab.grid()
	pylab.show()

if __name__ == "__main__":
	fn = sys.argv[1]
	main( fn )