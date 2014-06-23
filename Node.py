from __future__ import division
import sys

class Node( object ):
	def __init__( self, name, value ):
		self.name = name
		self.value = value
		self.index = None
		self.parent = None
	
	def __eq__( self, node ):
		if self.name == node.name and self.value == node.value:
			return True
		else:
			return False
		
	def identify( self ):
		return self.name, self.value
	
	
	def __repr__( self ):
		return "Node:(%s,%s)" % ( self.name, self.value )
