# -*- encoding: utf-8 -*-
from Sequence import *

class RandomSequence( Sequence ):
	def __init__( self, length, bases='ACGT', starts=[ 'ATG' ], stops=[ 'TAA', 'TAG' ] ):
		super( RandomSequence, self ).__init__( length=length )
	
	def info( self, comment="" ):
		return "Random sequence of length %d: %s" % ( self.length, comment )

	def generate( self ):
		"""
		Method to generate a random sequence of lenght length
		"""
		self.sequence = ""
		while len( self.sequence ) < self.length:
			self.sequence += random.choice( self.bases )