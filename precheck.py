# -*- encoding: utf-8 -*-
import sys
import logging

def precheck( configs ):
	"""
	checks configs for problems
	return value specifies number of errors found
	"""
	config_status = dict()
	logging.info( "Running pre-checks..." )
	
	overall_status = 0
	for key,value in config_status.iteritems():
		if value != 0:
			overall_status += value
	
	return overall_status