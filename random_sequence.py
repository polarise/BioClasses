#!/usr/bin/env python
from __future__ import division
import sys
from Sequence import *
import random

def main():
	for i in xrange( 1, 3001 ):
		s = RandomSequence( random.randint( 100, 2000 ))
		s.generate()
		print ">RandomSeq%d" % i
		print s

if __name__ == "__main__":
	main()
	