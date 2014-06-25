# -*- encoding: utf-8 -*-
from __future__ import division
import sys
import itertools
import random
import math
import termcolor

class Sequence( object ):
	"""
	The base class
	"""
	def __init__( self, sequence=None, length=None, bases='ACGU', starts=[ 'AUG' ], stops=[ 'UAA', 'UAG' ] ):
		"""
		Initialise a Sequence object
		"""
		# basic stuff
		self.bases = bases
		self.starts = starts
		self.stops = stops
		
		itercodons = itertools.product( self.bases, repeat=3 )
		self.non_stops = [ "".join( codon ) for codon in itercodons ]
		for stop in self.stops:
			self.non_stops.remove( stop )
		
		self.length = length
		self.sequence = sequence
		self.binary_codon_matrix = None
		
		self.is_frameshift = False
		self.as_codons = False
		
		self.stop_positions = dict()
		self.stop_sequence = list()
	
	#*****************************************************************************
	
	def all_colour_frames( self, sep=" " ):
		all_coloured_sequences = ""
		pass
	
	#*****************************************************************************
	
	def colour_frame( self, frame, sep=" " ):
		"""
		Method to return in colour for frame frame
		"""
		# ensure that you have a valid frame; no need for errorcheck
		frame = frame % 3
		
		coloured_sequence = ""
	
		# front
		codon = self.sequence[0:frame]
		if codon in self.starts:
			codon = termcolor.colored( codon, 'yellow', 'on_yellow', attrs=['bold'] )
		elif codon in self.stops:
			codon = termcolor.colored( codon, 'white', 'on_red', attrs=['bold'] )
		elif codon in self.non_stops:
			codon = termcolor.colored( codon, 'blue', 'on_white', attrs=['bold'] )
		else:
			codon = termcolor.colored( codon, 'red', 'on_green', attrs=['bold'] )
	
