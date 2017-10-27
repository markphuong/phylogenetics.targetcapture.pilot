
badlist = []

mybad = open('fuck', 'r')

for line in mybad:
	info = line.strip().split('\t')[0].split('|')[0]
	badlist.append(info)


################# only 456 loci got included in the first design, with no exon boundaries. this parses the baits fasta file, and 

mybaits = open('phylo670-bait-120-60.fas', 'r')

firstlist = []

for line in mybaits:
	if ">" in line:
		firstlist.append('_'.join(line.strip().split('_')[:-1])) 



out = open('conus_phylogenetic_targets.fa', 'w')

myfasta = open('phylogenetic_markers_final.fa', 'r')

counter = 0

exonlen = 0

for line in myfasta:
	if ">" in line:
		if line.strip() in firstlist:
			out.write(line.strip() + '|noex|first_design|no_exon_boundaries' + '\n')

			seq = next(myfasta)

			out.write(seq)
			counter += 1
			exonlen += len(seq.strip())
print counter
print exonlen


######################## in the second design, grab the exons that made up the second addition of baits


myconoidea = open('conoidea.fin', 'r')

conoideadict = dict()

for line in myconoidea:
	if ">" in line:
		conoideadict[line.strip()] = next(myconoidea)

myfasta2 = open('conus_addmore_final.fasta', 'r')

mycounter = 0
mycounter2 = 0
for line in myfasta2:
	if ">" in line:
		mycounter += len(next(myfasta2).strip()) #counts seq length for 'conus_addmore_final.fasta'
		if 'exon' in line:
			exons = line.strip().split('|')[-1].split('_')
			info = '|'.join(line.strip().split('|')[:-1])


			if info[1:] in badlist:
				print info
				continue

			for thing in exons:

				if 'exon' in thing:
					continue
				else:
					myID = info + '|exon' + thing
					out.write(myID + '|second_design|exon_sliced' + '\n')
					out.write(conoideadict[myID])
					mycounter2 += len(conoideadict[myID].strip())


		else:
			out.write(line.strip() + '|noex|second_design|no_exon_boundaries' + '\n')
			out.write(conoideadict[line.strip()])
			mycounter2 += len(conoideadict[line.strip()].strip())

print mycounter
print mycounter2








