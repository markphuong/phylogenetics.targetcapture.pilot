import os
import sys

thedir = [f for f in os.listdir('.') if os.path.isfile(f)]

myaba = open('ABA_loci_list', 'r')

abalist = []

for line in myaba:
	abalist.append('LotgiP'+line.strip())



for thing in thedir:
	if '_analyze' in thing and thing.split('_')[0] in abalist:
		os.system('cp ' + thing + ' test/')
