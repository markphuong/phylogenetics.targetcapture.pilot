import os
import sys
import numpy
from collections import defaultdict




#################################### get dictionary of the overlappers


altdict =defaultdict(dict)

myalternatives = open('test', 'r')

for line in myalternatives:
	info = line.strip().split('\t')

	if info[0] in altdict.keys() and info[1] in altdict[info[0]].keys():

		altdict[info[0]][info[1]].append([int(info[2]), info[3], info[4]])
	else:
		altdict[info[0]][info[1]] = [ [int(info[2]), info[3], info[4]] ]
		

therange = range(200,1000)

if 'Contig3' in altdict['80442']:
	for item in altdict['80442']['Contig3']:
		if item[0] in therange:
			print 'what'