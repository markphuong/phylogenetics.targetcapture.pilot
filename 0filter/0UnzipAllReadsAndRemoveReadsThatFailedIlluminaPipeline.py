#!/usr/bin/env python

#this concatenates all read files into read1 and read2 files [if you get multiple read files per index from illumina]

import os
import sys
import argparse
import multiprocessing

#manip these variables

ID = 'MAMP' #An ID common to all fastq files

### the script

directory = os.getcwd()


def concat(element):
	
	newname = element.split('/')
	newname = newname[-1]
	newname = newname[:-3]

	variables = dict(
	index = str(element),
	newfile = str(newname))

	commands = """
	echo "Processing {index}"
	zcat {index} | grep -A 3 '^@.* [^:]*:N:[^:]*:' | grep -v "^--$" | sed 's/ 1:N:0:.*/\\/1/g' | sed 's/ 2:N:0:.*/\\/2/g' > {newfile}
	""".format(**variables)

	cmd_list = commands.split("\n")
	for cmd in cmd_list:
		os.system(cmd)

mylist = []

for root, dirs, files in os.walk(directory):
	for filename in files:
		path = os.path.join(root, filename)
		if ID in filename:	
			mylist.append(path)
		else:
			continue

pool = multiprocessing.Pool()
pool.map(concat, mylist)


