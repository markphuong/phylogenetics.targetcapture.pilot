#!/usr/bin/env python

#REQUIRES: novoalign and samtools
#REQUIRES: a map file, with first column as sample ID, and second file as which fasta it goes to. The reason you have different fastas for different samples is because of divergent mtDNA genomes
#elements in the map file are separated by a tab

#This script aligns your paired and unpaired reads to a reference using novoalign, and makes a pileup file using samtools

import os
import sys
import argparse
import multiprocessing
from Bio.Nexus import Nexus

def align(element):

	variables = dict(
	thefile = element,
	newfile = element[:-5] + 'nexus'
	) #name your output

	commands = """
	python fasta2Nexus.py {thefile} {newfile}
	""".format(**variables)

	cmd_list = commands.split("\n")
	for cmd in cmd_list:
		os.system(cmd)

thedir = [f for f in os.listdir('.') if os.path.isfile(f)]

file_list = []

for thing in thedir:
	if '_analyze.fasta' in thing:
		align(thing)
		file_list.append(thing[:-5] + 'nexus')


nexi =  [(fname, Nexus.Nexus(fname)) for fname in file_list]

combined = Nexus.combine(nexi)
combined.write_nexus_data(filename=open('conus_phylogeny.nexus', 'w'))
