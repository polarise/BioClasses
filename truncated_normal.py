#!/usr/bin/env python
from __future__ import division
import sys
import scipy.stats
import matplotlib.pyplot as pylab

def main():
	L = 1000
	for sigma in xrange( 100, 900, 100 ):
		# sigma = 350
		a = 0
		b = L
		a_ = ( 0 - L/2 )/sigma
		b_ = ( L - L/2 )/sigma
	
		x = list()
		y2 = list()
		for s in xrange( 0, L, 1 ):
			s_ = ( s - L/2 )/sigma
			x.append( s )
			if 0 <= s <= L/2:
				y2.append( scipy.stats.truncnorm.cdf( s_, a_, b_ ))
			elif L/2 < s <= L:
				y2.append( 1 - scipy.stats.truncnorm.cdf( s_, a_, b_ ))
	
		pylab.plot( x, y2, label="$\sigma = %s$" % sigma )
	pylab.grid()
	pylab.legend( loc="upper left" )
	pylab.show()

if __name__ == "__main__":
	main()
	