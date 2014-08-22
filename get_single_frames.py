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

def PrintStatic( text ):
	sys.stderr.write( "\r%s" % text )
	sys.stderr.flush()

def main( fn, sn_file ):
	with open( sn_file ) as sf:
		seq_names = { row.strip( "\n" ):0 for row in sf }

		TM = TransitionMatrix()
		TM.read( "transition_matrices/euplotid_transition_matrix.pic" )
		pdf = PdfPages( "single_frames.pdf" )
		c = 0
		for seq_record in SeqIO.parse( fn, "fasta" ):
			#if c >= 100:
				#break
			sequence = str( seq_record.seq )
			seq_name = seq_record.id
			if seq_name in seq_names:
				PrintStatic( "Examining %s of %s sequences..." % ( c, len( seq_names )))
				s = Sequence( sequence=sequence, name=seq_name, stops=[ 'TAA', 'TAG' ] ) # Us
				s.truncate( effect_truncation=True, verbose=False )
				s.set_transition_matrix( TM )
				s.build_tree()
				s.get_frameshift_signals()
				s.estimate_likelihood()
				s.estimate_frameshift_likelihood()
				s.get_most_likely_frameshift()
				s.get_indexes()
				#s.repr_frameshift_sites( include_nulls=False )
				if s.most_likely_frameshift is not None:
					if len( s.most_likely_frameshift.frameshift_sites ) == 0:
						#s.plot_differential_graded_likelihood( outfile=pdf, show_name=False, \
							#show_starts=False, show_ML=False )
						print ">%s" % s.name
						print s
			c += 1
		print >> sys.stderr
		pdf.close()

if __name__ == "__main__":
	try:
		fn = sys.argv[1]
		sn_file = sys.argv[2]
	except IndexError:
		print >> sys.stderr, "./script.py <fasta-file> <seq_names_file>"
		sys.exit( 1 )
	main( fn, sn_file )
