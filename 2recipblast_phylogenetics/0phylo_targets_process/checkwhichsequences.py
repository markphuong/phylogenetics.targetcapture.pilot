mybaits = open('phylo670-bait-120-60.fas', 'r')

seenlist = []

for line in mybaits:
	if ">" in line:
		seenlist.append('_'.join(line.strip().split('_')[:-1]))

myfasta = open('phylogenetic_markers_final.fa', 'r')

out = open('fullname_notpresentinDesign', 'w')

for line in myfasta:
	if ">" in line:
		if line.strip() in seenlist:
			continue
		else:
			out.write(line)