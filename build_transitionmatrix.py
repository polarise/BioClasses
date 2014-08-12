#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from TransitionMatrix import *
from Sequence import *
import numpy
import matplotlib.pyplot as plt
import math
from Bio import SeqIO
from LeafCounter import *
from matplotlib.backends.backend_pdf import PdfPages

def main( fn ):
	# initialise the TransitionMatrix
	TM = TransitionMatrix()
	TM.build( fn )
	TM.write( "transition_matrices/homo_transition_matrix.pic" )
	#TM.write( "transition_matrices/tetrahymena_transition_matrix.pic" )
	#TM.read( "euplotid_transition_matrix.pic" )

if __name__ == "__main__":
	try:
		fn = sys.argv[1]
	except IndexError:
		raise IOError( "Missing CDS FASTA file for input." )
	main( fn )

