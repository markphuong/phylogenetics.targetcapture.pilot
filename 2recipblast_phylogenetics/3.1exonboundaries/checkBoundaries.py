import os
import sys
from collections import defaultdict

myfiles = [f for f in os.listdir('.') if os.path.isfile(f)]

mybeddict = defaultdict(list)

recorded = []

out = open('mybedfile', 'w')

for thing in myfiles:
	if '_newReference.fasta' in thing:
		#print thing

		bedfile = open(thing, 'r')

		templist = []

		for line in bedfile:
			info = line.strip().split('\t')
			if info[0] in recorded:
				if [info[1], info[2]] in mybeddict[info[0]]:
					continue
				else:
					print '\t'.join([info[0], info[1], info[2], thing])
					#print mybeddict[info[0]]


			else:
				if info[0] in mybeddict.keys():
					out.write('\t'.join([info[0], info[1], info[2], thing]) + '\n')
					mybeddict[info[0]].append([info[1], info[2]])
				else:
					out.write('\t'.join([info[0], info[1], info[2], thing]) + '\n')
					mybeddict[info[0]] = [[info[1], info[2]]]
					templist.append(info[0])
		
		for item in templist:
			recorded.append(item)

#print mybeddict