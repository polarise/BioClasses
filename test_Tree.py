#!/usr/bin/env python
from __future__ import division
import sys
from Node import *
from Branch import *
from Tree import *

def main():
	n1 = Node( 1, 0, True ) # the root node
	n2 = Node( 0, 1, False ) # left leaf
	n3 = Node( 2, 2, False )
	
	b1 = Branch( Node( 1, 0, True ), Node( 0, 1, False ), Node( 2, 2, False ))
	b2 = Branch( Node( 0, 1, True ), Node( 2, 2, False ), Node( 1, 4, False ))
	b3 = Branch( Node( 2, 2, True ), Node( 1, 4, False ), Node( 0, 5, False ))
	b4 = Branch( Node( 1, 4, True ), Node( 0, 5, False ), Node( 2, -1, False ))
	b5 = Branch( Node( 0, 5, True ), Node( 1, 6, False ), Node( 2, -1, False ))
	b6 = Branch( Node( 1, 6, True ), Node( 0, -1, False ), Node( 2, -1, False ))
	
	t = Tree()
	t.show()
	t.graft_branch( b1 )
	print
	t.show()
	print b2
	t.graft_branch( b2 )
	print
	t.show()
	t.graft_branch( b3 )
	t.graft_branch( b4 )
	t.graft_branch( b5 )
	t.graft_branch( b6 )
	print
	t.show()
	print
	print t.descend_left()
	
if __name__ == "__main__":
	main()