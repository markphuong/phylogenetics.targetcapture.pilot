myfasta = open('phylogenetic_markers_final.fa', 'r')

seqlen = 0

for line in myfasta:
	if ">" in line:
		seq = next(myfasta).strip()

		if len(seq) > 670:
			seqlen += len(seq)

print seqlen 	


myfasta2 = open('conus_phylogenetic_targets.fa', 'r')

loci = []

for line in myfasta2:
	if ">" in line:
		loci.append(line.strip().split('|')[0].split('_')[1])

print len(list(set(loci)))

#print list(set(loci))

myfasta2 = open('phylogenetic_markers_final.fa', 'r')

loci2 = []

for line in myfasta2:
	if ">" in line:
		loci2.append(line.strip().split('_')[1])

print len(list(set(loci2)))

print list(set(loci2)-set(loci))

