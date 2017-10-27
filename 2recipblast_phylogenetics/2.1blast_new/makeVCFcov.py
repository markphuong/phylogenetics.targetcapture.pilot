import os
import sys
from collections import defaultdict


########### initialize fastafile ###############

myfasta = open(sys.argv[1], 'r')

lengthdict = dict()

for line in myfasta:
	if ">" in line:
		lengthdict[line.strip()[1:]] = len(next(myfasta).strip())


############ initialize blastoutput ############
myblast = open(sys.argv[2], 'r')


blastlist = []

counter = 0

for line in myblast:

	info = line.strip().split('\t')

	blastlist.append(info[1])

############################# initialize VCF

vcfdict = defaultdict(list)

myvcf = open(sys.argv[3], 'r')

prevpos = 0
for line in myvcf:
	if '#' in line:
		continue
	else:
		info = line.strip().split('\t')
		if info[0] in blastlist:

			depth = int(info[7].split(';')[0].split('=')[1])

			if info[0] in vcfdict.keys():
				if prevpos == depth-1:
					vcfdict[info[0]].append(depth)
					prevpos = int(info[1])
				else:
					mylist = [0] * (int(info[1]) - prevpos - 1)


					for item in mylist:
						vcfdict[info[0]].append(item)
					vcfdict[info[0]].append(depth)
					prevpos = int(info[1])

			elif info[1] == '1':
				vcfdict[info[0]] = [depth]
				prevpos = 1
			else:

				mylist = [0] * (int(info[1]) - 1)
				mylist.append(depth)
				vcfdict[info[0]] = mylist
				prevpos = int(info[1])
		else:
			continue

############################################

out = open(sys.argv[4], 'w')

for key in vcfdict:

	if lengthdict[key] == len(vcfdict[key]):
		out.write(key + '######' + str(vcfdict[key]) + '\n')
	else:
		difference = lengthdict[key] - len(vcfdict[key])

		vcfdict[key].extend([0 for i in range(difference)])

		out.write(key + '######' + str(vcfdict[key]) + '\n')
		print len(vcfdict[key])















