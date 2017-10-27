import os
import sys
from collections import defaultdict
from Bio.Seq import reverse_complement

thedir = [f for f in os.listdir('.') if os.path.isfile(f)]


conus = open('conus_phylogenetic_targets_sliced_v2.fa', 'r')

conusdict = dict()

for line in conus:
        if ">" in line:
                conusdict[line.strip()[1:]] = 0


for thing in thedir:
        if 'loci_v2.fa' in thing:


                ID = thing.split('_')[0]


                myfasta = open(thing, 'r')

                alreadyseen = []

                for line in myfasta:
                        if ">" in line:
                                info = line.strip().split('|')

                                locus = '|'.join(info[-5:])


                                if locus in alreadyseen:
 					continue
                                else:
                                	alreadyseen.append(locus)
                                        conusdict[locus] += 1

out = open('target_species_coverage', 'w')

for thing in conusdict:
        out.write(thing + '\t' + str(conusdict[thing]) + '\n')
