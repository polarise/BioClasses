# -*- encoding: utf-8 -*-
import sys
import os
import os.path
import glob
import logging
from utils import *

def mapping( T, configs ):
	logging.debug( "Mapping data..." )
	
	try:
		os.mkdir( configs['READ_ALIGNER_PATH'] )
	except OSError:
		logging.warn( "%s directory already exists. Proceeding..." % \
			configs['READ_ALIGNER_PATH'] )
		
	if configs['WRITE_UNALIGNED'] == "yes":
		try:
			os.mkdir( configs['READ_ALIGNER_UNALIGNED_PATH'] )
		except OSError:
			logging.warn( "%s directory already exists. Proceeding..." % \
			configs['READ_ALIGNER_UNALIGNED_PATH'] )
	
	try:
		os.mkdir( configs['SPLICED_ALIGNER_PATH'] )
	except OSError:
		logging.warn( "%s directory already exists. Proceeding..." % \
			configs['SPLICED_ALIGNER_PATH'] )	
		
	# bowtie mapping (mapping without splice junctions)
	for run,R in T.runs.iteritems():
		# bowtie [options]* <ebwt> {-1 <m1> -2 <m2> | --12 <r> | <s>} [<hit>]
		trimmed_files = glob.glob( configs['TRIMMED_DATA_PATH'] + "/" + R.run + "*.fq" )
		
		# sample-mapping options
		smopts = configs[R.run].split( "," )
		
		for s in smopts:
			present_files = glob.glob( configs['READ_ALIGNER_PATH'] + "/" + \
			R.run + "_%s_ebwt%s.sam" % ( configs['READ_ALIGNER'], s ))
			
			if len( present_files ) > 0:
				logging.warn( "Found read-aligner mapped files for index %s." % s )
				continue		
		
			if configs['PAIRED'] == "yes":
				trimmed_files.sort()
				# read aligner
				ra_cmd = "%s %s %s --threads %s -1 %s -2 %s %s %s" % ( \
				configs['READ_ALIGNER'], \
				configs['READ_ALIGNER_PARAMS'], \
				" --un %s/%s_ebwt%s.fastq" % ( configs['READ_ALIGNER_UNALIGNED_PATH'], R.run, s ), \
				configs['READ_ALIGNER_THREADS'], \
				configs['EBWT_PATH' + s], \
				trimmed_files[0], \
				trimmed_files[1],\
				configs['READ_ALIGNER_PATH'] + "/" + R.run + "_%s_ebwt%s.sam" % ( os.path.basename( configs['READ_ALIGNER'] ), s ))
				
			else:
				# read aligner
				ra_cmd = "%s %s %s --threads %s %s %s %s" % ( \
				configs['READ_ALIGNER'], \
				configs['READ_ALIGNER_PARAMS'], \
				" --un %s/%s_ebwt%s.fastq" % ( configs['READ_ALIGNER_UNALIGNED_PATH'], R.run, s ), \
				configs['READ_ALIGNER_THREADS'], \
				configs['EBWT_PATH' + s], \
				trimmed_files[0], \
				configs['READ_ALIGNER_PATH'] + "/" + R.run + "_%s_ebwt%s.sam" % ( os.path.basename( configs['READ_ALIGNER'] ), s ))

			logging.debug( ra_cmd )
			
			run_command( ra_cmd )
	
	# first remove any BAM files that may have remained
	logging.debug( "Removing stray BAM files..." )
	cmd = "rm -vf %s/*.bam" % configs['READ_ALIGNER_PATH']
	
	logging.debug( cmd )
	
	run_command( cmd )	
	
	# convert SAM to BAM files
	logging.debug( "Converting SAM to BAM files..." )
	# samtools view -bS -o ./aligned/*.bam ./aligned/*.sam
	samfiles = glob.glob( configs['READ_ALIGNER_PATH'] + "/*.sam" )
	for samfile in samfiles:
		bamfile = samfile[:-3] + "bam"
		cmd = "samtools view -bS -o %s %s" % ( bamfile, samfile )
	
		logging.debug( cmd )
	
		run_command( cmd )
	
	# sort BAM files
	logging.debug( "Sorting BAM files..." )
	# samtools sort ./aligned/*.bam ./aligned/*.sorted
	bamfiles = glob.glob( configs['READ_ALIGNER_PATH'] + "/*.bam" )
	for bamfile in bamfiles:
		sortedfile = bamfile[:-3] + "sorted"
		cmd = "samtools sort %s %s" % ( bamfile, sortedfile )
		
		logging.debug( cmd )
		
		run_command( cmd )
	
	# delete the SAM files to save space
	logging.debug( "Deleting SAM files..." )
	# rm -rvf ./aligned/*.sam
	cmd = "rm -vf %s/*.sam" % configs['READ_ALIGNER_PATH']
	
	logging.debug( cmd )
	
	run_command( cmd )
	
	# tophat mapping (mapping with splice junctions)
	for run,R in T.runs.iteritems():
		# tophat [options] <bowtie_index> <reads1[,reads2,...]> [reads1[,reads2,...]] \
  	#                                  [quals1,[quals2,...]] [quals1[,quals2,...]]
		trimmed_files = glob.glob( configs['TRIMMED_DATA_PATH'] + "/" + R.run + "*.fq" )
		
		# sample-mapping options
		smopts = configs[R.run].split( "," )			
		for s in smopts:
			# try to make the tophat directory if it doesn't exist
			try:
				os.mkdir( configs['SPLICED_ALIGNER_PATH'] + "/" + R.run + "_%s_ebwt%s" % ( os.path.basename( configs['SPLICED_ALIGNER']), s ))
			except OSError:
				logging.warn( "%s directory already exists. Proceeding..." % (\
				configs['SPLICED_ALIGNER_PATH'] + "/" + R.run + "_%s_ebwt%s" % ( os.path.basename( configs['SPLICED_ALIGNER']), s )))

			if len( present_files ) > 0:
				logging.warn( "Found read-aligner mapped files for index %s." % s )
				continue
					
			if configs['PAIRED'] == "yes":
				trimmed_files.sort()
				# spliced aligner
				sa_cmd = "%s %s --output-dir %s  --num-threads %s --GTF %s %s %s %s" % (
				configs['SPLICED_ALIGNER'], \
				configs['SPLICED_ALIGNER_PARAMS'], \
				configs['SPLICED_ALIGNER_PATH'] + "/" + R.run + "_%s_ebwt%s" % ( os.path.basename( configs['SPLICED_ALIGNER']), s ), \
				configs['SPLICED_ALIGNER_THREADS'], \
				configs['GTF_PATH' + s], \
				configs['EBWT_PATH' + s], \
				trimmed_files[0], \
				trimmed_files[1] )
			else:				
				# spliced aligner
				sa_cmd = "%s %s --output-dir %s  --num-threads %s --GTF %s %s %s" % (
				configs['SPLICED_ALIGNER'], \
				configs['SPLICED_ALIGNER_PARAMS'], \
				configs['SPLICED_ALIGNER_PATH'] + "/" + R.run + "_%s_ebwt%s" % ( os.path.basename( configs['SPLICED_ALIGNER']), s ), \
				configs['SPLICED_ALIGNER_THREADS'], \
				configs['GTF_PATH' + s], \
				configs['EBWT_PATH' + s], \
				trimmed_files[0] )
			
			logging.debug( sa_cmd )
			
			run_command( sa_cmd )

