#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import division
import sys
import time
from Node import *
from LeafCounter import *
from Sequence import *
from Bio import SeqIO
from TransitionMatrix import *
import cPickle
from GeneticCode import *

def main( fn ):
	TM = TransitionMatrix()
	TM.read( "euplotid_transition_matrix.pic" )
	
	G = GeneticCode( "euplotid_genetic_code.txt" )
	G.read_CAI_table( "euplotid_CAI_table.txt" )
	
	c = 0
	for seq_record in SeqIO.parse( fn, "fasta" ):
		if c > 100: break
		sequence = str( seq_record.seq )
		seq_name = seq_record.id
		
		# first we check whether we will be able to build the tree
		s = Sequence( sequence )
		s.truncate()
		s.get_stop_sequence()
		s.sanitise_stop_sequence()
		nodes = [ Node( *d ) for d in s.unique_stop_sequence ]
		L = LeafCounter()
		for n in nodes[:-3]:
			L.add_node( n )
		# print "%s\t%s" % ( seq_name, L.leaf_count() )
		if L.leaf_count() > 10000:
			print >> sys.stderr, "Skipping complex sequence %s with %d leaves..." % ( seq_name, L.leaf_count())
			continue
			
		# now we know that we can ;-)
		s.set_transition_matrix( TM )
		s.set_genetic_code( G )
		s.build_tree()
		s.estimate_frameshift_likelihood()
		s.estimate_frameshift_CAI()
		
		s.get_most_likely_frameshift()
		
		if s.most_likely_frameshift is None:
			print >> sys.stderr, "%s admits no frameshifts..." % seq_name
		else:
			print seq_name + "\t" + s.most_likely_frameshift.repr_as_row()
		
		c += 0
	
if __name__ == "__main__":
	fn = sys.argv[1]
	main( fn )	