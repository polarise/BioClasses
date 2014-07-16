#!/usr/bin/env python
import sys
import glob

def main():
	with open( glob.glob( "~/bioinf/Translational_Frameshifting/2_Euplotes_data/ALLCDS.fa" )) as f:
		c = 0
		for row in f:
			if c > 10: break
			print row.strip()
			c += 1

if __name__ == "__main__":
	main()