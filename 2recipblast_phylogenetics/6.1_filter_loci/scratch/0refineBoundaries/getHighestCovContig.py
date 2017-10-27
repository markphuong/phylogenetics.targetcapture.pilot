import os
import sys
from collections import defaultdict
from Bio.Seq import translate
from Bio.Seq import reverse_complement
from Bio import SearchIO


def checkOverlap(thelists):

	overlap = 'no'
	for value1 in thelists:
		for value2 in thelists:
			if value1 == value2:
				continue
			else:
				if len(list(set(range(value1.query_range[0], value1.query_range[1] + 1)) & set(range(value2.query_range[0], value2.query_range[1] + 1)))) > 0:
					overlap = 'yes'

#	print overlap
	return overlap

################################# check the number of bases covered by the blastg coorindates for a particular locus


# you give it the blastdict, the key for a particular contig, and then the conus sequence..
def checkRange(key, mydict,conus):

	total = 0 #you add to this the range of each set of blast coordinates
	for thing in mydict[key]:
		total += len(range(thing[1], thing[2]+1))
		
	return total/float(len(conus))



######################################## initialize your original reference so you can obtain length and sequence information

myconus = open('conus_phylogenetic_targets_sliced.fa', 'r') 

conusdict = dict()

for line in myconus:
	if ">" in line:	
		conusdict[line.strip()[1:]] = next(myconus).strip()

################### slice these

slicethese = open('need_slicing', 'r')

slicelist = []

for line in slicethese:
	if '#' in line:
		continue
	else:
		if len(line)> 5:
			mynum = int(next(slicethese).strip())
			if mynum > 4:
				slicelist.append(line.strip())


######################################### open sorted blast files and find sample with longest contig for reference building
	
myfiles = [f for f in os.listdir('.') if os.path.isfile(f)]

keepdict = dict()

fastadict = defaultdict(dict)



for thing in myfiles:
	if 'filtered_recipblast.sorted' in thing:

################# load fasta info as fastadict, then the ID of the species, then the sequence name. This is so you can generate a 'genomic' sequence to give to exonerate later when you've chosen the species you want to use as the reference for a particular locus

		ID = thing.split('_')[0]

		myfasta = open(ID + '_phylo_contigs.fasta', 'r')

		for line in myfasta:
			if ">" in line:
				fastadict[ID][line.strip()[1:]] = next(myfasta).strip()


################ parse blast file for a particular species and put all the information you want into 'myblast'
		blastdict = defaultdict(list)

		myblast = open(thing, 'r')

		for line in myblast:
			info = line.strip().split('\t')

			if info[0] in slicelist:
				if info[0] in blastdict.keys():
					blastdict[info[0]].append([info[1], int(info[6]), int(info[7]), int(info[8]), int(info[9]), int(info[4])]) #the information you want is the contig name in the species, query start/end, db start/end, and the number of mismatches
				else:
					blastdict[info[0]] = [[info[1], int(info[6]), int(info[7]), int(info[8]), int(info[9]), int(info[4])]]		

		for key in blastdict:

			coverage = checkRange(key,blastdict,conusdict[key]) #returns the number of bases totaled from the blast coorindates


# if the target is already in keepdict, only replace it if the coverage is higher. Else, add it to keepdict.
			

######### modified here to only consider targets that had multiple hits in order to pick one to slice them
			if len(blastdict[key]) == 1:
				continue
			elif key in keepdict:	
				if coverage > keepdict[key][0]:
					keepdict[key] = [coverage, ID, blastdict[key]] # keepdict contains the %coverage of the target, the locus ID, and all the blast info
				else:
					continue
			else:
				keepdict[key] = [coverage, ID, blastdict[key]]
		


####################################################### now only deal with the 'best' reference per target #######
print keepdict

out3 = open('mynewbed', 'w') #new file with coordinates about how to cut up the reference, and what the exonerate output was like 




###### keepdict contains the %coverage of the target, the locus ID, and all the blast info
for key in keepdict:

