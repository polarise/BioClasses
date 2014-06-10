#!/usr/bin/env python
import Sequence

def main():
	s = Sequence()
	s.generate_random_sequence( 10 )
	for i in xrange( 3 ):
		print s.colour_frame( i )

if __name__ == "__main__":
	main()
