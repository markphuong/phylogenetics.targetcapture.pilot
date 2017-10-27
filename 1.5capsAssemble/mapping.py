#!/usr/bin/env python

#REQUIRES: novoalign and samtools
#REQUIRES: a map file, with first column as sample ID, and second file as which fasta it goes to. The reason you have different fastas for different samples is because of divergent mtDNA genomes
#elements in the map file are separated by a tab

#This script aligns your paired and unpaired reads to a reference using novoalign, and makes a pileup file using samtools

import os
import sys
import argparse
import multiprocessing

#this is a wrap around for novoalign and samtools where each sample identifier was "index#" where # was a number between 1 - 50

def get_args(): #arguments needed to give to this script
	parser = argparse.ArgumentParser(description="run novoalign")

	#forces required argument to let it run
	required = parser.add_argument_group("required arguments") 
	required.add_argument("--map", help="textfile with samples to run and what fasta file to match it to", required=True) #A map file with the sample ID and the fasta file it goes to

	return parser.parse_args()

def align(element):

	ID = element
	
	r1name = '_final1.fq'  #extension of front reads
	r2name = '_final2.fq' #extension of back reads
	uname = '_finalunpaired.fq'

	variables = dict(
	sample = ID,
	read1 = '/nfs/LabShared/MarkPhuong/exonCapturePilot/1spadesAssemble/' + ID + r1name,
	read2 = '/nfs/LabShared/MarkPhuong/exonCapturePilot/1spadesAssemble/' + ID + r2name,
	unpaired = '/nfs/LabShared/MarkPhuong/exonCapturePilot/1spadesAssemble/' + ID + uname,
	out_paired = ID + '_out_paired',
	out_unpaired = ID + '_out_unpaired',
	outfile = ID + '_sorted'
	) #name your output


	commands = """
	python makesomethingNotInterleaved.py {sample}_contigs.fasta {sample}_contigs.fasta.NI
	bowtie2-build {sample}_contigs.fasta.NI {sample}_contigs
	bowtie2 -x {sample}_contigs -1 {read1} -2 {read2} --local --very-sensitive-local --no-discordant -p 20 -S {out_paired}.sam > {sample}_paired.out 2> {sample}_paired.stderr
	bowtie2 -x {sample}_contigs -U {unpaired} --local --very-sensitive-local -p 20 -S {out_unpaired}.sam > {sample}_unpaired.out 2> {sample}_unpaired.stderr
	/home/analysis/bin/samtools-1.2/samtools view -bS -@ 20 {out_paired}.sam > {out_paired}.bam
	/home/analysis/bin/samtools-1.2/samtools view -bS -@ 20 {out_unpaired}.sam > {out_unpaired}.bam
	/home/analysis/bin/samtools-1.2/samtools merge -f {sample}.raw.bam {out_paired}.bam {out_unpaired}.bam
	/home/analysis/bin/samtools-1.2/samtools sort -@ 20 {sample}.raw.bam {outfile}
	/home/analysis/bin/samtools-1.2/samtools index {outfile}.bam
	java -jar /home/analysis/Downloads/picard-tools-1.138/picard.jar MarkDuplicates I={sample}_sorted.bam O={sample}_md.bam REMOVE_DUPLICATES=FALSE ASSUME_SORTED=TRUE METRICS_FILE={sample}_md.metrics
	/home/analysis/bin/samtools-1.2/samtools mpileup -d 1000000 -u -I -D -S -B -f {sample}_contigs.fasta.NI {sample}_md.bam | /home/analysis/bin/bcftools-1.2/bcftools call -c - > {sample}.vcf
	""".format(**variables)

	cmd_list = commands.split("\n")
	for cmd in cmd_list:
		os.system(cmd)
mylist = []
def main():
	args = get_args() 

	#Make a list of lists, each list within the list will have the first and second elements of the map file that are separated by a tab

	with open(args.map) as rfile:
		for line in rfile:
			line = line.strip()
			align(line)
#			mylist.append(line.split("\t"))

#	pool = multiprocessing.Pool()
#	pool.map(align, mylist)#run the function with the arguments

if __name__ == "__main__": #run main over multiple processors
	main()







