import os
import sys



out = open('paralogous', 'w')


for i in range(1,33):
	mystats = open('summarystats', 'r')

	IDlist = []
	exonlist = []
	for line in mystats:
		info = line.strip().split('\t')

		paralog = int(info[4])

		ID = info[0].split('|')[0].split('_')[1]

		if paralog >= i:
			IDlist.append(ID)
			exonlist.append(info[0])

	mystats.close()

	out.write(str(i) + '\t' + str(len(list(set(IDlist)))) + '\t' + str(len(list(set(exonlist)))) + '\n')
 