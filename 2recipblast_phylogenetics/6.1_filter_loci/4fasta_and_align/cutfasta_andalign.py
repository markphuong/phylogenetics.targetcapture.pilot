import os
import sys
from collections import defaultdict
from Bio.Seq import reverse_complement


thedir = [f for f in os.listdir('.') if os.path.isfile(f)]


for thing in thedir:
	if 'loci_v2.fa' in thing:
		

		ID = thing.split('_')[0]


		myfasta = open(thing, 'r')

		alreadyseen = []

		for line in myfasta:
			if ">" in line:
				info = line.strip().split('|')

				locus = '|'.join(info[-5:])


				out = open(locus.replace('|','-') + '.exonfasta', 'a')

:
				out.write(line)
				out.write(next(myfasta))

				out.close()



thedir = [f for f in os.listdir('.') if os.path.isfile(f)]


for thing in thedir:
	if 'exonfasta' in thing:
		cmd = 'mafft --adjustdirection ' + thing + ' > ' + thing + '.aligned'
		os.system(cmd)






















