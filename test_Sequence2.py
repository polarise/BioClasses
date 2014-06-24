#!/usr/bin/env python
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
	
	for i in xrange( 3 ):
		if i > 0:
			print "+%d: %s" % ( i, s.binary_frame( i, sep="" ))
		elif i == 0:
			print " %d: %s" % ( i, s.binary_frame( i, sep="" ))
		elif i < 0:
			print "%d: %s" % ( i, s.binary_frame( i, sep="" ))
	print "    " + "         |"*(( s.length )//30 )
	
	# a Sequence object
	# t = BiologicalSequence( s.sequence )
	t = RandomSequence( 1000 )
	t.generate()
		
	print 
	print t.info()
	for i in xrange( 3 ):
		print t.colour_frame( i, sep="" )
	print "         |"*(( s.length )//10 )
	
	t.get_frame_sequence()
	
	print "The raw frame sequence..."
	print t.frame_sequence
	
	# now to create paths
	p = Paths( t.frame_sequence )
	
	print "The sanitised frame sequence..."
	print p.unique_frame_sequence
	
	print "Create the branches..."
	p.create_branches()
	
	print "View the branches..."
	for B in p.branches:
		print B
	
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
		for j in p.get_frame_path_sequences( frame ):
			print len( j ), " : ", j
		print
	
if __name__ == "__main__":
	main()