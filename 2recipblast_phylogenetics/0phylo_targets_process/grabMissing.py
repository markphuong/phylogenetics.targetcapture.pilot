mylist = []
fasta1 = open('phylo670-bait-120-60.fas', 'r')
fasta2 = open('phylogenetic_markers_final.fa', 'r')

for line in fasta1:
	if ">" in line:
		mylist.append(line.strip().split('_')[1])




out = open('notpresentinDesign','w')

for line in fasta2:
	if ">" in line:
		if line.strip().split('_')[1] in list(set(mylist)):
			
			continue
		else:
#			continue
#			print line.strip().split('_')[1]
			out.write(line.strip().split('_')[1] + '\n')