###### only do this if there was more than ONE blast hit per target

	if len(keepdict[key][2]) > 1:
		fullseq = '' ### initializes genomc sequence
		alreadyhave = [] ### do not repeat 
		previous = ''

		ID = keepdict[key][1]

###### this is so you can get the minimum start and max end so that you can figure out the entire range that the blast coordinates encompass

		mymin = 100000000000000000000000 
	
		mymax = 0


######################## generate the 'genomic' sequence so that you can delimit exon/intron boundaries and 


		for thing in keepdict[key][2]:

			mymin = min(mymin, thing[1])
			mymax = max(mymax, thing[2])
			if thing[3] > thing[4]:
				seq = reverse_complement(fastadict[ID][thing[0]])
			else:
				seq = fastadict[ID][thing[0]]

			if thing[0] in alreadyhave and thing[0] != previous:
				previous = thing[0]
				print key
				print keepdict[key]
			elif thing[0] in alreadyhave:
				previous = thing[0]
				continue
			else:
				previous = thing[0]
				alreadyhave.append(thing[0])
				fullseq = fullseq + 'NNNNNNNNN' + seq


############################### write exonerate stuff and load the exonerate file

		out = open('mynewdata', 'w')
		out.write('>newdata'+ '\n')
		out.write(fullseq + '\n')

		out.close()

		out2 = open('myconus.fa', 'w')
		out2.write('>cDNA_'+key + '\n')
		out2.write(conusdict[key]+ '\n')
		out2.close()

		cmd = 'exonerate --model est2genome myconus.fa mynewdata > exoneratefile'
		os.system(cmd)
        	all_qresult = list(SearchIO.parse('exoneratefile', 'exonerate-text'))

##################### here, you make decisions about exonerate output i.e., manual changes

		hsp = all_qresult[0][0][0] #this allows you to access the first hit fragment info

		if key == 'index7_185711|noex|first_design|no_exon_boundaries':
			for i in range(0,len(all_qresult[0][0])):
				hsp = all_qresult[0][0][i]
					
				for k in range(0,len(hsp)):
					start = hsp[k].query_start
					end = hsp[k].query_end

					if end == 696:
						end = 693
					out3.write(key + '\t' + str(start) + '\t' + str(end) + '\t' + ID + '\t' + 'manual' + '\n')
		
		elif key == 'lividus_210692|noex|first_design|no_exon_boundaries':
			for i in range(0,len(all_qresult[0][0])):
				hsp = all_qresult[0][0][i]
					
				for k in range(0,len(hsp)):
					start = hsp[k].query_start
					end = hsp[k].query_end

					if 1000 in range(start,end):
						continue
					else:
						out3.write(key + '\t' + str(start) + '\t' + str(end) + '\t' + ID + '\t' + 'manual' + '\n')			

		elif key == 'index9_222542|noex|first_design|no_exon_boundaries':
			for i in range(0,len(all_qresult[0][0])-1):
				hsp = all_qresult[0][0][i]
					
				for k in range(0,len(hsp)):
					start = hsp[k].query_start
					end = hsp[k].query_end

					out3.write(key + '\t' + str(start) + '\t' + str(end) + '\t' + ID + '\t' + 'manual' + '\n')			

		elif key == 'rattus_114038_73|noex|first_design|no_exon_boundaries':
			for i in range(0,len(all_qresult[0][0])-1):
				hsp = all_qresult[0][0][i]
					
				for k in range(0,len(hsp)):
					start = hsp[k].query_start
					end = hsp[k].query_end

					out3.write(key + '\t' + str(start) + '\t' + str(end) + '\t' + ID + '\t' + 'manual' + '\n')			

		elif key == 'rattus_136673_20|noex|first_design|no_exon_boundaries':
			for i in range(0,len(all_qresult[0][0])-1):
				hsp = all_qresult[0][0][i]
					
				for k in range(0,len(hsp)):
					start = hsp[k].query_start
					end = hsp[k].query_end

					out3.write(key + '\t' + str(start) + '\t' + str(end) + '\t' + ID + '\t' + 'manual' + '\n')			


