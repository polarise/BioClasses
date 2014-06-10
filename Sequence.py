from __future__ import division
import sys
import itertools
import random
import termcolor

class Sequence( object ):
	# basic stuff
	self.bases = 'ACGU'
	self.start = [ 'AUG' ]
	self.stop = [ 'UAA', 'UAG' ]
	self.itercodons = itertools.product( self.bases, repeat=3 )
	self.non_stops = [ "".join( codon ) for codon in itercodons ]
	for stop in self.stop:
		self.non_stops.remove( stop )
	
	def __init__( self, sequence=None ):
		self.length = None
		self.sequence = None
		self.frameshifts = None
		self.frame_lengths = None
		
	def __repr__( self ):
	
	def generate_random_sequence( self, length ):
		self.sequence = ""
		while len( self.sequence ) < length:
			self.sequence += random.choice( self.bases )
		self.length = len( self.sequence )
	
	def colour_frame( self, frame, sep=" " ):
	frame = frame % 3 # ensure that you have a valid frame; no need for errorcheck
		
	split_sequence = ""
	
	# front
	codon = sequence[0:frame]
	if codon in start:
		codon = termcolor.colored( codon, 'yellow', 'on_yellow', attrs='bold' )
	if codon in stop:
		codon = termcolor.colored( codon, 'white', 'on_red', attrs='bold' )
	
	if frame % 3 != 0:
		split_sequence += codon + sep
	
	# body
	i = frame
	while i < len( sequence ):
		codon = sequence[i:i+3]
		if codon in start:
			codon = termcolor.colored( codon, 'yellow', 'on_green', attrs=['bold'] )
		if codon in stop:
			codon = termcolor.colored( codon, 'white', 'on_red', attrs=['bold'] )
		split_sequence += codon + sep
		i += 3
	
	return split_sequence
		
	def generate_frameshift_sequence( self, frameshifts, frame_lengths ):
	
	def initiate_sequence( self, frame ):
	
	def generate_nonstop_codon( self, length ):
	
	def generate_stop_codon( self ):
	
	def change_frame( self, change ):
	
	def generate_frameshifts( self, no_of_shifts ):
	
	def generate_frame_lengths( self, no_of_shifts ):
	
	
