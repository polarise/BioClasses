#!/usr/bin/env python
from __future__ import divisino
import sys
from BioClasses import *


def main( fn ):
	with open( fn ) as f:
		for row in f:
			l = row.strip( "\n" ).split( "\t" )
			



if __name__ == "__main__":
	try:
		fn = sys.argv[1] # refseq gtf
	except IndexError:
		print >> sys.stderr, "usage:./script.py <gtf>"
		sys.exit( 0 )
	
	main()
