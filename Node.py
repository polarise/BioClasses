from __future__ import division
import sys

class Node( object ):
	def __init__( self, name, value ):
		self.name = name
		self.value = value
		self.descendants = list()
		self.parent = None
	
	def __eq__( self, node ):
		if self.name == node.name and self.value == node.value:
			return True
		else:
			return False
		
	def identify( self ):
		return self.name, self.value
	
	def add_descendant( self, node ):
		if isinstance( node, Node ):
			node.parent = self
			self.descendants.append( node )
		elif isinstance( node, list ):
			for n in node:
				n.parent = self
			self.descendants += node
	
	def replace_descendant( self, old_node, new_node ):
		self.descendants.remove( old_node )
		self.add_descendant( new_node )
		
	def reset( self ):
		self.descendants = list()
		self.parent = None
	
	def __repr__( self ):
		if len( self.descendants ) == 0:
			return "Terminal node: (%s,%s)" % ( self.name, self.value )
		else:
			return "Root node: (%s,%s)" % ( self.name, self.value )