import os
import sys

thedir = [f for f in os.listdir('.') if os.path.isfile(f)]



splitdict = dict()

locusdict = dict()

species_num_loci = dict()

myconus = open('conus_phylogenetic_targets_sliced_v2.fa', 'r')


for line in myconus:
	if ">" in line:
		locusdict[line.strip()[1:]] = 0

for thing in thedir:
	if 'filtered_recipblast' in thing:
		ID = thing.split('_')[0]

		myblast = open(thing, 'r')


		alreadyseen = []


		for line in myblast:
			info = line.strip().split('\t')

			if info[0] in alreadyseen:
				continue
			else:
				locusdict[info[0]] += 1
				alreadyseen.append(info[0])



		species_num_loci[ID] = len(list(set(alreadyseen)))
		
		


out = open('num_species_per_target', 'w')

for thing in sorted(locusdict):
	out.write(thing + '\t' + str(locusdict[thing]) + '\n')

out.close()

out1 = open('num_targets_per_species' ,'w')

for item in species_num_loci:
	out1.write(item + '\t' + str(species_num_loci[item]) + '\n')

out1.close()







