import os
import sys

thedir = [f for f in os.listdir('.') if os.path.isfile(f)]

for thing in thedir:
	if '_filtered_recipblast' in thing:
		

		ID = thing.split('_')[0]

		blastlist = []


		myblast = open(ID + '_4.1_filtered_recipblast', 'r')

		for line in myblast:

			info = line.strip().split('\t')
			blastlist.append(info[1])			



		out = open(ID + '_phylo_contigs.fasta', 'w')

		myfasta = open(ID + '_assemblies_clustered.fasta.NI', 'r')

		for line in myfasta:
			if ">" in line:
				contig = line.strip()[1:]
				if contig in set(blastlist):
					out.write(line)
					out.write(next(myfasta))

		out.close()

		print len(list(set(blastlist)))
		print ID