def quantification( mq_configs ):
	logging.debug( "Quantifying data..." )
	
	try:
		os.mkdir( configs['QUANTIFIER_PATH'] )
	except OSError:
		logging.warn( "%s directory already exists. Proceeding..." % \
			configs['QUANTIFIER_PATH'] )
	
	# read aligned
	read_aligned_files = glob.glob( configs['READ_ALIGNED_PATH'] + "/" + "*.sam" )
	
	# cufflinks --multi-read-correct --frag-bias-correct --GTF /path/to/gtf --seed 1234 --num-threads 8 --output-dir ./quantified ./aligned/hits.sam
	for samfile in read_aligned_files:
		# get the gtf number to use from the *ebwt<no>.sam name of the SAM file
		e = basename( samfile ).split( "." )[0].split( "ebwt" )[1]
		cmd = "%s %s --frag-bias-correct %s --GTF %s --num-threads %s --output-dir %s %s" % (\
		configs['QUANTIFIER'], \
		configs['QUANTIFIER_PARAMS'], \
		configs['FASTA_PATH'], \
		configs['GTF_PATH' + e], \
		configs['QUANTIFIER_THREADS'], \
		configs['QUANTIFIER_PATH'], \
		samfile )
	
	# splice aligned
	splice_aligned_files = glob.glob( configs['SPLICED_ALIGNER_PATH'] + "/" + "*.bam" )
	# cufflinks --multi-read-correct --frag-bias-correct ~/bioinf/Resources/H_sapiens/hg19.fa --seed 1234 --num-threads 15 --output-dir ./quantified -G /home/paul/bioinf/Resources/H_sapiens/hg19.chr.gtf ./splice_aligned/accepted_hits.bam
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
