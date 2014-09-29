# -*- encoding: utf-8 -*-
import sys

class Exon( object ):
	def __init__( self, record ):
		if record.source == "exon":
			self.exon_id = record.group_dict['exon_id']
		elif record.source == "CDS":
			self.exon_id = record.group_dict['protein_id']
		elif record.source == "start_codon" or record.source == "stop_codon":
			self.exon_id = record.group_dict['ccds_id']
		self.source = record.source
		self.exon_number = record.group_dict['exon_number']
		self.start = record.start
		self.end = record.end
		
