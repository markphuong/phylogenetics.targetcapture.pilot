import os
import sys

thedir = [f for f in os.listdir('.') if os.path.isfile(f)]

out = open('summary_blasthits', 'w')

splitdict = dict()

for thing in thedir:
	if 'filtered_recipblast.sorted' in thing:
		ID = thing.split('_')[0]

		myblast = open(thing, 'r')


		blastlist = []

		repeats = []

		for line in myblast:
			info = line.strip().split('\t')

			if info[0] in blastlist:
				repeats.append(info[0])
				out.write(ID + '\t' + info[0] + '\n')

			blastlist.append(info[0])

		for item in set(repeats):
			if item in splitdict.keys():
				splitdict[item] += 1
			else:
				splitdict[item] = 1
		

for key in splitdict:
	print key
	print splitdict[key]
		
			