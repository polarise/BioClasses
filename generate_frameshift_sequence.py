#!/usr/bin/env python
from __future__ import division
import sys
import itertools
import random
import termcolor

itercodons = itertools.product( 'ACGU', repeat=3 )
non_stops = [ "".join( codon ) for codon in itercodons ]
non_stops.remove( "UAA" )
non_stops.remove( "UAG" )

start = [ 'AUG' ]
stop = [ 'UAA', 'UAG' ]

def generate_random_sequence( length ):
	sequence = ""
	while len( sequence ) < length:
		sequence += random.choice( "ACGU" )
	
	return sequence

def colour_frame( sequence, frame, sep=" " ):
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

def initiate_sequence( frame ):
	sequence = ""
	frame = frame % 3
	if frame == 0:
		return random.choice( start )
	elif frame == 1:
		return random.choice( 'ACGU' ) + random.choice( start )
	elif frame == 2:
		return random.choice( 'ACGU' ) + random.choice( 'ACGU' ) + \
		random.choice( start )
	
def generate_nonstop_codon( sequence, length ):
	final_length = len( sequence ) + length
	while len( sequence ) < final_length:
		sequence += random.choice( non_stops )
#	print len( sequence ) - final_length
	return sequence
	
def generate_stop_codon( sequence ):
	return sequence + random.choice( stop )

def change_frame( sequence, change ):
	# check whether the sequence is terminated by a stop; raise error
	the_stop = sequence[-3:]
	try:
		assert the_stop in stop
	except:
		raise ValueError( "Terminal sequence not stop: %s" % sequence[-3:] )
	
	if change == 1 or change == -2:
		sequence += random.choice( 'ACGU' )
	elif change == 2 or change == -1:
		sequence += random.choice( 'ACGU' ) + random.choice( 'ACGU' )
	
	return sequence

def make_frameshift_sequence2( frameshifts=[ 0, 1, 2 ], frame_lengths=[ 50, 50, 50 ] ):
	global non_stops
	global starts
	global stop 
	
	frameshift_sequence = ""
	# convert all frames to values on {0,1,2}
	frameshifts = map( lambda x: x % 3, frameshifts )
	
	# make sure that there are as many shifts as lengths
	try:
		assert len( frameshifts ) == len( frame_lengths )
	except:
		raise ValueError( "The number of frameshifts (%d) does not match the number of frame lengths (%d)." % ( len( frameshifts ), len( frame_lengths )))
	
	# check to make sure that you don't have null frame shifts e.g. 1 -> 1
	null_shifts = 0
	for j in xrange( len( frameshifts )-1 ):
		change = frameshifts[j+1] - frameshifts[j]
		if change == 0:
			null_shifts += 1
	
	if null_shifts > 0:
		raise ValueError( "Null shifts found (%d): %s" % ( null_shifts, ", ".join( map( str, frameshifts ))))
	
	# for each shift
	for i in xrange( len( frameshifts )-1 ): # exclude the last frame shift
		if i == 0: # this is the beginning
			frameshift_sequence = initiate_sequence( frameshifts[i] )
			frameshift_sequence = generate_nonstop_codon( frameshift_sequence, frame_lengths[i] )
			frameshift_sequence = generate_stop_codon( frameshift_sequence )
			change = frameshifts[i+1] - frameshifts[i]
			frameshift_sequence = change_frame( frameshift_sequence, change )
			continue
		else: # middle of sequence
			frameshift_sequence = generate_nonstop_codon( frameshift_sequence, frame_lengths[i] )
			frameshift_sequence = generate_stop_codon( frameshift_sequence )
			change = frameshifts[i+1] - frameshifts[i]
			frameshift_sequence = change_frame( frameshift_sequence, change )
	
	# the remaining
	frameshift_sequence = generate_nonstop_codon( frameshift_sequence, frame_lengths[i+1] )
	frameshift_sequence = generate_stop_codon( frameshift_sequence )
			
		# generate Ni non-stop codons: generate_nonstop_codons( sequence, length, index=None )
		# add a stop: terminate( sequence )
		# change frame: change_frame( sequence, from, to )
	
	return frameshift_sequence

def generate_frameshifts( no_of_shifts ):
	frameshifts = [ random.choice( range( 3 ))]
	for i in xrange( no_of_shifts-1 ):
		if frameshifts[i] == 0:
			frameshifts.append( random.choice([ 1, 2 ]))
		elif frameshifts[i] == 1:
			frameshifts.append( random.choice([ 0, 2 ]))
		elif frameshifts[i] == 2:
			frameshifts.append( random.choice([ 0, 1 ]))
	
	return frameshifts
	
def make_frameshift_sequence( length, no_of_frameshifts, frame_zero ):
	global non_stops
	global start
	global stop
	
	# frame_zero is the starting frame
	frame_zero = frame_zero % 3 # make sure frame_zero has a right value
	
	frameshift_sequence = ""
	if frame_zero == 1:
		frameshift_sequence += random.choice( 'ACGU' )
	elif frame_zero  == 2:
		frameshift_sequence += random.choice( 'ACGU' ) + random.choice( 'ACGU' )
	
	# start with a start
	frameshift_sequence += random.choice( start )
	
	# enter a loop
	l = 1	# keep the length in mind
	i = 0 # an index to count the number of frameshifts we've introduced
	while len( frameshift_sequence ) < length:
		if i < no_of_frameshifts:
			random_codon = random.choice( non_stops + stop )
			if random_codon in stop:
				i += 1
		else:
			random_codon = random.choice( non_stops )
		frameshift_sequence += random_codon
	
	# close with a stop
	frameshift_sequence += random.choice( stop )
	
	return frameshift_sequence

def main():
	L = int( raw_input( "sequence length:    " ))
	N = int( raw_input( "no. of frameshifts: " ))
	F0 = int( raw_input( "starting frame:     " ))
	frameshift_sequence = make_frameshift_sequence( L, N, F0 )

	return frameshift_sequence

if __name__ == "__main__":
#	sequence = main()
	
#	sequence = generate_random_sequence( 99 )
#	print sequence
	
#	for i in xrange( 3 ):
#		print colour_frame( sequence, i, sep="" )
#	print
#	print
	
	no_of_shifts = random.randint( 2, 5 )
	frameshifts = generate_frameshifts( no_of_shifts )
	frame_lengths = [ random.randint( 100, 150 ) for i in xrange( no_of_shifts )]
	frameshift_sequence2 = make_frameshift_sequence2( frameshifts, frame_lengths )
	print "Frameshift sequence (%s) of lengths (%s):" % ( ",".join( map( str, frameshifts )), ",".join( map( str, frame_lengths )))
	for i in xrange( 3 ):
		print "%d:%s" % ( i, colour_frame( frameshift_sequence2, i, sep="" ))
	print "Total length: %d" % len( frameshift_sequence2 )
