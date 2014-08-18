#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import division
import sys
import random
import numpy
import scipy.stats
import matplotlib.pyplot as plt
from Utils import *

def SG_filter5( inData ):
	outData = list()
	for i in xrange( len( inData)):
		if i < 2 or i > len( inData ) - 3:
			outData.append( inData[i] )
		else:
			data = 1/35*( -3 * inData[i-2] + 12 * inData[i-1] + 17 * inData[i] \
				+ 12 * inData[i+1] - 3 * inData[i+2] )
			outData.append( data )
	return outData

def SG_filter5_prime( inData ):
	outData = list()
	for i in xrange( len( inData)):
		if i < 2 or i > len( inData ) - 3:
			outData.append( inData[i] )
		else:
			data = 1/10*( -2 * inData[i-2] - inData[i-1] + 0 * inData[i] \
				+ inData[i+1] + 2 * inData[i+2] )
			outData.append( data )
	return outData

def SG_filter7( inData ):
	outData = list()
	for i in xrange( len( inData)):
		if i < 3 or i > len( inData ) - 4:
			outData.append( inData[i] )
		else:
			data = 1/21*( -2 * inData[i-3] + 3 * inData[i-2] + 6 * inData[i-1] \
				+ 7 * inData[i] + 6 * inData[i+1] + 3 * inData[i+2] - 2 * inData[i+3] )
			outData.append( data )
	return outData

def SG_filter7_prime( inData ):
	outData = list()
	for i in xrange( len( inData)):
		if i < 3 or i > len( inData ) - 4:
			outData.append( inData[i] )
		else:
			data = 1/28*( -3 * inData[i-3] - 2 * inData[i-2] - inData[i-1] \
				+ 0 * inData[i] + inData[i+1] + 2 * inData[i+2] + 3 * inData[i+3] )
			outData.append( data )
	return outData

def main():
	x = numpy.linspace( 0, 1, 1000 )
	x = numpy.linspace( -2*numpy.pi, 2*numpy.pi, 100 )
	"""
	y = [ 0 ]
	for i in xrange( len( x )-1 ):
		y.append( y[i] + scipy.stats.norm.rvs( loc=0, scale=10 ))
	"""
	y = numpy.sin( x )
	
	z = SG_filter5( y )
	z_prime = SG_filter5_prime( y )
	u = SG_filter7( y )
	u_prime = SG_filter7_prime( y )
	
	z = savgol( y, window_size=5 )
	z_prime = savgol( y, window_size=5, deriv=1 )
	
	fig, ( ax1, ax2 ) = plt.subplots( nrows=2, sharex=True )
	
	l1 = ax1.plot( x, y )
	l2 = ax1.plot( x, savgol( y, window_size=5 ), color="r", linewidth=2 )
	
	ax1.grid()
	
	l3 = ax2.plot( x, savgol( y, window_size=9, deriv=1 ), color="m", linewidth=1 )

	ax2.grid()
	
	fig.subplots_adjust( hspace=0.2 )
	
	plt.show()	
	
if __name__ == "__main__":
	main()