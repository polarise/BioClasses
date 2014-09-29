# -*- encoding: utf-8 -*-
import sys
import itertools
from Transcript import *
from Exon import *

class Gene( object ):
	def __init__( self, record ):
		self.gene_id = record.group_dict['gene_id']
		self.seqname = record.seqname
		self.source = record.source
		self.start = record.start
		self.end = record.end
		self.strand = record.strand
		self.transcripts = dict()
	
	def process_record( self, record ):
		if record.feature == "transcript":
			self.transcripts[record.group_dict['transcript_id']] = Transcript( record )
		elif record.feature == "exon":
			self.transcripts[record.group_dict['transcript_id']].process_exon( record )
		elif record.feature == "CDS":
			self.transcripts[record.group_dict['transcript_id']].process_CDS( record )
		elif record.feature == "UTR":
			self.transcripts[record.group_dict['transcript_id']].process_UTR( record )	
		elif record.feature == "start_codon":
					self.transcripts[record.group_dict['transcript_id']].process_start_codon( record )	
		elif record.feature == "stop_codon":
					self.transcripts[record.group_dict['transcript_id']].process_stop_codon( record )
	
	def __repr__( self ):
		return self.gene_id + " [" + ":".join([ self.seqname, self.start, self.end, self.strand ]) + "]"
	
	def get_protein_coding( self ):
		PCT = list()
		for transcript_id,T in self.transcripts.iteritems():
			if T.source == "protein_coding":
				PCT.append( T )
		
		return PCT
	
	def get_equal_cds( self ):
		PCT = self.get_protein_coding() # protein coding transcripts
		
		# we get the distribution of complete transcripts by (start_codon, stop_codon)
		start_stop_distr = dict()
		for P in PCT:
			if P.is_complete():
				start_stop = P.start_codon,P.stop_codon
				if start_stop not in start_stop_distr:
					start_stop_distr[start_stop] = 1
				else:
					start_stop_distr[start_stop] += 1
			else:
				pass
#				print >> sys.stderr, "Incomplete transcript: %s" % P
		
		# pick the start_stop with the most transcripts
		equal_cds_transcripts = set()
		if len( start_stop_distr ) > 0:
			start_stop_best = start_stop_distr.keys()[0]
			start_stop_max = start_stop_distr[start_stop_distr.keys()[0]] # guess that first is max
		
			for start_stop,start_stop_count in start_stop_distr.iteritems():
				if start_stop_count > start_stop_max:
					start_stop_best = start_stop
				
			# now get the transcripts corresponding
			best_start, best_stop = start_stop
			for P in PCT:
				if P.start_codon == best_start and P.stop_codon == best_stop:
					equal_cds_transcripts.add( P )
			
		return list( equal_cds_transcripts )



