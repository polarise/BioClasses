#!/usr/bin/env python
from __future__ import division
import sys
from Node import *
from Branch import *
from Paths import *

#frame_sequence = [ 1, 0, 2, 2, 1, 0, 1 ]
frame_sequence = [ 1, 0, 2, 1, 1, 1, 1, 2, 1, 0, 0, 1, 0, 1, 1, 2, 0, 2, 2 ]
indexes = range( len( frame_sequence ))

new_frame_sequence = zip( frame_sequence, indexes )

print frame_sequence
print new_frame_sequence

# remove duplicates
unique_frame_sequence = [ new_frame_sequence[0] ]
for i in xrange( 1, len( new_frame_sequence ) ):
	if new_frame_sequence[i][0] == unique_frame_sequence[-1][0]:
		continue
	else:
		unique_frame_sequence.append( new_frame_sequence[i] )

print unique_frame_sequence
		
# append [ 0, 1, 2 ]
unique_frame_sequence += zip( range( 3 ), [ -1 ]*3 )
print unique_frame_sequence
print

# generate branches
branches = list()
positions = list()
while len( unique_frame_sequence ) > 3:
	branch = list()
	position = list()
	i = 0
	while len( branch ) < 3:
		if unique_frame_sequence[i][0] not in branch:
			branch.append( unique_frame_sequence[i][0] )
			position.append( unique_frame_sequence[i][1] )
		i += 1
	branches.append( zip( branch, position ))
	unique_frame_sequence.pop( 0 )

print branches
print

Branches = list()
for b in branches:
	Branches.append( Branch( Node( *b[0] ), Node( *b[1] ), Node( *b[2] )))

p = Paths()
for B in Branches:
	print B
	p.extend( B )
	
for i in p.branches:
	print i
	print p.branches[i]

all_paths = p.get_all_path_sequences()
all_paths.sort()
print all_paths, len( all_paths )
print
for p in all_paths:
	print p, len( p ), sum( p )
