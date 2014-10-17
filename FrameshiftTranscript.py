# -*- encoding: utf-8 -*-
from __future__ import division
import sys
from FrameshiftSite import *

class FrameshiftTranscript( object ):
	def __init__( self, name, length ):
		self.name = name
		self.length = length
		self.frameshift_sites = dict()
	
	def add_frameshift_site( self, position, signal ):
		def frameshift_position_score( x, L ):
			"""
			triangular function
			P( frameshift ) is maximum in the middle and decreases to the edges
			"""
			if x < L/2:
				return x/(L/2)
			else:
				return ( L - x )/(L/2)
		
		position_score = frameshift_position_score( position, self.length )
		
		self.frameshift_sites[position] = FrameshiftSite( ( 0, position ), \
			( 0, 0 ), signal, self.length, position_score )
	
	def __repr__( self ):
		output_str = "Transcript: %s of length %s\n" % ( self.name, self.length )
		i = 1
		for pos,FS in self.frameshift_sites.iteritems():
			output_str += "Frameshift #%s: %s at %s (pos-score = %s).\n" % ( i, \
				FS.signal, FS.position, FS.position_score )
			i += 1
		
		return output_str

	def rough_equality( self, FS ):
		if len( self.frameshift_sites ) > 0 and len( FS.frameshift_sites ) > 0:
			return True
		else:
			return False
			
		
	
