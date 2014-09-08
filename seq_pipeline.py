#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import sys
import argparse
import logging
from precheck import *
from download_convert_qa import *
from mapping_quantification import *
from SRAObjects import *

def main( dcq_conf, mq_conf, skip_download=False, skip_convert=False, \
	skip_trim=False, skip_qa=False, skip_map=False, skip_quantify=False ):
	
	# read in the configuration files
	dcq_configs = dict()
	with open( dcq_conf ) as f:
		for row in f:
			if row[0] == "#" or row[0] == "\n" or row[0] == " ": # comments or blanks
				continue
			else:
				key,value = row.strip( "\n" ).split( "=" )
				dcq_configs[key] = value
	
	mq_configs = dict()
	with open( mq_conf ) as f:
		for row in f:
			if row[0] == "#" or row[0] == "\n" or row[0] == " ": # comments or blanks
				continue
			else:
				key,value = row.strip( "\n" ).split( "=" )
				mq_configs[key] = value
	
	# show the configs
	logging.debug( "DCQ CONFIGS:" )
	logging.debug( dcq_configs )

	# look for errors
	dcq_errors = precheck( dcq_configs )
	if dcq_errors > 0:
		logging.critical( "Found %s errors" % dcq_errors )
		sys.exit( 1 )
	else:
		logging.debug( "No errors found." )
	
	logging.debug( "MQ CONFIGS:" )
	logging.debug( mq_configs )
	mq_errors = precheck( mq_configs )
	if mq_errors > 0:
		logging.critical( "Found %s errors" % mq_errors )
		sys.exit( 1 )
	else:
		logging.debug( "No errors found." )

	# read the SraRunTable.txt
	T = SraRunTable( dcq_configs['SRARUNTABLE'], \
	ignore=dcq_configs['IGNORE_RUNS'] )
	T.read()
	
	# download, convert, QA
	if skip_download:
		logging.info( "Skipping download..." )
	else:
		download( T, dcq_configs )
	
	if skip_convert:
		logging.info( "Skipping convert..." )
	else:
		convert( T, dcq_configs )
	
	if skip_trim:
		logging.info( "Skipping trimming..." )
	else:
		trimming( T, dcq_configs )
	
	if skip_qa:
		logging.info( "Skipping QA..." )
	else:
		qa( T, dcq_configs )
	
	# mapping, quantification
	if skip_map:
		logging.info( "Skipping mapping..." )
	else:
		mapping( T, dcq_configs )
	
	sys.exit( 0 )
	
	if skip_quantify:
		logging.info( "Skipping quantification..." )
	else:
		quantification( T, mq_configs )	

if __name__ == "__main__":
	"""
	This script assumes that there is a file called SraRunTable.txt in this folder
	"""
	logging.basicConfig( filename="run.log", format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG )
	
	# begin this log
	logging.info( "################################################################################" )
	logging.info( "                            COMMENCING BREEZE RUN" )
	logging.info( "################################################################################" )
	
	parser = argparse.ArgumentParser( description=\
		"Script that makes high-throughtput data analysis a breeze." )
	parser.add_argument( "-D", "--dcq-conf", \
		help="configuration file for download-convert-QA" )
	parser.add_argument( "-M", "--mq-conf", \
		help="configuration file for mapping-quantification" )
	parser.add_argument( "-d", "--skip-download", action="store_true", \
		help="do not download files" )
	parser.add_argument( "-c", "--skip-convert", action="store_true", \
		help="do not convert files" )
	parser.add_argument( "-t", "--skip-trim", action="store_true", \
		help="do not trim files" )
	parser.add_argument( "-q", "--skip-qa", action="store_true", \
		help="do not QA files" )
	parser.add_argument( "-m", "--skip-map", action="store_true", \
		help="do not map files" )
	parser.add_argument( "-a", "--skip-quantify", action="store_true", \
		help="do not quantify files" )
	
	args = parser.parse_args()
	
	dcq_conf = args.dcq_conf
	mq_conf = args.mq_conf
	skip_download = args.skip_download
	skip_convert = args.skip_convert
	skip_trim = args.skip_trim
	skip_qa = args.skip_qa
	skip_map = args.skip_map
	skip_quantify = args.skip_quantify
	
	main( dcq_conf, mq_conf, skip_download, skip_convert, skip_trim, skip_qa, \
		skip_map, skip_quantify )
	
	# end this log
	logging.info( """############################################################\
	####################""" )
	logging.info( "                               ENDING BREEZE RUN" )
	logging.info( """############################################################\
	####################""" )
