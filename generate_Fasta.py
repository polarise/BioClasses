#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import division
import sys
import random
import itertools

def main():
	starts = [ 'ATG' ]
	stops = [ 'TAA', 'TAG' ]
	bases = 'ACGT'
	itercodons = itertools.product( bases, repeat=3 )
	non_stops = [ "".join( codon ) for codon in itercodons ]
	for stop in stops:
		non_stops.remove( stop )
	
	with open( "a_fasta.fa", 'w' ) as f:	
		codon_count = dict()
		for i in xrange( 1000 ):
			print >> f, ">sequence%s" % i
			codon = random.choice( starts )
			if codon not in codon_count:
				codon_count[codon] = 1
			else:
				codon_count[codon] += 1
			sequence = codon
			for j in xrange( 200 ):
				codon = random.choice( non_stops )
				sequence += codon
				if codon not in codon_count:
					codon_count[codon] = 1
				else:
					codon_count[codon] += 1
			codon = random.choice( stops )
			sequence += codon
			if codon not in codon_count:
				codon_count[codon] = 1
			else:
				codon_count[codon] += 1
			
			print >> f, sequence
	
	for c in codon_count:
		print "%s\t%s" % ( c, codon_count[c] )
		
if __name__ == "__main__":
	main()