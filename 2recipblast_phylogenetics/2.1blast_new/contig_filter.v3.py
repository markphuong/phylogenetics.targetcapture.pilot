import os
import sys
from collections import defaultdict

def checkoverlap(a, b):
	overlap = max(0, min(a[1], b[1]) - max(a[0], b[0]))
        length1 = len(range(a[0],a[1]+1))

	length2 = len(range(b[0],b[1]+1))

	ratio1 = float(overlap)/length1
	ratio2 = float(overlap)/length2

	return max(ratio1, ratio2)

#################### initialize cov ####################

mycov = open(sys.argv[1], 'r')

covdict = dict()

for line in mycov:
	info = line.strip().split('######')

	covlist = info[1][1:-1].split(', ')

	covlist = [int(thing) for thing in covlist]
	covdict[info[0]] = covlist


############ initialize blastoutput and store information like blast coordinates ############
myblast = open(sys.argv[3], 'r')


blastdict = defaultdict(list)

counter = 0

for line in myblast:

	info = line.strip().split('\t')

	if info[0] in blastdict.keys():
		blastdict[info[0]].append([info[1], info[6], info[7],info[8], info[9], str(counter)])
	else:
		blastdict[info[0]] = [[info[1], info[6], info[7],info[8], info[9], str(counter)]]

	counter += 1

myblast.close()

############################################ create lists full of 0s for unmapped loci

for key in blastdict.keys():
	for value in blastdict[key]:
		if value[0] in covdict.keys():
			continue
		else:
			covdict[value[0]] = [0]*4000


############################################

exclude_dict = defaultdict(list)


for key in blastdict.keys():
	alreadydone = []


##### value1 and value2 are lists containing the blast info #######

######## do all unique pairwise comparisons and check if they overlap. if they do, choose the contig with the higher coverage (to keep for now)

	for value1 in blastdict[key]:
		for value2 in blastdict[key]:
			ref1 = '_'.join(value1)
			ref2 = '_'.join(value2)
			
			phrase1 = ref1 + '-' + ref2
			phrase2 = ref2 + '-' + ref1
			
			if phrase1 in alreadydone or phrase2 in alreadydone:
				continue
			elif phrase1 == phrase2:
				continue
			else:
				alreadydone.append(phrase1)
				alreadydone.append(phrase2)
				

				a = [int(value1[1]), int(value1[2])]
				b = [int(value2[1]), int(value2[2])]

				if checkoverlap(a,b)> .2:

######################################### get the coverage for the two contigs for just the part that blasted.

                                        if int(value1[3]) < int(value1[4]):
						mycov1 = covdict[value1[0]][int(value1[3])-1:int(value1[4])]
                                        else:
						mycov1 = covdict[value1[0]][int(value1[4])-1:int(value1[3])]

					mydepth1 = sum(mycov1)/float(len(mycov1))

                                        if int(value2[3]) < int(value2[4]):
						mycov2 = covdict[value2[0]][int(value2[3])-1:int(value2[4])]
                                        else:
						mycov2 = covdict[value2[0]][int(value2[4])-1:int(value2[3])]
					mydepth2 = sum(mycov2)/float(len(mycov2))
				
##################################### exclude dict goes exclude_dict => target => blast list

##################################### pile up blast results into exclude_dict that have another contig with higher coverage

					if mydepth1 > mydepth2:
						if key in exclude_dict:
							exclude_dict[key].append(value2)
						else:
							exclude_dict[key] = [value2]
					else:
						if key in exclude_dict:
							exclude_dict[key].append(value1)
						else:
							exclude_dict[key] = [value1]

out1 = open(sys.argv[4] + '_removed', 'w')

out2 = open(sys.argv[4] + '_filtered_recipblast', 'w')


myblast = open(sys.argv[3], 'r')


blastdict = defaultdict(list)

counter = -1

### go through the blast file again, if it is found in the exclude_dict and matches perfectly what is in the exclude dict, put it in the 'removed' file, if it is not in the exclude dict, put it in the 'filtered' file
for line in myblast:
	counter += 1

	remove = 'no'
	info = line.strip().split('\t')

	key = info[0]

	thelist = [info[1], info[6], info[7],info[8], info[9], str(counter)]

	if key in exclude_dict.keys():
		for thing in exclude_dict[key]:
			if thelist == thing:
				remove = 'yes'
			else:
				continue


		if remove == 'no':
			out2.write(line)
		else:
			out1.write(line)
	else:
		out2.write(line)

















