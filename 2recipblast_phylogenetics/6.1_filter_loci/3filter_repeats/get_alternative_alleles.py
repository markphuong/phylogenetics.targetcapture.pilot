import os
import sys


thedir = [f for f in os.listdir('.') if os.path.isfile(f)]


counter = 0

out = open('alternative_alleles', 'w')

for thing in thedir:
	if '.vcf' in thing:
		ID = thing.split('_')[0]

		myvcf = open(thing, 'r')


		for line in myvcf:
			if "#" in line:
				continue
			else:
				info = line.strip().split('\t')

				if info[4] != '.' and '1/1:' in line:
					out.write(ID + '\t' + info[0] + '\t'+ info[1] + '\t' + info[4] + '\t' + '1/1' + '\n')
				elif info[4] != '.' and '0/1:' in line:
					out.write(ID + '\t' + info[0] + '\t'+ info[1] + '\t' + info[4] + '\t' + '0/1' + '\n')

