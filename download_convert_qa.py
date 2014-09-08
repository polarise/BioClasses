# -*- encoding: utf-8 -*-
import sys
import os
import os.path
import glob
import logging
from utils import *

def download( T, dcq_configs ):
	"""
	T - an SraRunTable object (holds info on all runs)
	dcq_configs - configs for download-convert-QA
	"""
	logging.debug( "Downloading data..." )
	
	# prefetch
	for run,R in T.runs.iteritems():
		# check if the file is already present
		if os.path.isfile( dcq_configs['SRATOOLKIT_PATH'] + "/" + R.run + ".sra" ):
			logging.warn( "%s.sra already exists at %s. Skipping..." % \
				( R.run, dcq_configs['SRATOOLKIT_PATH'] ))
			continue
		else:	
			cmd = "%s %s -a \"%s|%s\" %s" % ( dcq_configs['DOWNLOADER'], \
				dcq_configs['DOWNLOADER_PARAMS'], dcq_configs['ASPERA_PATH'], \
					dcq_configs['ASPERA_KEY_PATH'], R.run )
			logging.debug( cmd )
		run_command( cmd )

def convert( T, dcq_configs ):
	logging.info( "Converting data..." )
	
	try:
		os.mkdir( dcq_configs['DATA_PATH'] )
	except OSError:
		logging.warn( "%s directory already exists. Proceeding..." % \
			dcq_configs['DATA_PATH'] )
		
	for run,R in T.runs.iteritems():
		sra_file = dcq_configs['SRATOOLKIT_PATH'] + "/" + R.run + ".sra"
		
		present_files = glob.glob( dcq_configs['DATA_PATH'] + "/" + R.run + "*" )
		
		if len( present_files ) > 0:
			logging.warn( "Found converted files: %s." % ", ".join( \
				present_files ))
			continue
		else:
			if dcq_configs['PAIRED'] == "yes":
				cmd = "%s %s --split-files --outdir %s %s" % ( dcq_configs['FASTQ_DUMPER'], \
					dcq_configs['FASTQ_DUMPER_PARAMS'], dcq_configs['DATA_PATH'], sra_file )
			else:
				cmd = "%s %s --outdir %s %s" % ( dcq_configs['FASTQ_DUMPER'], \
					dcq_configs['FASTQ_DUMPER_PARAMS'], dcq_configs['DATA_PATH'], sra_file )
			
			logging.debug( cmd )
			
			run_command( cmd )

def trimming( T, dcq_configs ):
	logging.info( "Trimming data..." )
	
	try:
		os.mkdir( dcq_configs['TRIMMED_DATA_PATH'] )
	except OSError:
		logging.warn( "%s directory already exists. Proceeding..." % \
			dcq_configs['TRIMMED_DATA_PATH'] )
		
	for run,R in T.runs.iteritems():
		present_files = glob.glob( dcq_configs['TRIMMED_DATA_PATH'] + "/" + \
			R.run + "*" )
				
		if len( present_files ) > 0:
			logging.warn( "Found trimmed files: %s" % ", ".join( present_files ))
			continue
		else:
			fastq_files = glob.glob( dcq_configs['DATA_PATH'] + "/" + R.run + \
				"*.fastq.gz" )
			fastq_files.sort()
			
			cmd = "%s %s --output_dir %s %s" % ( dcq_configs['TRIMMER'], \
				dcq_configs['TRIMMER_PARAMS'], dcq_configs['TRIMMED_DATA_PATH'], \
					" ".join( fastq_files ))
			
			logging.debug( cmd )
			
			run_command( cmd )

def qa( T, dcq_configs ):
	logging.info( "Performing quality analysis on data..." )
	
	try:
		os.mkdir( dcq_configs['FASTQC_REPORT_PATH'] )
	except OSError:
		logging.warn( "%s directory already exisits. Proceeding..." % \
			dcq_configs['FASTQC_REPORT_PATH'] )
	
	for run,R in T.runs.iteritems():
		present_files = glob.glob( dcq_configs['FASTQC_REPORT_PATH'] + "/" + \
			R.run + "*" )
		
		if len( present_files ) > 0:
			logging.warn( "Found FastQC report files: %s" % \
				", ".join( present_files ))
			continue
		else:
			trimmed_files = glob.glob( dcq_configs['TRIMMED_DATA_PATH'] + "/" + \
				R.run + "*fq.gz" )
			trimmed_files.sort()
			
			cmd = "%s %s --outdir %s %s" % ( dcq_configs['FASTQC'], \
			dcq_configs['FASTQC_PARAMS'], dcq_configs['FASTQC_REPORT_PATH'], \
			" ".join( trimmed_files ))
			
			logging.debug( cmd )
			
			run_command( cmd )
	
	# delete zip files
	if dcq_configs['DELETE_FASTQC_ZIP'] == "yes":
		logging.info( "Deleting FastQC zip files..." )
	
		cmd = "rm -vf %s/*.zip" % dcq_configs['FASTQC_REPORT_PATH']
	
		logging.debug( cmd )
	
		run_command( cmd )
	
	# transfer FastQC reports
	if dcq_configs['TRANSFTER_FASTQC_REPORTS'] == "yes":		
		logging.info( "Creating remote FastQC report directory %s..." % \
		T.sra_study )
		
		cmd = "%s %s \"mkdir -p %s/%s\"" % ( dcq_configs['REMOTE_CONN'],\
		dcq_configs['FASTQC_FILE_TRANSFER_HOST'], \
		dcq_configs['FASTQC_FILE_TRANSFER_PATH'], T.sra_study )

		logging.debug( cmd )
		
		run_command( cmd )

		logging.info( "Transferring FastQC reports to %s:%s..." % ( \
		dcq_configs['FASTQC_FILE_TRANSFER_HOST'], \
		dcq_configs['FASTQC_FILE_TRANSFER_PATH'] ))
		
		cmd = "%s %s %s %s:%s/%s" % ( dcq_configs['FILE_TRANSFER'],\
		dcq_configs['FILE_TRANSFER_PARAMS'], dcq_configs['FASTQC_REPORT_PATH'],\
		dcq_configs['FASTQC_FILE_TRANSFER_HOST'],\
		dcq_configs['FASTQC_FILE_TRANSFER_PATH'],	T.sra_study )
		
		logging.debug( cmd )
		
		run_command( cmd )
		
			
