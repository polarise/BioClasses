# -*- encoding: utf-8 -*-

class FrameshiftSequence( object ):
	def __init__( self, sequence, path ):
		self.path = path
		self.frameshifted_sequence, self.fragments, self.signals = self.frameshift_from_path( sequence, path )
		self.length = len( self.frameshifted_sequence )
		self.frameshift_count = len( self.path ) - 1
			
	def frameshift_from_path( self, sequence, path ):
		"""
		"""
		# first get all frame of sequence
		sequence_in_frames = dict()
		for i in xrange( 3 ):
			sequence_in_frames[i] = sequence[i:]
		
		frameshifted_sequence = ""
		fragments = list()
		frameshift_signals = list()
		i = 0
		f_i = 0
		for f,j in path:
			frameshifted_sequence += sequence[i+(f-f_i):j]
			fragments.append( sequence[i+(f-f_i):j] )
			frameshift_signals.append( sequence[j-3:j+3] )
			i = j
			f_i = f
		
		# we could factor in the last trivial frameshift...
		frameshifted_sequence += sequence[-1]
		fragments[-1] += sequence[-1]
				
		return frameshifted_sequence, fragments, frameshift_signals[:-1]