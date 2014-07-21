#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import division
import sys
import itertools
import numpy
import datetime
import matplotlib
matplotlib.use( "Agg" )
import matplotlib.pyplot as pylab
from matplotlib.backends.backend_pdf import PdfPages

def f( x ):
	y = x.split( "," )
	return ( int( y[0].strip( " " )), int( y[1].strip( " " )))

def proc7( val ):
	l = map( f, [ v.lstrip( "," ).lstrip( "(" ) for v in val.split( ")" )[:-1] ])
	return l
	

def main( fn ):
	itercodons = itertools.product( "ACGT", repeat=3 )
	codons = [ "".join( codon ) for codon in itercodons ]
	
	hexamers = dict()
	with open( fn ) as f:
		c = 0
		for row in f:
			if c > 1000: break
			l = row.strip( "\n" ).split( "\t" )
			length = int( l[2] )
			path = proc7( l[6] )
			if len( path ) == 1	:
				pass
			else: # there are hexamers
				hexs = l[7].split( "," )
				i = 0 # index for position
				for h in hexs:
					if h not in hexamers:
						hexamers[h] = [ path[i][1]/length ]
					else:
						hexamers[h] += [ path[i][1]/length ]
					i += 1
			c += 0
	
	pdf = PdfPages( "signal_combined_histograms.pdf" )
	for codon in codons:
		h1 = codon + "TAA"
		h2 = codon + "TAG"
		try:
			# y1 = hexamers[h1]
			# y2 = hexamers[h2]
			y = hexamers[h1] + hexamers[h2]
		except KeyError:
			print >> sys.stderr, "Warning: no data for both stops for codon %s" % codon
			continue
		# y1.sort()
		# y2.sort()
		y.sort()
		pylab.hist( y, bins=100, range=( 0, 1 ), normed=False, label=codon )
		# pylab.subplot( 211 )
		# pylab.hist( y1, bins=100, range=( 0, 1 ), label=h1 )
		# pylab.grid()
		# pylab.legend( loc="upper center" )
		# pylab.subplot( 212 )
		# pylab.hist( y2, bins=100, range=( 0, 1 ), label=h2 )
		pylab.grid()
		pylab.legend( loc="upper center" )
		pdf.savefig()
		pylab.close()
		# pylab.show()
		# fname = "%s-%s.png" % ( h1, h2 )
		# pylab.savefig( fname=fname )
		d = pdf.infodict()
		d['Title'] = 'Frameshift Signals'
		d['Author'] = u'Paul K. Korir'
		d['Subject'] = 'Histograms showing relative positions of putative frameshift signals'
		d['Keywords'] = 'Frameshift, hexamer, signal'
		d['CreationDate'] = datetime.datetime(2014, 07, 21)
		d['ModDate'] = datetime.datetime.today()
	
	pdf.close()

if __name__ == "__main__":
	fn = sys.argv[1]
	main( fn ) # the output that has the hexamers from each putative transcript