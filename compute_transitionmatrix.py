#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import division
import sys
from Bio import SeqIO

def main( fn ):
	matrix = dict()
	c = 0
	codon_count = 0
	for seq_record in SeqIO.parse( fn, "fasta" ):
		if c > 100: break
		sequence = str( seq_record.seq )
		i = 0
		while i <= len( sequence ) - 6:
			codon_count += 1
			codon = sequence[i:i+3]
			next_codon = sequence[i+3:i+6]
			if codon not in matrix:
				matrix[codon] = dict()
			if next_codon not in matrix[codon]:
				matrix[codon][next_codon] = 1
			else:
				matrix[codon][next_codon] += 1
			i += 3
		c += 1
	print matrix
	
	# validation that computation is correct
	# another_codon_count = 0
	# for c in matrix:
	# 	for n in matrix[c]:
	# 		another_codon_count += matrix[c][n]
	#
	# print codon_count
	# print another_codon_count

if __name__ == "__main__":
	try:
		fn = sys.argv[1]
	except IndexError:
		raise IOError( "Missing input FASTA file" )
	
	main( fn )