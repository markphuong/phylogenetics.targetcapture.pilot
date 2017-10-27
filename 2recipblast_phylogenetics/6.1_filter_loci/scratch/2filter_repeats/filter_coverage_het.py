import os
import sys
import numpy
from collections import defaultdict

myremoved = open('blast_output_removed', 'r')

removed = defaultdict(list)

for line in myremoved:
	info = line.strip().split('\t')

	if info[0] in removed.keys():
		removed[info[0]].append('\t'.join(info[2:]))
	else:
		removed[info[0]] = ['\t'.join(info[2:])]
#print removed


thedir = [f for f in os.listdir('.') if os.path.isfile(f)]

counter = 0



for thing in thedir:
	if 'filtered_recipblast' in thing and 'MAP13' in thing:
		
		out = open('results', 'w')

		ID = thing.split('_')[0]

		myfasta = open(ID + '_phylo_contigs.fasta', 'r')

		fastadict = dict()

		for line in myfasta:
			if ">" in line:
				fastadict[line.strip()[1:]] = next(myfasta).strip()


		mycov = open(ID + '.exon.cov', 'r')

		covdict = dict()

		for line in mycov:
			info = line.strip().split('######')

			covlist = info[1][1:-1].split(', ')

			covlist = [int(thing) for thing in covlist]
			covdict[info[0]] = covlist

		myhet = open(ID + '.exon.het', 'r')

		hetdict = dict()

		for line in myhet:
			info = line.strip().split('######')

			hetlist = info[1][1:-1].split(', ')

			hetlist = [int(thing) for thing in hetlist]
			hetdict[info[0]] = hetlist		


		myblast = open(ID + '_6.1_filtered_recipblast', 'r')

		blastlist = []

		for line in myblast:
			blastlist.append(line.strip().split('\t')[1])

		myblast.close()

		for thing in set(blastlist):
			if thing in covdict.keys():
				continue
			else:
				covdict[thing] = [0]*4000

		for thing in set(blastlist):
			if thing in hetdict.keys():
				continue
			else:
				hetdict[thing] = [0]*4000

		myblast = open(ID + '_6.1_filtered_recipblast', 'r')

		outcov = open('low_cov_removed', 'a')

		keeplist = []

		myhetlist = []

		for line in myblast:
			info = line.strip().split('\t')

			if line.strip() in removed[ID]:
				continue
			else:
				if int(info[8]) > int(info[9]):
					start = int(info[9])
					end = int(info[8])
				else:
					start = int(info[8])
					end = int(info[9])	

				myseq = fastadict[info[1]][start-1:end]
				thecov = covdict[info[1]][start-1:end]			
				thehet = hetdict[info[1]][start-1:end]
				
				outseq = ''

				covcounter = 0

				hetcounter = 0

				lengthcounter = 0

				for i in range(0,len(myseq)):
					covcounter += thecov[i]

					if thecov[i] > 4:
						outseq = outseq + myseq[i]
						hetcounter += thehet[i]
						lengthcounter += 1

					else:
						outseq = outseq + 'N'


				if float(lengthcounter)/len(myseq) < 0.7:
					outcov.write(ID + '\t' + 'low_cov' + '\t'+ line)

				else:

					keeplist.append([info[0], info[1], float(covcounter)/len(myseq), float(hetcounter)/lengthcounter, float(lengthcounter)/len(myseq), outseq,  line])
					myhetlist.append(float(hetcounter)/lengthcounter)
					out.write(str(float(hetcounter)/lengthcounter) + '\n')


		themean = numpy.mean(myhetlist)
		stdev = numpy.std(myhetlist)

		mycutoff = themean + stdev*2

		outhet = open('high_het_removed', 'a')


		for item in keeplist:
			if item[3] >= mycutoff:
				outhet.write(ID + '\t' + 'high_het' + '\t' + item[-1])

			else:
				out.write(">" + ID + '|' + item[1] + '|' + str(item[2]) + '|' + str(item[3]) + '|' + str(item[4]) + '|' + item[0] + '\n')
				out.write(item[-2] + '\n')
			
				#if lengthcounter == 0:
				#	out.write('\t'.join([info[0], info[1], str(float(covcounter)/len(myseq)), '0', str(float(lengthcounter)/len(myseq))]) + '\n'), 
				#else:
				#	out.write('\t'.join([info[0], info[1], str(float(covcounter)/len(myseq)), str(float(hetcounter)/lengthcounter), str(float(lengthcounter)/len(myseq))]) + '\n'), 
					
				
				













