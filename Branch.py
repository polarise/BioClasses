from __future__ import division
import sys

class Branch( object ):
  def __init__( self, root_node, left_leaf, right_leaf ):
    self.root_node = root_node
    self.left_leaf = left_leaf
    self.right_leaf = right_leaf
    
    # set the root attribute for the leaves
    self.left_leaf.root = self.root_node
    self.right_leaf.root = self.root_node
    
    # set the direction attribute
    self.left_leaf.is_left = True
    self.right_leaf.is_left = True
    
    # set the parent branch attribute
    self.root_node.parent_branch = self
    self.left_leaf.parent_branch = self
    self.right_leaf.parent_branch = self
  
  def __repr__( self ):
    return "Branch root: %s; Left node: %s; Right node: %s" % ( self.root_node, self.left_leaf, self.right_leaf )