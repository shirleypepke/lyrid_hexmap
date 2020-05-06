# this file reads list of input SOM map indices ands outputs corresponding variable listing (from bmfile and lrnfile)
# not DONE!!!!!!

import sys
import argparse
import pandas as pd
import somutils

parser = argparse.ArgumentParser()
parser.add_argument("bmufile", help = "BMU file from SOMOCLU")
parser.add_argument("lrnfile", help = "Lrn file for given bmufile")
parser.add_argument("output_file")
args = parser.parse_args()

samplenames, featnames = somutils.parseLRNHeader(args.lrnfile)
print(len(samplenames))

nrows, ncols, bmus = somutils.parseBMFile(args.bmufile)
#invert bmu listing
map = [[[] for x in range(ncols)] for y in range(nrows)]
index = 0
for itm in bmus:
	map[itm[0]][itm[1]].append(samplenames[index])
	index += 1

optr = open(args.output_file,'w')
for i in range(nrows):
	for j in range(ncols):
		optr.write(str(i)+","+str(j))
		for itm in map[i][j]:
			optr.write(","+itm)
		optr.write("\n")

optr.close()

