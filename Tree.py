from __future__ import division
import sys

class Tree( object ):
	def __init__( self ):
		self.root = None
		self.leaves = list()
		
	def graft_branch( self, branch ):
		if self.root is None:
			self.root = branch.root_node
			self.leaves += [ branch.left_leaf, branch.right_leaf ]
		else:
			for leaf in self.leaves:
				if leaf == branch.root_node:
					if leaf.is_left:
						leaf.parent_branch.left_node = branch.root_node
					elif leaf.is_right:
						leaf.parent_branch.right_node = branch.root_node
					while leaf in self.leaves:
						self.leaves.pop( self.leaves.index( leaf ))
						self.leaves += [ branch.left_leaf, branch.right_leaf ]
	
	def show( self ):
		print "Root: %s" % self.root
		print "Leaves:"
		for leaf in self.leaves:
			print leaf
	
	def descend_left( self ):
		value = list()
		node = self.root
		while node.left_leaf.value > 0:
			value.append( node.left_leaf.value )
			
		
		return value