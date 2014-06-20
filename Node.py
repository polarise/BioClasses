from __future__ import division
import sys

class Node( object ):
	def __init__( self, name, value, is_root=False ):
		self.name = name
		self.value = value
		self.is_root = is_root
		self.is_leaf = not self.is_root
		self.is_left = None
		self.is_right = None
		self.parent_branch = None
	
	def __eq__( self, node ):
		if self.name == node.name and self.value == node.value:
			return True
		else:
			return False
	
	def __repr__( self ):
		return "Node: (%s, %s)" % ( self.name, self.value )