##################### if there are more than two alignable bits, do the following:
######### if the length of the target matches the length of the exonerate span, just use the first hit (HSP)
########## IF all the HSPs do NOT overlap, just write them all out
######### if they are overlapping, but the first HSP encapsulates > 98% of the blast output, then write out the first HSP
######## else, print everything out

		elif len(all_qresult[0][0]) > 2:


			if len(conusdict[key]) == all_qresult[0][0][0].query_span:
				for i in range(0,len(hsp)):
					start = hsp[i].query_start
					end = hsp[i].query_end
					out3.write(key + '\t' + str(start) + '\t' + str(end) + '\t' + ID + '\t' + 'more_than_2_frags_but_full_length' +'\n')

			elif checkOverlap(all_qresult[0][0]) == 'no':
				for i in range(0,len(all_qresult[0][0])):
					hsp = all_qresult[0][0][i]
					
					for k in range(0,len(hsp)):
						start = hsp[k].query_start
						end = hsp[k].query_end
						out3.write(key + '\t' + str(start) + '\t' + str(end) + '\t' + ID + '\t' + 'more_than_2_frags_fragmented_exonerate' + '\n')

			elif all_qresult[0][0][0].query_span/float(mymax-mymin+1) > 0.98:
				for i in range(0,len(hsp)):
					start = hsp[i].query_start
					end = hsp[i].query_end
					out3.write(key + '\t' + str(start) + '\t' + str(end) + '\t' + ID + '\t' + 'more_than_2_frags_but_almost_full_length' + '\n')

			else:
				print all_qresult[0][0]
				print keepdict[key]
				print all_qresult[0][0][0].query_span


###################### if the first fragment is equal to the length of the target, just write it out

		elif len(conusdict[key]) == all_qresult[0][0][0].query_span:

			for i in range(0,len(hsp)):
				start = hsp[i].query_start
				end = hsp[i].query_end
				out3.write(key + '\t' + str(start) + '\t' + str(end) + '\t' + ID + '\t' + 'full_length_less_than_2_frags' + '\n')

############### if there is just one fragment, write it out

		elif len(all_qresult[0][0]) == 1: 
			for i in range(0,len(hsp)):
				start = hsp[i].query_start
				end = hsp[i].query_end
				out3.write(key + '\t' + str(start) + '\t' + str(end) + '\t' + ID + '\t' + '1_Frag_not_full_length' +'\n')

############ if the two fragments do not overlap, just write them out
		elif checkOverlap(all_qresult[0][0]) == 'no':
			for i in range(0,len(all_qresult[0][0])):
				hsp = all_qresult[0][0][i]
				
				for k in range(0,len(hsp)):
					start = hsp[k].query_start
					end = hsp[k].query_end
					out3.write(key + '\t' + str(start) + '\t' + str(end) + '\t' + ID + '\t' + '2_frags_fragmented_exonerate' + '\n')

######## if they DO overlap, write out the longest one.
		elif all_qresult[0][0][0].query_span > all_qresult[0][0][1].query_span and all_qresult[0][0][0].query_span/float(mymax-mymin+1) > 0.98:
			hsp = all_qresult[0][0][0]
			for i in range(0,len(hsp)):
				start = hsp[i].query_start
				end = hsp[i].query_end
				out3.write(key + '\t' + str(start) + '\t' + str(end) + '\t' + ID  + '\t' + 'overlapping_2_frags_kept_longer' + '\n')

		elif all_qresult[0][0][1].query_span > all_qresult[0][0][0].query_span and all_qresult[0][0][1].query_span/float(mymax-mymin+1) > 0.98:
			hsp = all_qresult[0][0][1]
			for i in range(0,len(hsp)):
				start = hsp[i].query_start
				end = hsp[i].query_end
				out3.write(key + '\t' + str(start) + '\t' + str(end) + '\t' + ID + '\t' + 'overlapping_2_frags_kept_longer' + '\n')
		else:
			print 'fuck'
			print all_qresult[0][0]
			print keepdict[key]
			print all_qresult[0][0][0].query_span

	else:
		continue











































