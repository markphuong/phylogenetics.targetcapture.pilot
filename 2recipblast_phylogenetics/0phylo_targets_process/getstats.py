import os
import sys

myfasta = open('conus_phylogenetic_targets.fa', 'r')

lotlist = []

indexlist = []
adnanlist = []

seqlength = 0

for line in myfasta:
	if ">" in line:
		info = line.strip().split('|')
		lotID = info[0].split('_')[1]

		lotlist.append(lotID)

		if 'index' in info[0]:
			indexlist.append(lotID)
		else:
			adnanlist.append(lotID)
		
		seqlength += len(next(myfasta).strip())

print len(list(set(lotlist)))
print len(list(set(indexlist)))
print len(list(set(adnanlist)))
print seqlength
		