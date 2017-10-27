import os
import sys
from collections import defaultdict


################## initialize cov ####################

mycov = open(sys.argv[1], 'r')

covdict = dict()

for line in mycov:
	info = line.strip().split('######')

	covlist = info[1][1:-1].split(', ')

	covlist = [int(thing) for thing in covlist]
	covdict[info[0]] = covlist


############### initialize het ########################

myhet = open(sys.argv[2], 'r')

hetdict = dict()

for line in myhet:
	info = line.strip().split('######')

	hetlist = info[1][1:-1].split(', ')

	hetlist = [int(thing) for thing in hetlist]
	hetdict[info[0]] = hetlist

##########################################

myblast = open(sys.argv[3], 'r')

blastlist = []

for line in myblast:
	blastlist.append(line.strip().split('\t')[1])

############################################ create lists full of 0s for unmapped loci


for thing in set(blastlist):
	if thing in covdict.keys():
		continue
	else:
		print thing
		print sys.argv[4]
		covdict[thing] = [0]*4000

for thing in set(blastlist):
	if thing in hetdict.keys():
		continue
	else:
		hetdict[thing] = [0]*4000


############ initialize blastoutput and store information like blast coordinates ############
myblast = open(sys.argv[3], 'r')

out1 = open(sys.argv[4] + '.myhet', 'w')
out2 = open(sys.argv[4] + '.mycov', 'w')
blastdict = defaultdict(list)

counter = 0

for line in myblast:

	info = line.strip().split('\t')

	if int(info[8]) > int(info[9]):
		start = int(info[9])
		end = int(info[8])
	else:
		start = int(info[8])
		end = int(info[9])		

	out1.write(info[0] + info[1] + '\t' + str(sum(hetdict[info[1]][start-1:end])/float(len(range(start-1,end)))) + '\n') 

	out2.write(info[0] + info[1] + '\t' + str(sum(covdict[info[1]][start-1:end])/float(len(range(start-1,end)))) + '\n')








