#!/usr/bin/env python


import os
import sys
import argparse
import multiprocessing


def get_args(): 
	parser = argparse.ArgumentParser(description="run novoalign")

	#forces required argument to let it run
	required = parser.add_argument_group("required arguments") 
	required.add_argument("--map", help="textfile with samples to run and what fasta file to match it to", required=True) 

	return parser.parse_args()

def align(element):

	ID = element
	
	r1name = '_final1.fq'  #extension of front reads
	r2name = '_final2.fq' #extension of back reads
	uname = '_finalunpaired.fq' #extension of unpaired reads

# some names for input output files

	variables = dict(
	sample = ID,
	ref = ID + '_assemblies_clustered.fasta', 
	read1 = '/nfs/LabShared/MarkPhuong/exonCapturePilot/1spadesAssemble/' + ID + r1name,
	read2 = '/nfs/LabShared/MarkPhuong/exonCapturePilot/1spadesAssemble/' + ID + r2name,
	unpaired = '/nfs/LabShared/MarkPhuong/exonCapturePilot/1spadesAssemble/' + ID + uname,
	out_paired = ID + '_out_paired',
	out_unpaired = ID + '_out_unpaired',
	outfile = ID + '_sorted'
	) #name your output

# 1. make a bowtie2 index for your contigs
# 2. align the paired reads
# 3. align the unpaired reads
# 4. make a bam file of the paired reads
# 5. make a bam file of the unpaired reads
# 6. merge the bam files
# 7. sort the bam file
# 8. index the bam file
# 9. mark duplicates
# 10. create a VCF file

#	python makesomethingNotInterleaved.py {ref} {ref}.NI
#	bowtie2-build {ref}.NI {sample}
#	bowtie2 -x {sample} -1 {read1} -2 {read2} --local --very-sensitive-local --no-discordant -p 15 -S {out_paired}.sam > {sample}_paired.out 2> {sample}_paired.stderr
#	bowtie2 -x {sample} -U {unpaired} --local --very-sensitive-local -p 15 -S {out_unpaired}.sam > {sample}_unpaired.out 2> {sample}_unpaired.stderr
#	samtools view -bS -@ 15 {out_paired}.sam > {out_paired}.bam
#	samtools view -bS -@ 15 {out_unpaired}.sam > {out_unpaired}.bam
#	samtools merge -f {sample}.raw.bam {out_paired}.bam {out_unpaired}.bam
#	samtools sort -@ 15 -o {outfile}.bam -O bam {sample}.raw.bam 
#	samtools index {outfile}.bam

	commands = """
	java -jar /nfs/LabShared/MarkPhuong/myprograms/bin/picard.jar MarkDuplicates INPUT={sample}_sorted.bam OUTPUT={sample}_md.bam REMOVE_DUPLICATES=TRUE ASSUME_SORTED=TRUE METRICS_FILE={sample}_md.metrics
	samtools mpileup -d 1000000 -u -I -t DP -t SP -B -f {ref}.NI {sample}_md.bam | bcftools call -c - > {sample}.vcf
	samtools index {sample}_md.bam
	rm {out_paired}.sam {out_paired}.bam {out_unpaired}.sam {out_unpaired}.bam {sample}.raw.bam
	""".format(**variables)

	cmd_list = commands.split("\n")
	for cmd in cmd_list:
		os.system(cmd)
mylist = []
def main():
	args = get_args() 



	with open(args.map) as rfile:
		for line in rfile:
			line = line.strip()
			align(line)


#	pool = multiprocessing.Pool()
#	pool.map(align, mylist)#run the function with the arguments

if __name__ == "__main__": #run main over multiple processors
	main()







