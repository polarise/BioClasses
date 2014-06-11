from __future__ import division
import sys
import itertools
import random
import termcolor

class Sequence( object ):
	"""
	Sequence class
	execution paths
	1. Random sequence
		- generate_random_sequence( length )
	2. Frameshift sequence
		- self.min_length = <int>
		- self.max_length = <int>
		- self.no_of_frameshifts = <int>
		- generate_frameshift_sequence()
	"""
	def __init__( self, sequence=None, frameshifts=None, frame_lengths=None, no_of_shifts=None, min_length=None, max_length=None ):
		"""
		Initialise a Sequence object
		"""
		# basic stuff
		self.bases = 'ACGU'
		self.start = [ 'AUG' ]
		self.stop = [ 'UAA', 'UAG' ]
		itercodons = itertools.product( self.bases, repeat=3 )
		self.non_stops = [ "".join( codon ) for codon in itercodons ]
		for stop in self.stop:
			self.non_stops.remove( stop )
		
		# params
		self.is_frameshift = False
		self.length = None
		self.sequence = sequence
		self.frameshifts = frameshifts
		self.frame_lengths = frame_lengths
		self.no_of_shifts = no_of_shifts
		self.min_length = min_length
		self.max_length = max_length
		
	def info( self ):
		"""
		Method to print summary info
		"""
		if self.is_frameshift:
			return "Frameshift sequence (%s) of lengths (%s) and total length of %d:" % ( ",".join( map( str, self.frameshifts )), ",".join( map( str, self.frame_lengths )), self.length )
		else:
			return "Random sequence of length %d:" % self.length
		
	def __repr__( self, as_codons=False ):
		sequence = list()
		if as_codons:
			for i in xrange( 0, len( self.sequence ), 3 ):
				sequence.append( self.sequence[i:i+3] )
			return " ".join( sequence )
		else:
			return self.sequence
		
	def __str__( self ):
		return self.sequence
	
	def generate_random_sequence( self, length ):
		"""
		Method to generate a random sequence of lenght length
		"""
		self.sequence = ""
		while len( self.sequence ) < length:
			self.sequence += random.choice( self.bases )
		self.length = len( self.sequence )
		self.is_frameshift = False
	
	def colour_frame( self, frame, sep=" " ):
		"""
		Method to return in colour for frame frame
		"""
		# ensure that you have a valid frame; no need for errorcheck
		frame = frame % 3 
		
		coloured_sequence = ""
	
		# front
		codon = self.sequence[0:frame]
		if codon in self.start:
			codon = termcolor.colored( codon, 'yellow', 'on_yellow', attrs='bold' )
		if codon in self.stop:
			codon = termcolor.colored( codon, 'white', 'on_red', attrs='bold' )
	
		if frame % 3 != 0:
			coloured_sequence += codon + sep
	
		# body
		i = frame
		while i < len( self.sequence ):
			codon = self.sequence[i:i+3]
			if codon in self.start:
				codon = termcolor.colored( codon, 'yellow', 'on_green', attrs=['bold'] )
			if codon in self.stop:
				codon = termcolor.colored( codon, 'white', 'on_red', attrs=['bold'] )
			coloured_sequence += codon + sep
			i += 3
	
		return coloured_sequence
		
	def generate_frameshift_sequence( self ):
		"""
		Method to generate a sequence with frameshifts defined by frameshifts and
		frame_lengths
		"""
		self.initialise_frameshift_params()
		
		frameshift_sequence = ""
		
		# convert all frames to values on {0,1,2}
		self.frameshifts = map( lambda x: x % 3, self.frameshifts )
	
		# make sure that there are as many shifts as lengths
		try:
			assert len( self.frameshifts ) == len( self.frame_lengths )
		except:
			raise ValueError( "The number of frameshifts (%d) does not match the number of frame lengths (%d)." % ( len( self.frameshifts ), len( self.frame_lengths )))
	
		# check to make sure that you don't have null frame shifts e.g. 1 -> 1
		null_shifts = 0
		for j in xrange( len( self.frameshifts )-1 ):
			change = self.frameshifts[j+1] - self.frameshifts[j]
			if change == 0:
				null_shifts += 1
	
		if null_shifts > 0:
			raise ValueError( "Null shifts found (%d): %s" % ( null_shifts, ", ".join( map( str, frameshifts ))))
	
		# for each shift
		for i in xrange( len( self.frameshifts )-1 ): # exclude the last frame shift
			if i == 0: 
				# this is the beginning
				frameshift_sequence = self._initialise_sequence( self.frameshifts[i] )
				# generate Ni non-stop codons
				frameshift_sequence = self._generate_nonstop_codon( frameshift_sequence, self.frame_lengths[i] )
				# add a stop: terminate( sequence )
				frameshift_sequence = self._generate_stop_codon( frameshift_sequence )
				change = self.frameshifts[i+1] - self.frameshifts[i]
				# change frame: change_frame( sequence, from, to )
				frameshift_sequence = self._change_frame( frameshift_sequence, change )
				continue
			else: # middle of sequence
				frameshift_sequence = self._generate_nonstop_codon( frameshift_sequence, self.frame_lengths[i] )
				frameshift_sequence = self._generate_stop_codon( frameshift_sequence )
				change = self.frameshifts[i+1] - self.frameshifts[i]
				frameshift_sequence = self._change_frame( frameshift_sequence, change )
	
		# the last frame
		frameshift_sequence = self._generate_nonstop_codon( frameshift_sequence, self.frame_lengths[i+1] )
		frameshift_sequence = self._generate_stop_codon( frameshift_sequence )
		
		# make the sequence
		self.sequence = frameshift_sequence
		self.length = len( self.sequence )
		self.is_frameshift = True
	
	def _initialise_sequence( self, frame ):
		"""
		Internal method to initialise a frameshift sequence
		"""
		# fix frame to 0-2
		frame = frame % 3
		if frame == 0:
			return random.choice( self.start )
		elif frame == 1:
			return random.choice( 'ACGU' ) + random.choice( self.start )
		elif frame == 2:
			return random.choice( 'ACGU' ) + random.choice( 'ACGU' ) + \
			random.choice( self.start )
			
	def _generate_nonstop_codon( self, sequence, length ):
		"""
		Internal method to generate a non-stop codon
		"""
		final_length = len( sequence ) + length
		while len( sequence ) < final_length:
			sequence += random.choice( self.non_stops )
