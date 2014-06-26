#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import division
import sys
from Sequence import *
from Node import *
from Branch import *
from Paths import *

def main():
	s = RandomFSSequence( no_of_shifts=2, min_length=50, max_length=100 )
	s.generate()
	
	print s.info( "without UGA" )
	
	# a Sequence object
	#t = BiologicalSequence( s.sequence )
	#t = BiologicalSequence( "GCTGGTGGGGTAGCAGGTGTTTCTGTTGACTTGATATTATTTCCTCTGGATACCATTAAAACCAGGCTGCAGAGTCCCCAAGGATTTAGTAAGGCTGGTGGTTTTCATGGAATATATGCTGGCGTTCCTTCTGCTGCTATTGGATCCTTTCCTAATG" )
	t = BiologicalSequence( "AAATGACGAACACAGAGGAAAGAAGAGAGGCAACTGCTGAGGTCCCCTAGGCCTTTGAGAAAACGGAGTTGTACCTTTGGCAACATAAGTGCATATCTACAAGAAAGGCGATAATGTAGACACCAAGGGAATGGGTACTGTCCAAAAAGAAATGCCTCACAAATGTCACCATGGCAAAACTAAAAGAGTCTACAAAGTTACCTAGCATGCTGTTGGCATCATTGTAAACAAACAAGTTAAGGGCAAGATTCTTGCCAAGAGAATTAATATGCATATTGGGCATATTAAGCACTCTAAGAGCCAAGATGATTTCCTGAAAGTGTGTGAAGGAAAATAACCAGCATAAAGAGGGAAGCTAAAGAGAAACCTGAAGCTGCAGCCTGTTCCACCCAGAGAAGCACACTTTGTAAGAACCAATGAAAAGGAGCCTGAGCTGCTGGAGTCTATTAACTGAATTCATGGT" )
	#t = RandomSequence( 100 )
	#t.generate()
	#t.stops.append( "UGA" )	
		
	print 
	print t.info()
	for i in xrange( 3 ):
		print t.colour_frame( i, sep="" )
	print "         |"*(( s.length )//10 )
	
	t.get_stop_sequence()
	
	print "The raw stop sequence (%s)..." % len( t.stop_sequence )
	print t.stop_sequence
	print
	
	# now to create paths
	p = Paths( t.stop_sequence )
	
	print "The sanitised stop sequence (%d)..." % len( p.unique_frame_sequence )
	print p.unique_frame_sequence
	print
	
	print "Create the branches from the stop sequence..."
	p.create_branches()
	print
	
	print "View the branches..."
	for B in p.branches:
		print B
	
	#sys.exit()
	
	print "Build the paths..."
	p.build_paths()
	
	# print "View the paths..."
	# print p.paths
		
	all_paths = p.get_all_path_sequences()
	print "Get all the (%s) paths..." % len( all_paths )
	print all_paths
	print
	
	# print "Frameshift sequences preceded by their length..."
	# for a in all_paths:
	# 	print len( a )," : ", a
	
	for frame in xrange( 3 ):
		print "Frameshift sequences for frame %d:" % frame
		for j in p.get_frame_paths( frame ):
			print len( j ), " : ", j
		print
	
	"""
	frameshifted_sequence, fragments = t.frameshift_from_path( all_paths[0] )
	q = BiologicalSequence( s.sequence )
	print s.info()
	for i in xrange( 3 ):
		print q.colour_frame( i, sep="" )
	print "         |"*(( s.length )//10 )
	print
	
	print " ".join( fragments )
	print
	
	print t.path
	print t.colour_frameshifted_sequence( sep="" )
	print "         |"*(( s.length )//10 )
	"""
	
	for i in xrange( 3 ):
		all_paths = p.get_frame_paths( i )
		for a in all_paths:
			frameshifted_sequence, fragments, frameshift_signals = t.frameshift_from_path( a )
			print t.path
			print t.colour_frameshifted_sequence( sep="" )
			print " ".join( fragments )
			print " ".join( frameshift_signals )
			print
		
	print "Actual sequence: %s" % s.info()
	
if __name__ == "__main__":
	main()