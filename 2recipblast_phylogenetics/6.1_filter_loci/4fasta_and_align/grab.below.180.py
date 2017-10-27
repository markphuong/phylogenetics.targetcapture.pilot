myfile = open('MAP44_loci_v2.fa', 'r')


for line in myfile:
	if ">" in line:
		header = line.strip().split('|')
		seq = next(myfile).strip()		
		if len(seq) > 150 and len(seq) < 180:
			if float(header[2]) > 100:
				print header

		else:
			continue
