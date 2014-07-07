#!/usr/bin/env python
from __future__ import division
import sys
import math
from Bio import SeqIO

hexamers = dict()
with open( "/home/paul/bioinf/Translational_Frameshifting/2_Euplotes_data/Crassus-NEWBLER.hexamer.tab" ) as f:
	for row in f:
		if row[0] == 'h': continue
		l = row.strip( "\n" ).split( "\t" )
		hexamers[l[0]] = float( l[1] )

def log_likelihood( sequence ):
	# get the position of the first start
	# it has to be divisible by three
	#start_pos = 0
	#"""
	i = 0
	start_found = False
	start_pos = -1
	while not start_found:
		if sequence[i:i+3] == "ATG":
			start_pos = i
			start_found = True
		else:
			if i < len( sequence ):
				i += 3
			else:
				break
	
	if start_pos < 0:
		return 0, -1
	#"""
	
	j = start_pos
	loglik = 0
	while j < len( sequence ):
		hexamer = sequence[j:j+6]
		if len( hexamer ) < 6:
			break
		hex_score = hexamers[hexamer]
		loglik += math.log( hex_score )
		j += 3
	return loglik, start_pos

def no_frames( sequence ):
	# parse something like this: >1:49|0:60|1:70|0:-1;GTATAA,TTATAG,TTGTAA
	frames, signals  = sequence.split( ";" )
	frame_count = len( frames.split( "|" ))
	return frames, signals, frame_count

def main( fasta_file ):
	# read each sequence
	for seq_record in SeqIO.parse( fasta_file, "fasta" ):
		frames, signals, frame_count = no_frames( seq_record.id )
		loglik, start_pos = log_likelihood( str( seq_record.seq ))
		length = len( str( seq_record.seq ))
		orf_length = length - start_pos
		
		actual_frame_count = frame_count
		for F in frames.split( "|" )[:-1]:
			if int( F.split( ":" )[1] ) < start_pos:
				actual_frame_count -= 1
		
		score = loglik/frame_count
		actual_score = abs( loglik/( actual_frame_count*math.sqrt( orf_length )))
		
		if signals == "":
			signals = "None"
		print "\t".join( map( str, [ frames, signals, length, orf_length, frame_count, actual_frame_count, loglik, start_pos, score, actual_score ] ))

if __name__ == "__main__":
	try:
		fasta_file = sys.argv[1]
	except IndexError:
		raise InputError( "Missing input file" )
	
	main( fasta_file )