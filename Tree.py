from __future__ import division
import sys
from Node import *

class Tree( object ):
	def __init__( self ):
		self.root = None
		self.leaves = list()
		
	def graft_branch( self, branch ):
		if self.root is None:
			self.root = branch.root
			self.leaves = branch.descendands
		else:
			leaves = list()
			for leaf in self.leaves:
				if leaf = branch.root:
					for d in branch.descendants:
						d.parent = leaf
						leaves.append( d )
				else:
					leaves.append( leaf )
			
			self.leaves = leaves
		
	def graft( self, node ):
 		print >> sys.stderr, "Attempting to add %s with %s..." % ( str( node ), ", ".join( map( str, node.descendants )))
		if self.root is None:
			self.root = node
			self.leaves = node.descendants
			# self.root = Node( *node.identify())
			# self.root.add_descendant( node.descendants )
			# self.leaves = self.root.descendants
		else:
			leaves = list()
			for leaf in self.leaves:
				leaf.descendants = list()
				if leaf == node:
					leaf.add_descendant( node.descendants )
					leaves += leaf.descendants
					# new_node = Node( *node.identify())
					# new_node.add_descendant( node.descendants )
					# leaves += new_node.descendants
					# leaf.parent.replace_descendant( leaf, new_node )
				else:
					leaves.append( leaf )
			
			self.leaves = leaves
			print len( self.leaves )
			
			# this is where the problem is
			# self.nodes[ node.identify() ] = node
			# additional_leaves = list()
			# leaves_to_remove = list()
			# for leaf in self.leaves:
			# 	if leaf == node:
			# 		leaf.parent.replace_descendant( leaf, node )
			# 		additional_leaves += node.descendants
			# 		leaves_to_remove.append( leaf )
			#
			# for leaf in leaves_to_remove:
			# 	self.leaves.pop( self.leaves.index( leaf ))
			#
			# self.leaves += additional_leaves
	
	def __repr__( self ):
		# tree_str = "Tree with the %d composite nodes and %d leaves.\n" % ( len( self.nodes ), len( self.leaves ))
		tree_str = "Tree with %d leaves.\n" % len( self.leaves )
		tree_str += "Root:\n\t%s\n" % str( self.root )
		# tree_str += "Nodes:\n\t%s\n" % ", ".join( map( str, self.nodes.values()))
		tree_str += "Leaves:\n\t%s\n" % ", ".join( map( str, self.leaves ))
		return tree_str
		
	def path_to_leaf( self, leaf, reverse=True ):
		path = list()
		node = leaf
		while node != self.root:
			path.append( node.name )
			node = node.parent
		path.append( node.name )
		if reverse:
			return path[::-1]
		else:
			return path