#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import division
import sys
from AminoAcid import *
from Bio import SeqIO

def main( fn, fastafile ):
	aa_dict = dict()
	codon_dict = dict()
	with open( fn ) as f:
		for row in f:
			l = row.strip( "\n" ).split( "\t" )
			aa_dict[l[0]] = AminoAcid( *l[:-1] )
			for c in l[3].split( "," ):
				codon_dict[c] = l[0]
	
	print aa_dict, len( aa_dict )
	print
	print codon_dict, len( codon_dict )
	print
	for a in aa_dict:
		print aa_dict[a]
		print
	
	
	# read in the data from the fasta file
	for seq_record in SeqIO.parse( fastafile, 'fasta' ):
		sequence = str( seq_record.seq )
		
		# get the position of the first ATG
		# make sure it's in the first coding frame
		# count the amino acids
	
	# normalise each amino acid
	

if __name__ == "__main__":
	try:
		fn = sys.argv[1]
		fastafile = sys.argv[2]
	except IndexError:
		raise IOError( "Missing genetic code definition file." )
		sys.exit( 1 )
	main( fn )