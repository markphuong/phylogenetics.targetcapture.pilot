counter = 0

with open('conus_phylogenetic_targets_sliced.fa', 'r') as rfile:
	for line in rfile:
		if ">" in line:
			continue
		else:
			counter += len(line.strip())

print counter

counter = 0

with open('conus_phylogenetic_targets.fa', 'r') as rfile:
	for line in rfile:
		if ">" in line:
			continue
		else:
			counter += len(line.strip())

print counter