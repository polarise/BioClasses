#!/usr/bin/env python
import sys
from Sequence import *
from Tree import *
from Bio import SeqIO

def main( fasta_file ):
	bad_sequence = [ "comp1705_c0_seq1", "comp1716_c0_seq1", "comp1809_c0_seq1", "comp2102_c0_seq1", "comp2215_c0_seq1", "comp2215_c0_seq2", "comp2216_c0_seq1", "comp2216_c0_seq2" ]
	c = 0
	for seq_record in SeqIO.parse( fasta_file, "fasta" ):
		if c > 10: break
		if seq_record.id.split( " " )[0] in bad_sequence:
			continue
		fname = seq_record.id.split( " " )[0] + ".fa"
		sequence = str( seq_record.seq )
		# first_start = sequence.find( "ATG" )
# 		if first_start < 0:
# 			print >> sys.stderr, "Missing start codon in sequence %s" % seq_record.id
# 			continue
# 		else:
# 			sequence = sequence[first_start:]
		s = Sequence( sequence )
		# s.truncaste()
		s.build_tree()
		with open( fname, 'w' ) as f:
			for k in s.frameshift_sequences:
				F = s.frameshift_sequences[k] # a FrameshiftSequence object
				print >> f, ">%s" % "|".join( map( lambda x: "%s:%s" % x, F.path )) + ";" + ",".join( F.signals )
				print >> f, F.frameshifted_sequence
		c += 0

if __name__ == "__main__":
	try:
		fasta_file = sys.argv[1]
	except IndexError:
		raise InputError( "Missing input file" )
	
	main( fasta_file )