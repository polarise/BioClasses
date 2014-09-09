# -*- encoding: utf-8 -*-
import sys
import os
import os.path
import glob
import logging
from utils import *

def download( T, configs ):
	"""
	T - an SraRunTable object (holds info on all runs)
	configs - configs for download-convert-QA
	"""
	logging.debug( "Downloading data..." )
	
	# prefetch
	for run,R in T.runs.iteritems():
		# check if the file is already present
		if os.path.isfile( configs['SRATOOLKIT_PATH'] + "/" + R.run + ".sra" ):
			logging.warn( "%s.sra already exists at %s. Skipping..." % \
				( R.run, configs['SRATOOLKIT_PATH'] ))
			continue
		else:	
			cmd = "%s %s -a \"%s|%s\" %s" % ( configs['DOWNLOADER'], \
				configs['DOWNLOADER_PARAMS'], configs['ASPERA_PATH'], \
					configs['ASPERA_KEY_PATH'], R.run )
			logging.debug( cmd )
		run_command( cmd )

def convert( T, configs ):
	logging.info( "Converting data..." )
	
	try:
		os.mkdir( configs['DATA_PATH'] )
	except OSError:
		logging.warn( "%s directory already exists. Proceeding..." % \
			configs['DATA_PATH'] )
		
	for run,R in T.runs.iteritems():
		sra_file = configs['SRATOOLKIT_PATH'] + "/" + R.run + ".sra"
		
		present_files = glob.glob( configs['DATA_PATH'] + "/" + R.run + "*" )
		
		if len( present_files ) > 0:
			logging.warn( "Found converted files: %s." % ", ".join( \
				present_files ))
			continue
		else:
			if configs['PAIRED'] == "yes":
				cmd = "%s %s --split-files --outdir %s %s" % ( configs['FASTQ_DUMPER'], \
					configs['FASTQ_DUMPER_PARAMS'], configs['DATA_PATH'], sra_file )
			else:
				cmd = "%s %s --outdir %s %s" % ( configs['FASTQ_DUMPER'], \
					configs['FASTQ_DUMPER_PARAMS'], configs['DATA_PATH'], sra_file )
			
			logging.debug( cmd )
			
			run_command( cmd )

def trimming( T, configs ):
	logging.info( "Trimming data..." )
	
	try:
		os.mkdir( configs['TRIMMED_DATA_PATH'] )
	except OSError:
		logging.warn( "%s directory already exists. Proceeding..." % \
			configs['TRIMMED_DATA_PATH'] )
		
	for run,R in T.runs.iteritems():
		present_files = glob.glob( configs['TRIMMED_DATA_PATH'] + "/" + \
			R.run + "*" )
				
		if len( present_files ) > 0:
			logging.warn( "Found trimmed files: %s" % ", ".join( present_files ))
			continue
		else:
			fastq_files = glob.glob( configs['DATA_PATH'] + "/" + R.run + \
				"*.fastq" )
			fastq_files.sort()
			
			cmd = "%s %s --output_dir %s %s" % ( configs['TRIMMER'], \
				configs['TRIMMER_PARAMS'], configs['TRIMMED_DATA_PATH'], \
					" ".join( fastq_files ))
			
			logging.debug( cmd )
			
			run_command( cmd )

def qa( T, configs ):
	logging.info( "Performing quality analysis on data..." )
	
	try:
		os.mkdir( configs['FASTQC_REPORT_PATH'] )
	except OSError:
		logging.warn( "%s directory already exisits. Proceeding..." % \
			configs['FASTQC_REPORT_PATH'] )
	
	for run,R in T.runs.iteritems():
		present_files = glob.glob( configs['FASTQC_REPORT_PATH'] + "/" + \
			R.run + "*" )
		
		if len( present_files ) > 0:
			logging.warn( "Found FastQC report files: %s" % \
				", ".join( present_files ))
			continue
		else:
			trimmed_files = glob.glob( configs['TRIMMED_DATA_PATH'] + "/" + \
				R.run + "*fq" )
			trimmed_files.sort()
			
			cmd = "%s %s --outdir %s %s" % ( configs['FASTQC'], \
			configs['FASTQC_PARAMS'], configs['FASTQC_REPORT_PATH'], \
			" ".join( trimmed_files ))
			
			logging.debug( cmd )
			
			run_command( cmd )
	
	# delete zip files
	if configs['DELETE_FASTQC_ZIP'] == "yes":
		logging.info( "Deleting FastQC zip files..." )
	
		cmd = "rm -vf %s/*.zip" % configs['FASTQC_REPORT_PATH']
	
		logging.debug( cmd )
	
		run_command( cmd )
	
	# transfer FastQC reports
	if configs['TRANSFTER_FASTQC_REPORTS'] == "yes":		
		logging.info( "Creating remote FastQC report directory %s..." % \
		T.sra_study )
		
		cmd = "%s %s \"mkdir -p %s/%s\"" % ( configs['REMOTE_CONN'],\
		configs['FASTQC_FILE_TRANSFER_HOST'], \
		configs['FASTQC_FILE_TRANSFER_PATH'], T.sra_study )

		logging.debug( cmd )
		
		run_command( cmd )

		logging.info( "Transferring FastQC reports to %s:%s..." % ( \
		configs['FASTQC_FILE_TRANSFER_HOST'], \
		configs['FASTQC_FILE_TRANSFER_PATH'] ))
		
		cmd = "%s %s %s %s:%s/%s" % ( configs['FILE_TRANSFER'],\
		configs['FILE_TRANSFER_PARAMS'], configs['FASTQC_REPORT_PATH'],\
		configs['FASTQC_FILE_TRANSFER_HOST'],\
		configs['FASTQC_FILE_TRANSFER_PATH'],	T.sra_study )
		
		logging.debug( cmd )
		
		run_command( cmd )
		
			
