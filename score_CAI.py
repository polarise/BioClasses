#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from GeneticCode import *
from Sequence import *
from Bio import SeqIO

def main( fn ):
	# read in the CAI table
	G = GeneticCode( "euplotid_genetic_code.txt" )
	G.read_CAI_table( "euplotid_CAI_table.txt" )
	
	c = 0
	for seq_record in SeqIO.parse( fn, "fasta" ):
		if c > 100: break
		sequence = str( seq_record.seq )
		s = Sequence( sequence )
		s.set_genetic_code( G )
		# s.truncate()
		s.build_tree()
		# get the first stop in the first frame
		main_orf = ""
		for m,n in s.unique_stop_sequence:
			if m == 0 and n > 0: # exclude the terminal frame markers e.g. (0,-1)
				main_orf = s.sequence[:n]
				break
		s.estimate_frameshift_CAI()
		with open( seq_record.id + ".cai", 'w' ) as f:
			if main_orf != "":
				t = Sequence( main_orf )
				t.set_genetic_code( G )
				t.estimate_CAI()
				print >> f, t.repr_as_row()
			for fs in s.frameshift_sequences:
				print >> f, s.frameshift_sequences[fs].repr_as_row()
		
		c += 1

if __name__ == "__main__":
	try:
		fn = sys.argv[1]
	except IndexError:
		raise IOError( "Missing FASTA input file." )
	main( fn )