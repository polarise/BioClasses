#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import division
import sys
from AminoAcid import *
from Bio import SeqIO

class ORFInfo( object ):
	def __init__( self, name, last, frame ):
		self.name = name
		self.last = int( last ) - 1 # 0-based
		self.frame = int( frame ) - 1 # 0-based

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
	
	#print genetic_code, len( genetic_code )
	#print
	#print codon_dict, len( codon_dict )
	#print
	#for a in genetic_code:
		#print genetic_code[a]
		#print
	
	orf_frame = dict()
	with open( "/home/paul/Dropbox/Euplotes/FrameshiftPredictionData/one_orfs.txt" ) as f:
		for row in f:
			if row[0] == "T":
				continue
			l = row.strip( "\n" ).split( "\t" )
			orf_frame[l[0]] = ORFInfo( *l )
	
	# read in the data from the fasta file
	total = 0
	ok_count = 0
	nok_count = 0
	for seq_record in SeqIO.parse( fastafile, 'fasta' ):
		sequence = str( seq_record.seq )
		seq_name = seq_record.id.split( " " )[0]
		
		# get the position of the first ATG
		frame = orf_frame[seq_name].frame
		last = orf_frame[seq_name].last
		i = frame
		start = None
		while i <= len( sequence ) - 3:
			codon = sequence[i:i+3]
			if codon == "ATG":
				start = i
				break
			else:
				i += 3
		
		if start == None:
			print >> sys.stderr, "Missing ATG in frame %d in sequence %s" % ( frame, seq_name )
			total += 1
			nok_count += 1
			continue
		
		#if ( last - start + 1 ) % 3 == 0:
			#ok_count += 1
			#total += 1
		#else:
			#print seq_name, start, last, ( last - start ) + 1, ( last - start + 1 ) % 3, i
			#nok_count += 1
			#total += 1
			
	#print ok_count/total, nok_count/total
	#print ok_count, nok_count, total
		
		# make sure it's in the first coding frame
		cds = sequence[start:last+1]
		
		print ">" + seq_record.id
		print cds
		
		# from the first codon to the end read in the codons as follows
		#for m in xrange( len( cds ) - 3 ):
			#codon = cds[m:m+3]
			## get the amino acid name from codon_dict
			#aa = codon_dict[codon]
			## then get the amino acid and add the codon
			#genetic_code[aa].count_codon( codon )
	
	# normalise each amino acid
	#for g in genetic_code:
		#genetic_code[g].normalise()
		#print genetic_code[g]
		#print
	

if __name__ == "__main__":
	try:
		fn = sys.argv[1]
		fastafile = sys.argv[2]
	except IndexError:
		raise IOError( "Missing genetic code definition file." )
		sys.exit( 1 )
	main( fn, fastafile )