#		if frame % 3 != 0:
		coloured_sequence += codon + sep
	
		# body
		i = frame
		while i < len( self.sequence ):
			codon = self.sequence[i:i+3]
			if codon in self.starts:
				codon = termcolor.colored( codon, 'yellow', 'on_green', attrs=['bold'] )
			elif codon in self.stops:
				codon = termcolor.colored( codon, 'white', 'on_red', attrs=['bold'] )
			elif codon in self.non_stops:
				codon = termcolor.colored( codon, 'blue', 'on_white', attrs=['bold'] )
			else:
				codon = termcolor.colored( codon, 'red', 'on_green', attrs=['bold'] )
			coloured_sequence += codon + sep
			i += 3
		
		return coloured_sequence
	
	#*****************************************************************************
	
	def __repr__( self ):
		sequence = list()
		if self.as_codons:
			for i in xrange( 0, len( self.sequence ), 3 ):
				sequence.append( self.sequence[i:i+3] )
			return " ".join( sequence )
		else:
			return self.sequence
	
	#*****************************************************************************
		
	def info( self, comment="" ):
		raise NotImplementedError
	
	#*****************************************************************************
	
	def binary_frame( self, frame, sep=" " ):
		"""
		Method that returns a binary codon sequence: 0 - stop; 1 - non-stop;
		red: stop; blue: start
		"""
		binary_sequence = ""
			
		# body
		i = frame
		while i < self.length + frame:
			if i < 0:
				bit = termcolor.colored( "0", 'red', 'on_green', attrs=['bold'] )			
			else:
				codon = self.sequence[i:i+3]
				if codon in self.starts:
					bit = termcolor.colored( "1", 'white', 'on_blue', attrs=['bold'] )
				elif codon in self.stops:
					bit = termcolor.colored( "0", 'white', 'on_red', attrs=['bold'] )
				elif codon in self.non_stops:
					bit = termcolor.colored( "1", 'blue', 'on_white', attrs=['bold'] )
				else:
					bit = termcolor.colored( "0", 'red', 'on_green', attrs=['bold'] )
			binary_sequence += bit + sep
			i += 3
		
		return binary_sequence
	
	#*****************************************************************************
		
	def codon_frame_vector( self, frame, SS=10, ES=0, NS=1, IS=-1, weighted_start=False ):
		"""
		SS - start codon score
		ES - stop (end) codon score
		NS - non-stop codon score
		IS - incomplete codon score
		"""
		frame_vector = list()
		
		# body
		i = frame
		while i < self.length + frame:
			if i < 0:
				ind = IS
			else:
				codon = self.sequence[i:i+3]
				if codon in self.starts:
					if weighted_start:
						ind = max( NS, SS - len( frame_vector )) # arbitrary value
					else:
						ind = SS
				elif codon in self.stops:
					ind = ES
				elif codon in self.non_stops:
					ind = NS
				else:
					ind = IS
			frame_vector.append( ind )
			i += 3
		
		return frame_vector
	
	#*****************************************************************************
	
	def set_binary_codon_matrix( self, min_frame=-2, max_frame=2, SS=10, ES=0, NS=1, IS=-1, weighted_start=False ):
		self.binary_codon_matrix = dict()
		for i in xrange( min_frame - 2, max_frame + 3, 1 ):
			row = self.codon_frame_vector( i, SS, ES, NS, IS, weighted_start )
			self.binary_codon_matrix[i] = row
			
	#*****************************************************************************
	
	def show_binary_codon_matrix( self ):
		keys = self.binary_codon_matrix.keys()
		keys.sort( reverse=True )
		
		max_frame = max( map( abs, keys ))
		rjust_int = int( math.floor( math.log( max_frame, 10 ) + 1 ))
		
		output_str = "BinaryCodonMatrix of length %d:\n" % len( self.binary_codon_matrix[0] )
		for k in keys:
			if k > 0:
				output_str += "+%s: %s\n" % ( str( k ).rjust( rjust_int ), " ".join( map( lambda x: x.rjust( 2 ), map( str, self.binary_codon_matrix[k] ))))
			elif k == 0:
				output_str += " %s: %s\n" % ( str( k ).rjust( rjust_int ), " ".join( map( lambda x: x.rjust( 2 ), map( str, self.binary_codon_matrix[k] ))))
			elif k < 0:
				output_str += "%s: %s\n" % ( str( k ).rjust( rjust_int ), " ".join( map( lambda x: x.rjust( 2 ), map( str, self.binary_codon_matrix[k] ))))
		
		return output_str.strip( "\n" )
	
	#*****************************************************************************
	
	"""
	
	"""
	def dist_to_stop( self, frame, pos=0 ):
		if self.binary_codon_matrix is None: # set the binary codon matrix if it's not set yet
			print >> sys.stderr, "Setting binary codon matrix...", 
			self.set_binary_codon_matrix()
			print >> sys.stderr, "DONE"

		# make sure frame is is a valid number
		try:
			frame in self.binary_codon_matrix
		except KeyError:
			raise ValueError( "Invalid frame (%d) against available frames (%s)" % ( frame, ",".join( map ( str, self.binary_codon_matrix.keys() ))))
		
		dist = 0
		score = 0
#		found_stop = False
		codon = self.binary_codon_matrix[frame][pos]
		
		if codon <= 0:
			stop_reached = True
			pos += 1
		else:
			stop_reached = False
			end_reached = False
		
		while not stop_reached:
			try:
				codon = self.binary_codon_matrix[frame][pos]
			except IndexError:
				break # stop not reached but end reached
			if codon >= 1:
				dist += 1
				score += codon
			elif codon <= 0:
				stop_reached = True
			pos += 1
		
		# set end_reached flag if necessary
		try:
			codon = self.binary_codon_matrix[frame][pos]
			if codon < 0:
				end_reached = True
		except IndexError:
			end_reached = True
			
#		while not reached_end:
#			try:
#				codon = self.binary_codon_matrix[frame][pos]
#			except IndexError:
#				break
#			if codon > 0:
#				dist += 1
#				score += codon
#			elif codon == 0:
#				return dist, score
#			elif codon < 0:
#				reached_end = True
#			pos += 1	
		
