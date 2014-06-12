#!/usr/bin/env python
import Sequence

def main():
	s = Sequence.RandomSequence( 100 )
	s.generate_random_sequence()
	print s.info()
	print s.as_codons
	s.as_codons = True
	print s
	print s.as_codons
	for i in xrange( 3 ):
		print "%d: %s" % ( i, s.colour_frame( i ))
#	
#	print
#	
#	# initialise
#	s = Sequence.Sequence( no_of_shifts=2, min_length=50, max_length=100 )
#	s.generate_frameshift_sequence()
#	
#	print s.info()
#	for i in xrange( 3 ):
#		print "%d: %s" % ( i, s.colour_frame( i, sep="" ))
		
#	# generate 10 frameshifted sequences
#	for i in xrange( 10 ):
#		s = Sequence.Sequence( no_of_shifts=2, min_length=50, max_length=100 )
#		s.generate_frameshift_sequence()
#		print "\t".join([ str( s ), str( s.no_of_shifts ), ",".join( map( str, s.frameshifts )), ",".join( map( str, s.frame_lengths ))] )

if __name__ == "__main__":
	main()