#		print len( sequence ) - final_length
		return sequence
	
	def _generate_stop_codon( self, sequence ):
		"""
		Internal method to generate a stop codon
		"""
		return sequence + random.choice( self.stop )
	
	def _change_frame( self, sequence, change ):
		"""
		Internal method to change frame by change
		"""
		# check whether the sequence is terminated by a stop; raise error
		the_stop = sequence[-3:]
		try:
			assert the_stop in self.stop
		except:
			raise ValueError( "Terminal sequence not stop: %s" % sequence[-3:] )
	
		if change == 1 or change == -2:
			sequence += random.choice( 'ACGU' )
		elif change == 2 or change == -1:
			sequence += random.choice( 'ACGU' ) + random.choice( 'ACGU' )
	
		return sequence
		
	def initialise_frameshift_params( self ):
		"""
		Method to initialise a sequence for frameshifting
		"""
		# make sure that self.min_length < self.max_length
		try:
			assert self.min_length < self.max_length
		except:
			raise ValueError( "Minimum length is greater or equal to maximum sequence length!" )
		
		self.sequence = None
		if self.frameshifts is None:
			self.frameshifts = self._generate_frameshifts( self.no_of_shifts )
		if self.frame_lengths is None:
			self.frame_lengths = self._generate_frame_lengths( self.no_of_shifts, self.min_length, self.max_length )
	
	def _generate_frameshifts( self, no_of_shifts ):
		"""
		Internal method to generate a valid frameshift sequence
		"""
		frameshifts = [ random.choice( range( 3 ))]
		for i in xrange( no_of_shifts-1 ):
			if frameshifts[i] == 0:
				frameshifts.append( random.choice([ 1, 2 ]))
			elif frameshifts[i] == 1:
				frameshifts.append( random.choice([ 0, 2 ]))
			elif frameshifts[i] == 2:
				frameshifts.append( random.choice([ 0, 1 ]))
	
		return frameshifts
	
	def _generate_frame_lengths( self, no_of_shifts, min_length, max_length ):
		"""
		Internal method to generate a frame_lengths to use
		"""
		# only use lengths divisible by three between min_length and max_length
		# to ensure min_length, max_length are included use the formula below
		length_range = range( min_length+(3-min_length % 3)%3, (max_length-max_length%3)+1, 3 )
		return [ random.choice( length_range ) for i in xrange( no_of_shifts )]
