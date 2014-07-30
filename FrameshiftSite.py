# -*- encoding: utf-8 -*-
from __future__ import division
import sys

class FrameshiftSite( object ):
	def __init__( self, initial_node, final_node, signal, probability, radians_vector ):
		self.initial_frame = initial_node[0]
		self.final_frame = final_node[0]
		self.position = initial_node[1]
		desig = self.final_frame - self.initial_frame
		if desig == 1:
			self.designation = "+1"
		elif desig == 2:
			self.designation = "+2"
		elif desig == -1:
			self.designation = "-1"
		elif desig == -2:
			self.designation = "-2"
		self.signal = signal
		self.probability = "%.4f" % probability
		self.radians_vector = "%.4f\t%.4f\t%.4f" % radians_vector