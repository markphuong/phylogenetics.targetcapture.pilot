#!/usr/bin/env python

import os
import sys
from collections import defaultdict


out = open(sys.argv[2], 'w')

counter = 0 

with open(sys.argv[1]) as rfile:
	for line in rfile:
		if ">" in line:
			if counter == 0:
				output = line
				counter += 1
			else:
				output = "\n" + line
			out.write(output)
		else:
			line = line.strip()
			out.write(line)

out.close()
