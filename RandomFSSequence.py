# -*- encoding: utf-8 -*-
from Sequence import *

class RandomFSSequence( Sequence ):
	def __init__( self, frameshifts=None, frame_lengths=None, no_of_shifts=None, min_length=None, max_length=None, bases='ACGT', starts=[ 'ATG' ], stops=[ 'TAA', 'TAG' ] ):
		super( RandomFSSequence, self ).__init__( bases=bases, starts=starts, stops=stops )
		self.is_frameshift = True
		self.frameshifts = frameshifts
		self.frame_lengths = frame_lengths
		self.no_of_shifts = no_of_shifts
		self.min_length = min_length
		self.max_length = max_length
	
	#*****************************************************************************
	
	def info( self, comment="" ):
		return "Frameshift sequence (%s) of lengths (%s) and total length of %d: %s" % ( ",".join( map( str, self.frameshifts )), ",".join( map( str, self.frame_lengths )), self.length, comment )
	
	#*****************************************************************************

	def _initialise_sequence( self, frame ):
		"""
		Internal method to initialise a frameshift sequence
		"""
		# fix frame to 0-2
		frame = frame % 3
		if frame == 0:
			return random.choice( self.starts )
		elif frame == 1:
			return random.choice( 'ACGU' ) + random.choice( self.starts )
		elif frame == 2:
			return random.choice( 'ACGU' ) + random.choice( 'ACGU' ) + \
			random.choice( self.starts )
	
	#*****************************************************************************
			
	def _generate_nonstop_codon( self, sequence, length ):
		"""
		Internal method to generate a non-stop codon
		"""
		final_length = len( sequence ) + length
		while len( sequence ) < final_length:
			sequence += random.choice( self.non_stops )
			#		print len( sequence ) - final_length
		return sequence
		
	#*****************************************************************************
	
	def _generate_stop_codon( self, sequence ):
		"""
		Internal method to generate a stop codon
		"""
		return sequence + random.choice( self.stops )
	
	#*****************************************************************************
	
	def _change_frame( self, sequence, frame ):
		"""
		Internal method to change frame by frame
		"""
		# check whether the sequence is terminated by a stop; raise error
		the_stop = sequence[-3:]
		try:
			assert the_stop in self.stops
		except:
			raise ValueError( "Terminal sequence not stop: %s" % sequence[-3:] )
	
		if frame == 1 or frame == -2:
			sequence += random.choice( 'ACGU' )
		elif frame == 2 or frame == -1:
			sequence += random.choice( 'ACGU' ) + random.choice( 'ACGU' )
	
		return sequence
	
	#*****************************************************************************

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
	
	#*****************************************************************************
	
	def _generate_frame_lengths( self, no_of_shifts, min_length, max_length ):
		"""
		Internal method to generate a frame_lengths to use
		"""
		# only use lengths divisible by three between min_length and max_length
		# to ensure min_length, max_length are included use the formula below
		length_range = range( min_length+(3-min_length % 3)%3, (max_length-max_length%3)+1, 3 )
		return [ random.choice( length_range ) for i in xrange( no_of_shifts )]
	
	#*****************************************************************************
	
	def initialise_frameshift_params( self ):
		"""
		Method to initialise a sequence for frameshifting
		"""
		# make sure that self.min_length < self.max_length
		try:
			assert self.min_length < self.max_length
		except:
			raise ValueError( "Minimum length is greater or equal to maximum sequence length!" )
		
		# reset sequence
		self.sequence = None
		
		if self.frameshifts is None and self.frame_lengths is None:
			self.frameshifts = self._generate_frameshifts( self.no_of_shifts )
			self.frame_lengths = self._generate_frame_lengths( self.no_of_shifts, self.min_length, self.max_length )
		elif self.frameshifts is not None and self.frame_lengths is not None:
			print >> sys.stderr, "Frameshifts and frame lengths retained:", self.frameshifts, self.frame_lengths
		else:
			raise ValueError( "Non-empty frameshifts or frame_lengths:", self.frameshifts, self.frame_lengths)
	
	#*****************************************************************************

	def generate( self ):
		"""
		Method to generate a sequence with frameshifts defined by frameshifts and
		frame_lengths
		"""
		# will generate params if they don't already exist
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