#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import division
import sys
from Sequence import *
from TransitionMatrix import *
import numpy
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from Bio import SeqIO

def main( fn ):
	TM = TransitionMatrix()
	TM.read( "euplotid_transition_matrix.pic" )
	# pdf = PdfPages( "likelihood_profiles_1000fs.pdf" )
	c = 0
	for seq_record in SeqIO.parse( fn, "fasta" ):
		if c > 1:
			break
		sequence = str( seq_record.seq )
		seq_name = seq_record.id
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
		# s.plot_differential_graded_likelihood( outfile=pdf )
		s.plot_differential_graded_likelihood()
		c += 1
	# pdf.close()
	
if __name__ == "__main__":
	try:
		fn = sys.argv[1]
	except IndexError:
		print >> sys.stderr, "./script.py <fasta-file>"
		sys.exit( 1 )
	main( fn )
