#!/usr/bin/env python
from __future__ import division
import sys
import math

class ShiftMatrix( object ):
	def __init__( self, length, min_shift=-4, max_shift=4 ):
		self.length = length
		self.min_shift = min_shift
		self.max_shift = max_shift
		indexes = range( length )
		self.matrix = list()
		for i in xrange( self.min_shift, self.max_shift+1 ):
			row = map( lambda x: x - i, indexes )
			self.matrix.append( row )
	
	def __repr__( self ):
		rjust_int = int( math.floor( math.log( self.length, 10 ) + 1 ))
		output_str = "ShiftMatrix for sequence of length %d:\n" % self.length
		i = self.max_shift
		for row in self.matrix:
			if i > 0:
				output_str += " +%d: %s\n" % ( i, " ".join( map( lambda x: x.rjust( rjust_int ), map( str, row ))))
			elif i == 0:
				output_str += "  %d: %s\n" % ( i, " ".join( map( lambda x: x.rjust( rjust_int ), map( str, row ))))
			else:
				output_str += " %d: %s\n" % ( i, " ".join( map( lambda x: x.rjust( rjust_int ), map( str, row ))))
			i -= 1
		return output_str.strip( '\n' )

def main():
	m = ShiftMatrix( 70 )
	print m
	


if __name__ == "__main__":
	main()
