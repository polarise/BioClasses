# -*- encoding: utf-8 -*-
from __future__ import division
import math
from FrameshiftSite import *

class FrameshiftSequence( object ):
	def __init__( self, sequence, path ):
		self.path = path
		self.path_str = ",".join( map( str, [ a for a,b in path ]))
		self.frameshifted_sequence, self.fragments, self.signals = self.frameshift_from_path( sequence, path )
		self.length = len( self.frameshifted_sequence )
		self.frameshift_count = len( self.path ) - 1
		self.CAI = None
		self.likelihood = None
		self.graded_likelihood = None
		self.differential_graded_likelihood = None
		self.radians = None
		self.radian_sums = None
		self.indexes = None
		self.frameshift_sites = dict()
		self.GC_content = None
		self.gradient = None
	
	#*****************************************************************************
	
	def __repr__( self ):		
		return """\
Path:                  %s
Frameshifted sequence: %s
Fragments:             %s
Signals:               %s
Length:                %s
No. of frameshifts:    %s
CAI:                   %s
Log-likelihood:        %s"""\
	% ( ",".join( map( str, self.path )), \
		"...".join([ self.frameshifted_sequence[:20], \
			self.frameshifted_sequence[-20:] ]), ", ".join( self.fragments ),\
				",".join( self.signals ), self.length, self.frameshift_count, self.CAI, self.likelihood )
	
	#*****************************************************************************
	
	def repr_as_row( self, sep="\t" ):
		return sep.join([ "...".join([ self.frameshifted_sequence[:20], 
				self.frameshifted_sequence[-20:] ]), str( self.length ), \
					str( self.frameshift_count ), str( self.CAI ), \
						str( self.CAI/math.sqrt( self.frameshift_count + 1 )), ",".join( map( str, self.path )), \
							",".join( self.signals ), str( self.likelihood )])
	
	#*****************************************************************************
			
	def frameshift_from_path( self, sequence, path ):
		"""
		"""
		# first get all frame of sequence
		sequence_in_frames = dict()
		for i in xrange( 3 ):
			sequence_in_frames[i] = sequence[i:]
		
		frameshifted_sequence = ""
		fragments = list()
		frameshift_signals = list()
		i = 0
		f_i = 0
		for f,j in path:
			frameshifted_sequence += sequence[i+(f-f_i):j]
			fragments.append( sequence[i+(f-f_i):j] )
			frameshift_signals.append( sequence[j-3:j+3] )
			i = j
			f_i = f
		
		# we could factor in the last trivial nucleotide...
		frameshifted_sequence += sequence[-1]
		fragments[-1] += sequence[-1]
				
		return frameshifted_sequence, fragments, frameshift_signals[:-1]
	
	#*****************************************************************************
	
	def find_frameshift_sites( self ):
		def frameshift_position_score( x, L ):
			"""
			triangular function
			P( frameshift ) is maximum in the middle and decreases to the edges
			"""
			if x < L/2:
				return x/(L/2)
			else:
				return ( L - x )/(L/2)
			
		for i in xrange( len( self.indexes ) - 1 ):
			if self.indexes[i] == 0 and self.indexes[i + 1] == 0:
				initial_node = self.path[i]
				final_node = self.path[i+1]
				signal = self.signals[i]
				radians_vector = self.radians[i]
				position_score = frameshift_position_score( initial_node[1], self.length )
				self.frameshift_sites[initial_node] = FrameshiftSite( initial_node, \
					final_node, signal, position_score, radians_vector )
				
	#*****************************************************************************
	def estimate_GC_content( self ):
		self.GC_content = ( self.frameshifted_sequence.count( "C" ) + \
			self.frameshifted_sequence.count( "G" ))/self.length
		return self.GC_content
	
	#*****************************************************************************
	def estimate_gradient( self ):
		self.gradient = self.differential_graded_likelihood[-1]/self.length
		return self.gradient
	