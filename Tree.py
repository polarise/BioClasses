from __future__ import division
import sys
from Node import *

class Tree( object ):
	def __init__( self ):
		self.root = None
		self.head = list()
		self.leaves = list()
		
	def graft2( self, branch ):
		"""
		Method to graft a branch to a growing tree
		"""
		if self.root is None:
			self.root = branch.root
			self.root.left_leaf = branch.descendants[0]
			self.root.right_leaf = branch.descendants[1]
			self.head.append( self.root )
		else:
			for h in self.head:
				# left_leaf
				if h.left_leaf == branch.root:
					h.left_leaf.left_leaf, h.left_leaf.right_leaf = branch.descendants
					self.head.append( h.left_leaf )
				# right_leaf
				elif h.right_leaf == branch.root:
					h.right_leaf.left_leaf, h.right_leaf.right_leaf = branch.descendants
					self.head.append( h.right_leaf )
			
			# prune head: remove those without descendants
			for h in self.head:
				if h.left_leaf is None and h.right_leaf is None:
					self.head.remove( h )
		
		# refresh leaves
		self.leaves = list()
		for l in self.head:
			if l.left_leaf.left_leaf is None and l.left_leaf.right_leaf is None:
				self.leaves.append( l.left_leaf )
			if l.right_leaf.right_leaf is None and l.right_leaf.left_leaf is None:
				self.leaves.append( l.right_leaf )
		
		
	def graft_branch( self, branch ):
		if self.root is None:
			self.root = branch.root
			for d in branch.descendants:
				d.parent = branch.root
				self.leaves.append( d )
		else:
			leaves_to_remove = list()
			print "leaves: ",self.leaves
			for leaf in self.leaves:
				print leaf, leaf.parent, leaf.parent.parent
			print
			leaves = list()
			for leaf in self.leaves:
				if leaf == branch.root:
					for d in branch.descendants:
						d.parent = leaf
						self.leaves.append( d )
					leaves_to_remove.append( leaf )
			
			for l in leaves_to_remove:
				self.leaves.remove( l )
			
			# self.leaves += leaves
			print "leaves: ", self.leaves
			for leaf in self.leaves:
				print leaf, leaf.parent, leaf.parent.parent
		
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
		leave_str = ", ".join( map( str, self.leaves ))
		#tree_str += "Leaves:\n\t%s\n" % ", ".join( map( str, self.leaves ))
		tree_str += "Leaves:\n\t%s\n" % leave_str
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
	
	def get_paths( self ):
		stack = list()
		path = list()
		count_leaves = len( self.leaves )
		current_node = self.root
		while count_leaves > 0:
			if current_node.left_leaf != None and current_node.right_leaf != None:
				if not current_node.left_leaf.flag and not current_node.right_leaf.flag:
					stack.append( current_node )
					current_node = current_node.left_leaf
				elif current_node.left_leaf.flag and not current_node.right_leaf.flag:
					stack.append( current_node )
					current_node = current_node.right_leaf
				elif not current_node.left_leaf.flag and current_node.right_leaf.flag:
					print >> sys.stderr, "How did I get here?"
				elif current_node.left_leaf.flag and current_node.right_leaf.flag:
					current_node = stack[-1]
					stack.pop()
			elif current_node.left_leaf == None and current_node.right_leaf == None:
				this_path = [ current_node ] + stack[::-1]
				path.append( this_path[::-1] )
				current_node.flag = True
				current_node = stack[-1]
				stack.pop()	
		
		return path