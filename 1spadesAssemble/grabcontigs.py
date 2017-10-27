#!/usr/bin/env python

#this concatenates all read files into read1 and read2 files [if you get multiple read files per index from illumina]

import os
import sys
import argparse
import multiprocessing



directory = os.getcwd()


def concat(path,filename):


	variables = dict(
	ID = path.split('/')[-2],
	path = path)

	commands = """
	mv {path} {ID}_contigs.fasta
	""".format(**variables)

	cmd_list = commands.split("\n")
	for cmd in cmd_list:
		os.system(cmd)



for root, dirs, files in os.walk(directory):
	for filename in files:
		path = os.path.join(root, filename)
		if '/contigs.fasta' in path:
			concat(path,filename)
		else:
			continue




