import os
import sys






thedir = [f for f in os.listdir('.') if os.path.isfile(f)]


for thing in thedir:
	if not "cap" in thing:
		if "contigs.fasta" in thing:
			myfile = open(thing, 'r')

			for line in myfile:
				if "NODE_14314_length_467_cov_11.4564_ID_28635" in line:
					print thing 
