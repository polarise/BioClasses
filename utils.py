# -*- encoding: utf-8 -*-
from __future__ import division
import sys
import os
import os.path
import glob
import logging
import subprocess

def run_command( cmd ):
	p = subprocess.Popen( cmd, shell=True, stdout=subprocess.PIPE, \
		stderr=subprocess.PIPE )
	stdoutdata,stderrdata = p.communicate()
	
	if stdoutdata is not None:
		logging.debug( stdoutdata )
	if stderrdata is not None:
		logging.debug( stderrdata )
