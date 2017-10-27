import os
import sys
from collections import defaultdict


########### initialize fastafile ###############

myfasta = open(sys.argv[1], 'r')

lengthdict = dict()

for line in myfasta:
	if ">" in line:
		lengthdict[line.strip()[1:]] = len(next(myfasta).strip())


############################# initialize VCF

vcfdict = defaultdict(list)

heterodict = defaultdict(list)

myvcf = open(sys.argv[2], 'r')


for line in myvcf:
	if '#' in line:
		continue
	else:
		info = line.strip().split('\t')

		depth = int(info[7].split(';')[0].split('=')[1])

		if info[4] != '.' and '0/1' in line:
			het = 1
		else:
			het = 0

		if info[0] in vcfdict.keys():
			if prevpos == depth-1:
				vcfdict[info[0]].append(depth)
				heterodict[info[0]].append(het)
				prevpos = int(info[1])
			else:
				mylist = [0] * (int(info[1]) - prevpos - 1)


				for item in mylist:
					vcfdict[info[0]].append(item)
					heterodict[info[0]].append(item)
				vcfdict[info[0]].append(depth)
				heterodict[info[0]].append(het)
				prevpos = int(info[1])

		elif info[1] == '1':
			vcfdict[info[0]] = [depth]
			heterodict[info[0]] = [het]
			prevpos = 1
		else:

			mylistdepth = [0] * (int(info[1]) - 1)
			mylistdepth.append(depth)
			vcfdict[info[0]] = mylistdepth

			mylisthet = [0] * (int(info[1]) - 1)
			mylisthet.append(het)
			heterodict[info[0]] = mylisthet

			prevpos = int(info[1])


############################################

out = open(sys.argv[3], 'w')
out2 = open(sys.argv[4], 'w')

for key in vcfdict:

	if lengthdict[key] == len(vcfdict[key]):
		out.write(key + '######' + str(vcfdict[key]) + '\n')
		out2.write(key + '######' + str(heterodict[key]) + '\n')
	else:
		difference = lengthdict[key] - len(vcfdict[key])

		vcfdict[key].extend([0 for i in range(difference)])
		heterodict[key].extend([0 for i in range(difference)])

		out.write(key + '######' + str(vcfdict[key]) + '\n')
		out2.write(key + '######' + str(heterodict[key]) + '\n')
		
















