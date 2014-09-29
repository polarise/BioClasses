# -*- encoding: utf-8 -*-
import sys
from Exon import *

class Transcript( object ):
	def __init__( self, record ):
		self.transcript_id = record.group_dict['transcript_id']
		self.source = record.source # protein_coding|...|miRNA| etc
		self.start = record.start
		self.end = record.end
		self.exons = dict()
		self.CDS = dict()
		self.UTR = dict()
		self.start_codon = None
		self.stop_codon = None
	
	def is_complete( self ):
		if self.start_codon is not None and self.stop_codon is not None:
			return True
		else:
			return False
	
	def process_exon( self, record ):
		self.exons[record.group_dict['exon_id']]  = Exon( record )
	
	def process_CDS( self, record ):
		self.CDS[record.group_dict['protein_id']] = Exon( record )
		
	def process_UTR( self, record ):
		pass
		
	def process_start_codon( self, record ):
		self.start_codon = record.start
		
	def process_stop_codon( self, record ):
		self.stop_codon = record.start
	
	def __repr__( self ):
		return "%s [%s(%s):(%s)%s]" % ( self.transcript_id, self.start, self.start_codon, self.stop_codon, self.end )
	
	def __eq__( self, T ):
		"""
		we define equality based on having the same CDS
		"""
		if self.start_codon == T.start_codon and self.stop_codon == T.stop_codon:
			return True
		else:
			return False
		
