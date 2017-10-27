import os
import sys
from collections import defaultdict
from Bio.Seq import reverse_complement

thedir = [f for f in os.listdir('.') if os.path.isfile(f)]





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
 					print ID
					print locus
                                else:
                                	alreadyseen.append(locus)



