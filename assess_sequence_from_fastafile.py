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

def my_dot0( v1 ):
	v2 = ( 1, -1, -1 )
	try:
		#result = ( v1[0]*v2[0] + v1[1]*v2[1] + v1[2]*v2[2] )/( math.sqrt( v1[0]**2 + v1[1]**2 + v1[2]**2 )*math.sqrt( v2[0]**2 + v2[1]**2 + v2[2]**2 ))
		result = numpy.dot( v1, v2 )/numpy.linalg.norm( v1 )/numpy.linalg.norm( v2 )
	except TypeError:
		result = None
	return result

def my_dot1( v1 ):
	v2 = ( -1, 1, -1 )
	try:
		#result = ( v1[0]*v2[0] + v1[1]*v2[1] + v1[2]*v2[2] )/( math.sqrt( v1[0]**2 + v1[1]**2 + v1[2]**2 )*math.sqrt( v2[0]**2 + v2[1]**2 + v2[2]**2 ))
		result = numpy.dot( v1, v2 )/numpy.linalg.norm( v1 )/numpy.linalg.norm( v2 )
	except TypeError:
		result = None
	return result

def my_dot2( v1 ):
	v2 = ( -1, -1, 1 )
	try:
		#result = ( v1[0]*v2[0] + v1[1]*v2[1] + v1[2]*v2[2] )/( math.sqrt( v1[0]**2 + v1[1]**2 + v1[2]**2 )*math.sqrt( v2[0]**2 + v2[1]**2 + v2[2]**2 ))
		result = numpy.dot( v1, v2 )/numpy.linalg.norm( v1 )/numpy.linalg.norm( v2 )
	except TypeError:
		result = None
	return result

def my_arccos( v ):
	if v is not None:
		return numpy.arccos( v )/numpy.pi
	else:
		return None
	

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
			s.get_most_likely_frameshift()
			#print s.differential_graded_likelihood
			s.get_indexes()
			"""
			for fs in s.frameshift_sequences:
				print fs
				print s.frameshift_sequences[fs].fragments
				print s.frameshift_sequences[fs].signals
				print s.frameshift_sequences[fs].radians
				print s.frameshift_sequences[fs].indexes
				dgl_list = map( TM.differential_graded_likelihood, s.frameshift_sequences[fs].fragments ) # frame 0
				dgl_list1 = map( lambda x: TM.differential_graded_likelihood( x[1:] ), s.frameshift_sequences[fs].fragments ) # frame 1
				dgl_list2 = map( lambda x: TM.differential_graded_likelihood( x[2:] ), s.frameshift_sequences[fs].fragments ) # frame 2
				vector_list = zip( map( TM.likelihood_slope, dgl_list ), map( TM.likelihood_slope, dgl_list1 ), map( TM.likelihood_slope, dgl_list2 ))
				print "Vector list:",vector_list
				print "Frame 0:"
				print map( my_dot0, vector_list ) # frame 0
				print map( my_arccos, map( my_dot0, vector_list ))
				print
				print "Frame 1:"
				print map( my_dot1, vector_list ) # frame 1
				print map( my_arccos, map( my_dot1, vector_list ))
				print
				print "Frame 2:"
				print map( my_dot2, vector_list ) # frame 2
				print map( my_arccos, map( my_dot2, vector_list ))
				print
				print
				"""
			print "Most likely frameshift:"
			ML = s.most_likely_frameshift
			print ML.path
			print ML.indexes
			print ML.radian_sums
			print ML.signals
			print
			s.plot_differential_graded_likelihood( show_name=True, show_starts=False, show_ML=True )
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
