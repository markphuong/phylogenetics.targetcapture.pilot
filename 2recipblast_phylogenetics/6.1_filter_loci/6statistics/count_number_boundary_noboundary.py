import os
import sys

myfasta = open('conus_phylogenetic_targets_sliced_v2.fa', 'r')

boundarylist = []
noboundarylist = []

for line in myfasta:
	if ">" in line:
		if 'no_exon_boundaries' in line:
			info = line.strip().split('|')[0].split('_')[1]
			noboundarylist.append(info)

		else:
			info = line.strip().split('|')[0].split('_')[1]
			boundarylist.append(info)


print list(set(boundarylist))
print list(set(noboundarylist))
print len(list(set(boundarylist)))
print len(list(set(noboundarylist)))