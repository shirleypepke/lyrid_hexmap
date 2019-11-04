# Take matrix input file and output in lrn format, which really means just commenting first line and adding extra header info plus coverting to tsv

import pandas as pd
import sys

infile = input("Enter a csv training matrix file: ")

df = pd.read_csv(infile)

nsamples = len(df.index)
nvariables = len(df.columns) - 1

mask = ["1" for x in range(nvariables+1)]
mask[0] = "9"
maskstr = ' '.join(mask)
varnames = ' '.join(df.columns)
samplenames = df['index'].tolist()
samplestr = ' '.join(samplenames)
#df = df.drop(['index'],axis=1)

filename = infile[:-4]
with open(filename+".lrn", 'a') as outfile:
	outfile.write("#"+samplestr+"\n")
	outfile.write("%"+str(nsamples)+"\n")
	outfile.write("%"+str(nvariables)+"\n")
	outfile.write("%"+maskstr+"\n")
	outfile.write("%"+varnames+"\n")
	df.to_csv(outfile, header=False, columns = df.columns[1:], sep=' ')




