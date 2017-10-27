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


thedir = [f for f in os.listdir('.') if os.path.isfile(f)]

counter = 0


out = open('removed_overlappers', 'w')

for thing in thedir:
	if 'filtered_recipblast' in thing:
		ID = thing.split('_')[0]

		myblast = open(thing, 'r')

		blastdict = defaultdict(list)

		for line in myblast:
			info = line.strip().split('\t')

			if int(info[8]) > int(info[9]):
				start = int(info[9])
				end = int(info[8])
			else:
				start = int(info[8])
				end = int(info[9])	

			if info[1] in blastdict.keys():
	
				blastdict[info[1]].append([info[0], [start, end], line])
				counter += 1
			else:
				blastdict[info[1]] = [[info[0], [start, end], line]]
				counter += 1

		badlist = []

		for key in blastdict:
			if len(blastdict[key]) > 1:
				for value1 in blastdict[key]:
					for value2 in blastdict[key]:


						if value1 == value2:
							continue

						elif checkoverlap(value1[1], value2[1]) != 0:
							badlist.append(value1[2])
							badlist.append(value2[2])


		badlist = list(set(badlist))

		for item in badlist:
			out.write(ID + '\t' + 'overlapper' + '\t' +  item)

		








			