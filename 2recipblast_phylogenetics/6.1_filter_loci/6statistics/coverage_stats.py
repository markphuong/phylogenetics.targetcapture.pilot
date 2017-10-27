import os
import sys
from collections import defaultdict
from Bio.Seq import reverse_complement

thedir = [f for f in os.listdir('.') if os.path.isfile(f)]

out = open('cov.stats', 'w')

out2 = open('divergence', 'w')

for thing in thedir:
        if '_coverage' in thing:


                ID = thing.split('_')[0]


                mycov = open(thing, 'r')
		
		covdict = dict()

		covcounter = 0
		covlength = 0
		
                for line in mycov:
			
			
			info = line.strip().split('\t')

			covcounter += float(info[2])
			covlength += 1

			if info[0] in covdict.keys():
				del covdict[info[0]]
			else:
				covdict[info[0]] = info[2]

		out.write(ID + '\t' + str(covcounter/covlength) + '\n')

                myblast = open(ID + '_6.1_filtered_recipblast', 'r')
		
                for line in myblast:

			info = line.strip().split('\t')

			if info[0] in covdict.keys():
				out2.write(ID + '\t' + info[0] + '\t' + str(100.00-float(info[2])) + '\t' + covdict[info[0]] + '\t' + info[0].split('|')[2] + '\t'+ info[0].split('|')[3]+ '\n')
			


















