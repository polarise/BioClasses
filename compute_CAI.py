#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import division
import sys
from AminoAcid import *
from Bio import SeqIO

def main( fn, fastafile ):
	genetic_code = dict()
	codon_dict = dict()
	with open( fn ) as f:
		for row in f:
			l = row.strip( "\n" ).split( "\t" )
			genetic_code[l[0]] = AminoAcid( *l[:-1], as_RNA=False )
			for c in l[3].split( "," ):
				c = c.replace( "U", "T" )
				codon_dict[c] = l[0]
	
	print genetic_code, len( genetic_code )
	print
	print codon_dict, len( codon_dict )
	print
	for a in genetic_code:
		print genetic_code[a]
		print
	
	
	# read in the data from the fasta file
	total = 0
	ok_count = 0
	nok_count = 0
	for seq_record in SeqIO.parse( fastafile, 'fasta' ):
		sequence = str( seq_record.seq )
		
		# get the position of the first ATG
		first_start = sequence.find( "ATG" )
		if first_start % 3 == 0:
			print sequence[:3], "OK", first_start
			ok_count += 1
			total += 1
		else:
			print sequence[:3], "NOK", first_start
			nok_count += 1
			total += 1
	
	print ok_count/total, nok_count/total
		# make sure it's in the first coding frame
		# from the first codon to the end read in the codons as follows
		# get the amino acid name from codon_dict
		# then get the amino acid and add the codon
	
	# normalise each amino acid
	

if __name__ == "__main__":
	try:
		fn = sys.argv[1]
		fastafile = sys.argv[2]
	except IndexError:
		raise IOError( "Missing genetic code definition file." )
		sys.exit( 1 )
	main( fn, fastafile )