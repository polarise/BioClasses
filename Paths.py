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
		new_paths = list()
		if len( self.paths ) == 0:
			for d in branch.descendants:
				new_paths.append([ d, branch.root ] )
		else:
			for d in branch.descendants:
				for p in self.paths:
					if p[0] == branch.root:
						new_paths.append( [d] + p )
					else:
						if p not in new_paths:
							new_paths.append( p )
		
		self.paths = new_paths
		self.branches[ branch.root.identify() ] = branch
	
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
