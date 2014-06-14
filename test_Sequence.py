#!/usr/bin/env python
import Sequence

def main():
#	s = Sequence.RandomSequence( 100 )
#	s.generate()
#	print s.info()
##	s.as_codons = True
#	print s
#	for i in xrange( 3 ):
#		print "%d: %s" % ( i, s.colour_frame( i, sep="" ))
#	
#	print
	
#	# initialise
	s = Sequence.RandomFSSequence( no_of_shifts=3, min_length=100, max_length=200 )
#	s = Sequence.RandomFSSequence( no_of_shifts=2, min_length=50, max_length=100 )
	s.generate()
		
#	print s.info()
#	for i in xrange( 3 ):
#		print "%d: %s" % ( i, s.colour_frame( i, sep="" ))
#	
#	print "   " + "         |"*(( s.length )//10 )
#	print
	
	print s.info( "without UGA" )
	
	for i in xrange( 4, -5, -1 ):
		if i > 0:
			print "+%d: %s" % ( i, s.binary_frame( i, sep="" ))
		elif i == 0:
			print " %d: %s" % ( i, s.binary_frame( i, sep="" ))
		elif i < 0:
			print "%d: %s" % ( i, s.binary_frame( i, sep="" ))
		
#	s.stops.append( "UGA" )
#	print

#	print s.info( "with UGA" )
#	for i in xrange( 4, -5, -1 ):
#		if i > 0:
#			print "+%d: %s" % ( i, s.binary_frame( i, sep="" ))
#		elif i == 0:
#			print " %d: %s" % ( i, s.binary_frame( i, sep="" ))
#		elif i < 0:
#			print "%d: %s" % ( i, s.binary_frame( i, sep="" ))
	
#	print
#	print s.info()
#	for i in xrange( 3 ):
#		print s.codon_frame_vector( i )
#	print
	
#	s.set_binary_codon_matrix( weighted_start=False )	
#	print s.show_binary_codon_matrix()
#	print
#	s.set_binary_codon_matrix( weighted_start=True )
#	print s.show_binary_codon_matrix()
#	print
	
#	for i in xrange( 3 ):
#		print i, s.dist_to_stop( i )
#	print s.get_best_frame( 0 )
	print
	
	t = Sequence.BiologicalSequence( s.sequence )
	for i in xrange( 3 ):
		t.detect_frameshifts( i )
		print "frameshifts:   ", t.frameshifts
		print "frameshifts:   ", map( lambda x: x % 3, t.frameshifts )
		print "frame lengths: ", map( lambda x: i + 3 + ( x - 3 )*3 + 3 - i, t.frame_lengths )
		print "frame scores:  ", t.frame_scores
		print "overall score: ", t.overall_score
		print
			
	# generate 10 frameshifted sequences
#	for i in xrange( 10 ):
#		s = Sequence.RandomFSSequence( no_of_shifts=2, min_length=50, max_length=100 )
#		s.generate()
#		print "\t".join([ str( s ), str( s.no_of_shifts ), ",".join( map( str, s.frameshifts )), ",".join( map( str, s.frame_lengths ))] )

if __name__ == "__main__":
	main()
