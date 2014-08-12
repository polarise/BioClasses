#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import sys
from Bio import SeqIO

def main( fn ):
	count = 0
	bad = 0
	for seq_record in SeqIO.parse( fn, "fasta" ):
		sequence = str( seq_record.seq )
		seq_name = seq_record.id
		if sequence.find( "N" ) >= 0:
			bad += 1
		else:
			print ">%s" % seq_name
			print sequence
		count += 1
		
	print >> sys.stderr, "%s of %s were removed" % ( bad, count )
	
if __name__ == "__main__":
	try:
		fn = sys.argv[1]
	except IndexError:
		raise IOError( "Missing FASTA file." )
	
	main( fn )