#		while not reached_end:
#			try:
#				codon = self.binary_codon_matrix[frame][pos]
#			except IndexError:
#				reached_end = True
#				continue
#			
#			if codon == 0: # found a stop
#				found_stop = True
#			elif codon < 0: # found the end
#				reached_end = True
#			else:
#				dist += 1
#				pos += 1
#				score += codon
#			except IndexError:
#				reached_end = True
				
		return dist, score, end_reached
			
	#*****************************************************************************
	
	def dist_to_stop2( self, frame, pos=0 ):
		dist = 0
		score = 0
		end_reached = False
		
		while not end_reached:
			try:
				codon = self.binary_codon_matrix[frame][pos]
			except IndexError:
				end_reached = True
				return dist, score, end_reached
			
			try:
				next_codon = self.binary_codon_matrix[frame][pos+1]
			except IndexError:
				next_codon = -1
				end_reached = True
				
			if codon == 0 and next_codon < 0:
				return dist, score, end_reached
			elif codon >= 1 and next_codon == 0:
				dist += 1
				score += codon
				end_reached = True
				return dist, score, end_reached
			elif codon >= 1 and next_codon < 0:
				dist += 1
				score += codon
				end_reached = True
				return dist, score, end_reached
			elif codon >= 1 and next_codon >= 1:
				dist += 1
				score += codon
			pos += 1
	
	#*****************************************************************************
	
	def get_best_frame( self, frame, pos=0 ):
		frames = self.binary_codon_matrix.keys()
		max_frame = max( frames )
		min_frame = min( frames )
		
		# determine the frame range to search
#		frame_range = range( min( max_frame, frame + 2 ), max( min_frame, frame - 3 ), -1 )
		frame_range = range( 3 )
		frame_range.remove( frame ) # exclude the current frame
		
		best_frame = None
		orf_length = 0
		orf_score = 0
		for i in frame_range:
			d, s, er = self.dist_to_stop( i, pos )
			if best_frame is None:
				orf_length = d
				orf_score = s
				best_frame = i
			else:
				if d > orf_length:
					orf_length = d
					orf_score = s
					best_frame = i
		
		end_reached = er
		
		return best_frame, orf_length, orf_score, end_reached
	
	#*****************************************************************************
	
	def get_stop_positions( self ):
		"""
		Method to return the position of stop codons in all frames
		"""		
		stop_pos = dict()
		
		for frame in xrange( 3 ):
			i = frame
			while i < self.length:
				codon = self.sequence[i:i+3]
				if codon in self.stops:
					stop_pos[i] = frame
					# if i not in stop_pos:
					# 	stop_pos[i] = [ frame ]
					# else:
					# 	stop_pos[i] += [ frame ]
				i += 3

		return stop_pos
		
	#*****************************************************************************
	
	def get_stop_sequence( self ):
		self.stop_positions = self.get_stop_positions()
		positions = self.stop_positions.keys()
		positions.sort()
		
		self.stop_sequence = list()
		for p in positions:
			self.stop_sequence.append( ( self.stop_positions[p], p ))
		
	
#*******************************************************************************

class RandomSequence( Sequence ):
	def __init__( self, length ):
		super( RandomSequence, self ).__init__( length=length )
	
	def info( self, comment="" ):
		return "Random sequence of length %d: %s" % ( self.length, comment )

	def generate( self ):
		"""
		Method to generate a random sequence of lenght length
		"""
		self.sequence = ""
		while len( self.sequence ) < self.length:
			self.sequence += random.choice( self.bases )
			
#*******************************************************************************

class RandomFSSequence( Sequence ):
	def __init__( self, frameshifts=None, frame_lengths=None, no_of_shifts=None, min_length=None, max_length=None ):
		super( RandomFSSequence, self ).__init__()
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
	
#*******************************************************************************
	
class BiologicalSequence( RandomFSSequence ):
	def __init__( self, sequence ):
		super( BiologicalSequence, self ).__init__( sequence )
		self.sequence = sequence
		self.length = len( sequence )
	
		# must have a valid binary codon matrix
		self.set_binary_codon_matrix( weighted_start=True )
		
		self.frameshifted_sequence = None
		self.path = None
		self.fragments = list()
		
	#*****************************************************************************
	
	def info( self, comment="" ):
		return "Unknown biological sequence of length %s bases." % self.length
	
	#*****************************************************************************
	
	def detect_frameshifts( self, frame=0 ):
		self.frameshifts = list() # initialise
		self.frame_lengths = list()
		self.frame_scores = list()
		self.overall_score = None
		
		self.frameshifts.append( frame )
		
		l, s, er = self.dist_to_stop( frame )
		end_reached = er
		
		pos = l + 1
		score = s
		
		self.frame_lengths.append( l )
		self.frame_scores.append( s )
		
		print "frame\tpos\tscore\tf\tl\ts\tend?"
		print "%d\t%d\t%d\t%s\t%d\t%d\t%s" % ( frame, pos, score, frame, l, s, end_reached )

		while not end_reached:
			f, l, s, er = self.get_best_frame( frame, pos )	# frame, length, score
			end_reached = er
			frame = f
			pos += l + 1
			score += s
			print "%d\t%d\t%d\t%s\t%d\t%d\t%s" % ( frame, pos, score, frame, l, s, end_reached )
			self.frameshifts.append( f )
			self.frame_lengths.append( l )
			self.frame_scores.append( s )
		
		self.no_of_shifts = len( self.frameshifts ) - 1
		self.overall_score = sum( self.frame_scores )
		
	#*****************************************************************************	
	
	def detect_frameshifts2( self ):
		"""
		Alternative algorithm to detect frameshifts: the sequence with the longest
		frames corresponds with the a sequence defined as follows:
		- the first frame is the third 
		- every other frame except the current frame and the next frame i.e. every second unique frame
		"""
		stop_pos = dict()
		frame_scores = dict()
		for frame in xrange( 3 ):
			pos = 0
			score = 0
			matrix_length = len( self.binary_codon_matrix[frame] )
			end_reached = False
