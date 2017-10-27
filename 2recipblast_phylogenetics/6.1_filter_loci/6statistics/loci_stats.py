import os
import sys

myfile = open('num_species_per_target', 'r')

infodict = dict()

for line in myfile:
	info = line.strip().split('\t')

	infodict[info[0]] = [info[1], 0, 0, 0]

myoverlap = open('removed_overlappers', 'r')

for line in myoverlap:
	info = line.strip().split('\t')

	infodict[info[2]][1] += 1

mylowcov = open('removed_low_cov', 'r')

for line in mylowcov:
	info = line.strip().split('\t')

	infodict[info[2]][2] += 1

myhighhet = open('removed_high_het', 'r')

for line in myhighhet:
	info = line.strip().split('\t')

	infodict[info[2]][3] += 1

out = open('summarystats', 'w')

for thing in infodict:
	output = [str(x) for x in infodict[thing]]
	out.write(thing + '\t' + '\t'.join(output) + '\n')















