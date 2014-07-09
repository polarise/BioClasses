# -*- encoding: utf-8 -*-
from __future__ import division
import sys

class AminoAcid( object ):
	def __init__( self, name, lsymbol, ssymbol, codons ):
		self.name = name # full name e.g. 'Phelinalanine'
		self.lsymbol = lsymbol # long symbol e.g. 'Phe'
		self.ssymbol = ssymbol # short symbol e.g. 'F'
		self.codons = codons.split( "," ) # list
		self.codon_counts = dict()
		self.norm_counts = dict()
	
	def __repr__( self ):
		return "Amino acid: %s (%s/%s)\nCodons    : %s" % ( self.name, \
			self.lsymbol, self.ssymbol, ",".join( self.codons ))
		
	def count_codon( self, codon ):
		if codon not in self.codon_counts:
			self.codon_counts[codon] = 1
		else:
			self.codon_counts[codon] += 1
	
	def normalise( self ):
		total_count = sum( self.codon_counts.values() )
		for c in self.codon_counts:
			self.norm_counts[c] = self.codon_counts[c]/total_counts