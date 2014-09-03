# -*- encoding: utf-8 -*-
import sys
import os
import os.path
import glob
import logging
from utils import *

def mapping( T, dcq_configs ):
	logging.debug( "Mapping data..." )
	
	try:
		os.mkdir( dcq_configs['READ_ALIGNER_PATH'] )
	except OSError:
		logging.warn( "%s directory already exists. Proceeding..." % \
			dcq_configs['READ_ALIGNER_PATH'] )
		
	if dcq_configs['WRITE_UNALIGNED'] == "yes":
		try:
			os.mkdir( dcq_configs['READ_ALIGNER_UNALIGNED_PATH'] )
		except OSError:
			logging.warn( "%s directory already exists. Proceeding..." % \
			dcq_configs['READ_ALIGNER_UNALIGNED_PATH'] )
		
	# bowtie mapping (mapping without splice junctions)
	for run,R in T.runs.iteritems():
		# bowtie [options]* <ebwt> {-1 <m1> -2 <m2> | --12 <r> | <s>} [<hit>]
		trimmed_files = glob.glob( dcq_configs['TRIMMED_DATA_PATH'] + "/" + R.run + "*.fq.gz" )
		
		# sample-mapping options
		smopts = dcq_configs[R.run].split( "," )
		
		for s in smopts:
			if dcq_configs['PAIRED'] == "yes":
				trimmed_files.sort()
				cmd = "%s %s %s --threads %s -1 %s -2 %s %s %s" % ( \
					dcq_configs['READ_ALIGNER'], \
						dcq_configs['READ_ALIGNER_PARAMS'], \
							" --un %s/%s_ebwt%s.unaligned" % ( dcq_configs['READ_ALIGNER_UNALIGNED_PATH'], R.run, s ), \
								dcq_configs['READ_ALIGNER_THREADS'], \
									dcq_configs['EBWT_PATH' + s], \
										trimmed_files[0], \
											trimmed_files[1],\
												dcq_configs['READ_ALIGNER_PATH'] + "/" + R.run + "ebwt%s.sam" % s )
			else:
				cmd = "gunzip %s | %s %s %s --threads %s %s - %s" % ( \
					trimmed_files[0],\
					dcq_configs['READ_ALIGNER'], \
						dcq_configs['READ_ALIGNER_PARAMS'], \
							" --un %s/%s_ebwt%s.unaligned" % ( dcq_configs['READ_ALIGNER_UNALIGNED_PATH'], R.run, s ), \
								dcq_configs['READ_ALIGNER_THREADS'], \
									dcq_configs['EBWT_PATH' + s], \
											dcq_configs['READ_ALIGNER_PATH'] + "/" + R.run + "_ebwt%s.sam" % s )

			logging.debug( cmd )
			
			run_command( cmd )			
	
	# tophat [options] <bowtie_index> <reads1[,reads2,...]> [reads1[,reads2,...]] \
  #                                  [quals1,[quals2,...]] [quals1[,quals2,...]]


def quantification( mq_configs ):
	print >> sys.stderr, "Quantifying data..."
