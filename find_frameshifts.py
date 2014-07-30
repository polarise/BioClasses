#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import division
import sys
import math
from Sequence import *
from TransitionMatrix import *
import numpy
import numpy.linalg
import scipy.signal
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from Bio import SeqIO

def main( fn, count ):
	TM = TransitionMatrix()
	TM.read( "euplotid_transition_matrix.pic" )
	pdf = PdfPages( "found_frameshifts.pdf" )
	c = 0
	for seq_record in SeqIO.parse( fn, "fasta" ):
		if c >= count:
			break
		sequence = str( seq_record.seq )
		seq_name = seq_record.id
		s = Sequence( sequence=sequence, name=seq_name )
		s.truncate( effect_truncation=True, verbose=False )
		no_of_leaves = s.count_leaves()
		if no_of_leaves > 1000:
			print >> sys.stderr, "Complex tree with %s leaves...omitting." % no_of_leaves
			continue
		s.set_transition_matrix( TM )
		s.build_tree()
		s.get_frameshift_signals()
		s.estimate_likelihood()
		s.estimate_frameshift_likelihood()
		s.get_most_likely_frameshift()
		s.get_indexes()
		s.repr_frameshift_sites( include_nulls=False )
		if s.most_likely_frameshift is not None:
			if len( s.most_likely_frameshift.frameshift_sites ) > 0:
				s.plot_differential_graded_likelihood( outfile=pdf, show_name=True, \
					show_starts=False, show_ML=True )
		c += 1
	pdf.close()

if __name__ == "__main__":
	try:
		fn = sys.argv[1]
		try:
			count = sys.argv[2]
		except IndexError:
			count = 10
	except IndexError:
		print >> sys.stderr, "./script.py <fasta-file> [<seq-count>]"
		sys.exit( 1 )
	main( fn, count )
