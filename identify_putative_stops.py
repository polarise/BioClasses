#!/usr/bin/env python
from __future__ import division
import sys
import argparse

#===============================================================================

class Seqname( object ):
	def __init__( self, seqname, length ):
		self.seqname = seqname
		self.length = int( length )
		self.frameshift = dict() # position->Frameshift object
	
	def add_frameshift( self, F ):
		self.frameshift[ F.pos ] = F
	
	def get_putative_stop( self, pos_score_threshold=0.5 ):
		keys = self.frameshift.keys()
		keys.sort()
		if len( keys ) > 1: # if we have another frameshift after the main one
			if self.frameshift[keys[1]].pos_score < pos_score_threshold and self.frameshift[keys[1]].pos > self.length/2:
				# if this one falls in the stop zone
				print "\t".join(map( str, [ self, self.frameshift[keys[1]]]))
			
	def __repr__( self ):
		return "\t".join( map( str, [ self.seqname, self.length ]))

#===============================================================================

class Frameshift( object ):
	def __init__( self, loglik, signal, f0, f1, design, pos, pos_score, theta0, theta1, theta2 ):
		self.loglik = float( loglik )
		self.signal = signal
		self.f0 = int( f0 )									# initial frame
		self.f1 = int( f1 )									# final frame
		self.design = design								# frameshift designation
		self.pos = int( pos )								# position of the frameshift
		self.pos_score = float( pos_score )
		self.theta0 = float( theta0 )
		self.theta1 = float( theta1 )
		self.theta2 = float( theta2 )
	
	def __repr__( self ):
		return "\t".join( map( str, [ self.loglik, self.signal, self.f0, self.f1, self.design, self.pos, self.pos_score, self.theta0, self.theta1, self.theta2 ]))

#===============================================================================
	
def main( fs_fn, fn, pos_score ):
	# read in putative frameshifts
	sequences = dict()
	with open( fs_fn ) as f:
		for row in f:
			l = row.strip( "\n" ).split( "\t" )
			F = Frameshift( *l[2:] )
			if l[0] not in sequences:
				S = Seqname( l[0], l[1] )
				S.add_frameshift( F )
				sequences[l[0]] = S
			else:
				sequences[l[0]].add_frameshift( F )
	
	# stop:
	# the immediate next FS in the conservative stop zone after a putative stop
	with open( fn ) as f:
		for row in f:
			l = row.strip( "\n" ).split( "\t" )
			F = Frameshift( *l[2:] )
			if l[0] not in sequences:
				pass
#				S = Seqname( l[0], l[1] )
#				S.add_frameshift( F )
#				sequences[l[0]] = S
			else:
				sequences[l[0]].add_frameshift( F )
	
	for seqname,S in sequences.iteritems():
		S.get_putative_stop( pos_score )	

if __name__ == "__main__":
	parser = argparse.ArgumentParser( description="Identify high-confidence stop positions" )
	
	parser.add_argument( "-f", "--frameshifts", help="file containing putative frameshifts" )
	parser.add_argument( "-p", "--pos-score", default=0.5, type=float, help="threshold for position score [default: 0.5]" )
	parser.add_argument( "file", help="analytical results for most sequences" )
	
	args = parser.parse_args()
	
	fs_fn = args.frameshifts
	pos_score = args.pos_score
	fn = args.file
	
	# validate pos_score
	try:
		assert 0 <= pos_score <= 1
	except:
		raise ValueError( "Invalid value for pos_score: %f" % pos_score )

	main( fs_fn, fn, pos_score )
