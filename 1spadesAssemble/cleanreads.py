#!/usr/bin/env python

#flash manual: http://ccb.jhu.edu/software/FLASH/MANUAL

#This script aligns your paired and unpaired reads to a reference using novoalign, and makes a pileup file using samtools

import os
import sys
import argparse
import multiprocessing

#this is a wrap around for novoalign and samtools where each sample identifier was "index#" where # was a number between 1 - 50

def get_args(): #arguments needed to give to this script
	parser = argparse.ArgumentParser(description="run blastx")

	#forces required argument to let it run
	required = parser.add_argument_group("required arguments") 
	required.add_argument("--map", help="textfile with samples to run and what fasta file to match it to", required=True) #A map file with the sample ID and the fasta file it goes to

	return parser.parse_args()


def align(element):



	variables = dict(
	adfile = 'ADAPTERS.txt',
	trimmomatic = '/nfs/LabShared/MarkPhuong/exonCapturePilot/0filter/Trimmomatic-0.33/trimmomatic-0.33.jar',
	read1 = element + '_final1.fq',
	read2 = element + '_final2.fq',
	read1out = element + '_R1_trimmed.fq', 
	read1unpairedout = element + '_R1_trimmedunpaired.fq',
	read2out = element + '_R2_trimmed.fq',
	read2unpairedout = element + '_R2_trimmedunpaired.fq',
	sampleID = element) #name your output


	commands = """
	java -classpath {trimmomatic} org.usadellab.trimmomatic.TrimmomaticPE -phred33 {read1} {read2} {read1out} {read1unpairedout} {read2out} {read2unpairedout} ILLUMINACLIP:{adfile}:2:20:3 SLIDINGWINDOW:4:20 MINLEN:40 LEADING:15 TRAILING:15
	""".format(**variables)

	cmd_list = commands.split("\n")
	for cmd in cmd_list:
		os.system(cmd)

def main():
	args = get_args() 

	#Make a list of lists, each list within the list will have the first and second elements of the map file that are separated by a tab

	with open(args.map) as rfile:
		for line in rfile:
			line = line.strip()
			align(line)


if __name__ == "__main__": #run main over multiple processors
	main()







