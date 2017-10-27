import os
import sys
from collections import defaultdict
from Bio.Seq import reverse_complement

thedir = [f for f in os.listdir('.') if os.path.isfile(f)]

out = open('length_loci_recovered.stats', 'w')


totalgenelist = []
finalexonlist = []

for thing in thedir:
        if '_6.1_filtered_recipblast' in thing:


                ID = thing.split('_')[0]


                myblast = open(thing, 'r')

                seqlength = 0
		adnanlist = []
		indexlist = []
		exonlist = []

		genelist = []

                for line in myblast:
			info = line.strip().split('\t')
			
			seqlength += int(info[3])

			if 'index' in info[0]:
				indexlist.append(info[0].split('|')[0].split('_')[1])				
			else:
				adnanlist.append(info[0].split('|')[0].split('_')[1])				
			genelist.append(info[0].split('|')[0].split('_')[1])
			finalexonlist.append(info[0])
			exonlist.append(info[0])
			totalgenelist.append(info[0].split('|')[0].split('_')[1])


		out.write(ID + '\t' + str(seqlength) + '\t' + str(len(list(set(adnanlist)))) + '\t' + str(len(list(set(indexlist)))) + '\t' + str(len(list(set(exonlist)))) + '\t' + str(len(list(set(genelist)))) +'\n')



print len(list(set(totalgenelist)))
print len(list(set(finalexonlist)))
