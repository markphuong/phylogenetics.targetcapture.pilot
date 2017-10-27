mytargets = open('target_species_coverage', 'r')


keeplist = []

for line in mytargets:
	info = line.strip().split('\t')
	if int(info[1]) > 26:
		keeplist.append(info[0].replace('|', '-') + '.exonfasta.aligned')

print len(keeplist)