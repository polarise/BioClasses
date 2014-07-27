#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import division
import sys
from Sequence import *
from TransitionMatrix import *
import numpy
import scipy.signal
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from Bio import SeqIO

def main( fn, seq_name ):
	TM = TransitionMatrix()
	TM.read( "euplotid_transition_matrix.pic" )
	# find the sequence we're looking for
	found = False
	for seq_record in SeqIO.parse( fn, "fasta" ):
		if seq_record.id == seq_name:
			sequence = str( seq_record.seq )
			s = Sequence( sequence=sequence, name=seq_name )
			s.truncate( effect_truncation=True )
			no_of_leaves = s.count_leaves()
			if no_of_leaves > 1000:
				print >> sys.stderr, "Complex tree with %s leaves...omitting." % no_of_leaves
				continue
			s.set_transition_matrix( TM )
			s.build_tree()
			s.get_frameshift_signals()
			s.estimate_likelihood()
			s.estimate_frameshift_likelihood()
			#print s.differential_graded_likelihood
			#for fs in s.frameshift_sequences:
				#corr = scipy.signal.correlate( s.differential_graded_likelihood, \
					#s.frameshift_sequences[fs].differential_graded_likelihood, mode='same' )
				#plt.plot( range( 212 ), corr )
			#plt.grid()
			#plt.show()
			s.plot_differential_graded_likelihood( show_name=False )
			found = True
			break
	
	if not found:
		print >> sys.stderr, "Sequence %s was not found." % seq_name
	
if __name__ == "__main__":
	try:
		fn = sys.argv[1]
		seq_name = sys.argv[2]
	except IndexError:
		print >> sys.stderr, "./script.py <fasta-file> <seq-name>"
		sys.exit( 1 )
	main( fn, seq_name )
