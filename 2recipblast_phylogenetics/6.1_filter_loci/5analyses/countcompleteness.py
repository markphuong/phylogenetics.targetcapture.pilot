myfasta = open("conus_phylogeny_headed.nexus" , 'r')

for line in myfasta:
	if "#" in line or "begin" in line or ';' in line or 'ntax' in line or 'matrix' in line:
		continue

	else:
		myseq = line.strip()
		mylength = 573854 - myseq.count('-') - myseq.count('?')
		print myseq.count('-')
		print myseq.count('?')
		mylength = float(mylength)
		print line[:13]
		print mylength/573854
