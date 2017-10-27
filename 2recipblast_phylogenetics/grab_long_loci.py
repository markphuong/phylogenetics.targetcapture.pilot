import os
import sys

myfasta = open('conus_phylogenetic_targets_sliced.fa', 'r')

for line in myfasta:
	if ">" in line:
		seq = next(myfasta).strip()

		if len(seq) > 500:
			print line
