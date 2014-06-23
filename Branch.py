from __future__ import division
import sys

class Branch( object ):
  def __init__( self, root_node, desc1, desc2 ):
    self.root = root_node
    self.descendants = [ desc1, desc2 ]