#			while pos < matrix_length:
			while not end_reached:
				d, s, er = self.dist_to_stop( frame, pos )
				end_reached = er
				pos += d + 1
				score += s
				if pos not in stop_pos:
					stop_pos[pos] = [ frame ]
				else:
					stop_pos[pos] += [ frame ]
				frame_scores[frame] = score
		
		print stop_pos
		print frame_scores
		
		keys = stop_pos.keys()
		keys.sort()
		
		stop_sequence = list()
		for k in keys:
			stop_sequence.append( stop_pos[k][0] )
			
		print stop_sequence
		
		frameshifts = list()
		ignore = set()
		for s in stop_sequence:
			if len( ignore ) < 2:
				ignore.add( s )
			elif s in ignore:
				pass
			else:
				frameshifts.append( s )
				ignore = set()
				ignore.add( s )
		
		print frameshifts
		
	#*****************************************************************************
	
	def frameshift_from_path( self, path ):
		"""
		"""
		# first get all frame of self.sequence
		sequence_in_frames = dict()
		for i in xrange( 3 ):
			sequence_in_frames[i] = self.sequence[i:]
		
		#for f in sequence_in_frames:
			#print f, ":", sequence_in_frames[f]
		#print "    " + "         |"*(( self.length )//10 )
		#print
		
		self.frameshifted_sequence = ""
		self.fragments = list()
		i = 0
		f_i = 0
		for f,j in path:
			self.frameshifted_sequence += self.sequence[i+(f-f_i):j]
			self.fragments.append( self.sequence[i+(f-f_i):j] )
			i = j
			f_i = f
			# we could factor in the last trivial frameshift...
		self.frameshifted_sequence += self.sequence[-1]
		self.fragments[-1] += self.sequence[-1]
			# or (preferably) allow the last fragment to run until the end
			#self.frameshifted_sequence += self.sequence[j:]
			#self.fragments[-1] += self.sequence[-1]
		
		self.path = path
			
		return self.frameshifted_sequence, self.fragments
	
	def colour_frameshifted_sequence( self, frame=0, sep=" " ):
		"""
		Method to return in colour for frame frame
		"""
		# ensure that you have a valid frame; no need for errorcheck
		frame = frame % 3
		
		coloured_sequence = ""
	
		# front
		codon = self.frameshifted_sequence[0:frame]
		if codon in self.starts:
			codon = termcolor.colored( codon, 'yellow', 'on_yellow', attrs=['bold'] )
		elif codon in self.stops:
			codon = termcolor.colored( codon, 'white', 'on_red', attrs=['bold'] )
		elif codon in self.non_stops:
			codon = termcolor.colored( codon, 'blue', 'on_white', attrs=['bold'] )
		else:
			codon = termcolor.colored( codon, 'red', 'on_green', attrs=['bold'] )
	
#		if frame % 3 != 0:
		coloured_sequence += codon + sep
	
		# body
		i = frame
		while i < len( self.frameshifted_sequence ):
			codon = self.frameshifted_sequence[i:i+3]
			if codon in self.starts:
				codon = termcolor.colored( codon, 'yellow', 'on_green', attrs=['bold'] )
			elif codon in self.stops:
				codon = termcolor.colored( codon, 'white', 'on_red', attrs=['bold'] )
			elif codon in self.non_stops:
				codon = termcolor.colored( codon, 'blue', 'on_white', attrs=['bold'] )
			else:
				codon = termcolor.colored( codon, 'red', 'on_green', attrs=['bold'] )
			coloured_sequence += codon + sep
			i += 3
		
		return coloured_sequence