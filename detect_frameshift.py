#!/usr/bin/env python
from __future__  import division
import sys
import itertools
import random
import termcolor
import Sequence

itercodons = itertools.product( 'ACGU', repeat=3 )
non_stops = [ "".join( codon ) for codon in itercodons ]
non_stops.remove( "UAA" )
non_stops.remove( "UAG" )

start = [ 'AUG' ]
stop = [ 'UAA', 'UAG' ]

def get_start_frames( sequence ):
	"""
	given a sequence returns start site and first stop site for each frame
	"""
	start_frames = dict()
	for i in xrange( 3 ):
		start_frames[i] = {'start':-1, 'stop':-1}
		found_start = False
		for j in xrange( i, len( sequence )-3, 3 ):
			codon = sequence[j:j+3]
			if codon in start and not found_start:
				start_frames[i]['start'] = j
				found_start = True
			if codon in stop:
				start_frames[i]['stop'] = j
				break
	
	return start_frames

def get_start_pos( sequence, frame ):
	for i in xrange( frame, len( sequence ), 3 ):
		codon = sequence[i:i+3]
		if codon in start:
			return i
	return -1

def get_stop_pos( sequence, pos=0, frame=0 ):
	# the sum of pos and change should be >= 0
	try:
		assert pos + frame >= 0
	except:
		raise ValueError( "Invalid values for 'pos' (%d) and 'change' (%d)!" % ( pos, frame ))
		
	# the frame should be confined to -2...2
	try:
		assert frame in [ -2, -1, 0, 1, 2 ]
	except:
		raise ValueError( "Invalid value for frame: %d" % frame )	
	
	for i in xrange( pos+frame, len( sequence[pos+frame:] ), 3 ):
		codon = sequence[i:i+3]
		if codon in stop:
			return i
	return -1
		
def f1( sequence ):
	stop_poss = [ sequence.find( st ) for st in stop ]
	min_stop_pos = map( lambda x: x if x > 0 else 4000000000, stop_poss )
	return min( min_stop_pos )
		

def f2( sequence, stop_pos ):
	return sequence[stop_pos:]
	
def get_stop_pos2( sequence ):
	stop_poss = list()
	while len( sequence ) > 0:
		stop_pos = f1( sequence ) # get the position of the stop codon
		print sequence, len( sequence ), stop_pos
		print
		if stop_pos < 0:
			break
		else:
			stop_poss.append( stop_pos )
			sequence = f2( sequence, stop_pos ) # get the subsequence
	
	return stop_poss


def get_internal_frames( sequence, start_frames ):
	"""
	given a sequence returns the first stop site for each frame
	"""	
	for frame in start_frames:
		stop_pos = start_frames[stop]
		# for each shift get the distance to the first stop
		for change in [ -2, -1, 1, 2 ]:
			subsequence = shift_frame( sequence, stop_pos, change )
			start_frames = get_start_frames( subsequence )
			get_internal_frames( subsequence, start_frames )


def get_stop_position( sequence, stop_pos, change ):
	"""
	given a sequence, stop site finds the next stop in change frame
	"""
	for change in [ -2, -1, 1, 2 ]:
		subsequence = shift_frame( sequence, stop_pos, change )
		print subsequence
	
	

def shift_frame( sequence, pos, change ):
	"""
	given a sequence returns the frameshifted subsequence starting at pos
	"""
	return sequence[pos+change:]


def main():
 	s = 'AUGGAAGAAGAAGAAGAAGAAGAAGAAGAAGAAUAGGAAGAAGAAGAAGAAGAAGAAGAAGAAGAAGAAUAG'
 	s = Sequence.Sequence( no_of_shifts=3, min_length=50, max_length=100 )
 	s.generate_frameshift_sequence()
 	print s.info()
 	print s
 	print
 	
 	print get_stop_pos2( str( s ))
 	
# 	start_poss = list()
# 	for i in xrange( 3 ):
# 		start_poss = get_start_pos( s, i )
# 		stop_pos = get_stop_pos( s )
 	
 	
 	
# 	start_frames = get_start_frames( s )
# 	for i in start_frames:
# 	 	print "%d: start = {0}; stop = {1}".format( start_frames[i]['start'], start_frames[i]['stop'] )
# 	get_stop_position( s, start_frames )
 	
 	
# 	print
# 	s = Sequence.Sequence( no_of_shifts=2, min_length=50, max_length=100 )
# 	s.generate_frameshift_sequence()
# 	print s.info()
# 	for i in xrange( 3 ):
# 		print i,":",s.colour_frame( i, sep="" )
# 	print get_start_frames( str( s ))


if __name__ == "__main__":
	main()
