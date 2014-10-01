# -*- encoding: utf-8 -*-
from __future__ import division
import sys
import pysam
from scipy import stats
from GTFRecord import *

class TabixResult( object ):
	def __init__( self, region, tabixfile, filetype="bed", store_tabix_result=False ):
		"""
		filetype can be 'bed', 'gtf' or 'gff',
		"""
		self.region = region
		self.tabixfile = tabixfile
		try:
			tabix_result = tabixfile.fetch( region )
		except ValueError:
			print >> sys.stderr, "Warning: unable to create iterator for %s" % region
			tabix_result = list()
		if store_tabix_result:
			self.tabix_result = tabix_result			
		self.chrom, self.start, self.end = self.process_region_str( region )
		if filetype == "bed":
			self.count, self.density, self.serial_data = self.compute_stats( tabix_result )
		elif filetype == "gtf" or filetype == "gff":
			self.records = self.extract_records( tabix_result )
			self.record_count = len( self.records )
		else:
			raise NotImplementedError( "handler for other filetypes not implemented" )
	
	def extract_records( self, tabix_result ):
		records = list()
		for row in tabix_result:
			l = row.strip( "\n" ).split( "\t" )
			records.append( GTFRecord( *l ))
		
		return records
				
	def process_region_str( self, region ):
		chrom, start_end = region.split( ":" )
		start, end = map( int, start_end.split( "-" ))
		
		return chrom, start, end
	
	def compute_stats( self, tabix_result ):
		count_data = dict()
		count_rows = 0
		for row in tabix_result:
			l = row.strip( "\n" ).split( "\t" )
			pos = int( l[1] )
			pos_count = int( l[-2] )
			count_data[int( l[1] )] = pos_count
			count_rows += 1
			
		count = sum( count_data.values())
		
		# fill in the blanks for count_data
		serial_data = list()
		for pos in xrange( self.start, self.end + 1, 1 ):
			try:
				serial_data.append( count_data[pos] )
			except KeyError:
				serial_data.append( 0 )
		
		try:
			density = round( count/(self.end - self.start + 1 ), 4 )
		except ZeroDivisionError:
			density = "Inf"
		return count, density, serial_data
	
	def compute_peaks( self, density, n=21, pvalue_thresh=0.01 ):
		"""
		n must be odd
		"""
		# put n/2 zeros at the beginning...
		self.peak_data = [0]*(n//2)
		self.peak_pvalues = [1]*(n//2)
		
		c = self.serial_data
		for i in xrange( len( self.serial_data ) - n + 1 ):
			x_sum = 0
			for j in xrange( i, i + n ):
				x_sum += c[j]
			x_bar = x_sum/n
			
			if x_bar > 5*density*n:
				self.peak_data.append( 1 )
				pvalue = stats.poisson.pmf( c[i+(n//2)], mu=density*n )
				self.peak_pvalues.append( pvalue )
			else:
				self.peak_data.append( 0 )
				self.peak_pvalues.append( 1 )
		
		# and at the end
		self.peak_data += [0]*(n//2)
		self.peak_pvalues += [1]*(n//2)
		
		# look for peaks		
		self.found_peaks = dict()
		peak = list()
		i = 0	
		peak_pos = -1
		for p in self.peak_pvalues:
			if p == 0:
				if peak_pos < 0:
					peak_pos = i
				peak.append( p )	
			elif p == 1:
				if len( peak ) >= n:
					self.found_peaks[self.start + peak_pos] = len( peak )
				peak = list()
				peak_pos = -1
			i += 1
		
