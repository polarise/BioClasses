import sys
from Node import *	
from Branch import *

class Paths( object ):
	"""
	A class that constructs paths from branches
	"""
	def __init__( self ):
		"""
		initiate an empty Paths object
		"""
		self.paths = list()
		self.branches = dict()
	
	def extend( self, branch ):
		"""
		Consider the branch and generate all possible paths in path
		"""
		new_paths = list() # a new list to put new paths
		if len( self.paths ) == 0: # if we're starting from scratch...
			for d in branch.descendants: # for each descendant in the branch...
				new_paths.append([ d, branch.root ] ) # create a list ending in the branch root
		else: 
			for d in branch.descendants: # for each descendant in the branch...
				for p in self.paths: # for each path we already had...
					if p[0] == branch.root: # if the leaf resembles the branch root...
						new_paths.append( [d] + p ) # extend this path; put in our new list
					else:
						if p not in new_paths: # otherwise, put only one copy in our new list
							new_paths.append( p )
		
		self.paths = new_paths # sub the paths with the updated list of paths
		self.branches[ branch.root.identify() ] = branch # record this branch
	
	def get_path_sequences( self, leaf ):
		"""
		Return a list of all paths having leaf as its terminus
		"""
		path_sequences = list()
		for p in self.paths:
			if p[0] == leaf:
				path_sequences.append( map( lambda x: x.name, p[::-1] ))
		
		return path_sequences
	
	def get_all_path_sequences( self ):
		"""
		Return all paths present from the branches
		"""
		all_path_sequences = list()
		for p in self.paths:
			all_path_sequences.append( map( lambda x: x.name, p[::-1] ))
		
		return all_path_sequences
