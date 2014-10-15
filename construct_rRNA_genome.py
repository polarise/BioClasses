#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import division
import sys
import pysam

def main( gtf_fn, genome_fn ):
	fastafile = pysam.Fastafile( genome_fn )
	
	with open( gtf_fn ) as f:
		for row in f:
			l = row.strip( "\n" ).split( "\t" )
			if l[2] != "transcript":
				continue
			# chrom, start, stop
			chrom = l[0]
			start = int( l[3] )
			stop = int( l[4] )
			
			# build the region string
			region = "%s:%s-%s" % ( chrom, start - 1, stop - 1 ) # 0-based
			
			sequence = fastafile.fetch( region=region )
			
			if sequence == "":
				print >> sys.stderr, "Blank for transcript:%s..." % region
			else:		
				print ">transcript:%s" % region
				print sequence.upper()
	
	with open( gtf_fn ) as f:
		for row in f:
			l = row.strip( "\n" ).split( "\t" )
			if l[2] != "exon":
				continue
			# chrom, start, stop
			chrom = l[0]
			start = int( l[3] )
			stop = int( l[4] )
			
			# build the region string
			region = "%s:%s-%s" % ( chrom, start - 1, stop - 1 ) # 0-based
			
			sequence = fastafile.fetch( region=region )
			
			if sequence == "":
				print >> sys.stderr, "Blank for exon:%s..." % region
			else:		
				print ">exon:%s" % region
				print sequence.upper()

if __name__ == "__main__":
	try:
		gtf_fn = sys.argv[1]
	except IndexError:
		print >> sys.stderr, "usage: script.py <gtf_fn>"
		sys.exit( 1 )
	
	try:
		genome_fn = sys.argv[2]
	except IndexError:
		print >> sys.stderr, "Warning: trying with human genome..."
		genome_fn = "/home/paul/bioinf/Resources/H_sapiens/full_genome/hg19.fa"
	
	main( gtf_fn, genome_fn )
