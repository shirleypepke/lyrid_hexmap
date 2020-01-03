# Take matrix input file and output in lrn format, which really means just commenting first line and adding extra header info plus coverting to tsv

import pandas as pd
import sys
import os
from os import path
import argparse

# parse option normal or transposed
parser = argparse.ArgumentParser()
parser.add_argument("--transpose", help="generate transposed data matrix for training", action="store_true")
parser.add_argument("csvfile",help = "csv file name")
args = parser.parse_args()

#infile = input("Enter a csv training matrix file: ")
if args.csvfile:
	infile = args.csvfile
else:
	parser.print_help()
	sys.exit(0)

df = pd.read_csv(infile)

nsamples = len(df.index)
nvariables = len(df.columns) - 1

samplenames = df['index'].tolist()
samplestr = ' '.join(samplenames)

filename = infile[:-4]

if args.transpose:
    if path.exists(filename+".transpose.lrn"):
        os.system('rm '+filename+'.transpose.lrn')
    varnames = ' '.join(df.columns[1:])
    samplestr = "index "+samplestr
    mask = ["1" for x in range(nsamples+1)]
    mask[0] = "9"
    maskstr = ' '.join(mask)
    with open(filename+".transpose.lrn", 'a') as outfile:
        outfile.write("#"+varnames+"\n")
        outfile.write("%"+str(nvariables)+"\n")
        outfile.write("%"+str(nsamples+1)+"\n")
        outfile.write("%"+maskstr+"\n")
        outfile.write("%"+samplestr+"\n")
        df = df.transpose()
        # now need to output all columns but not first row
        df.drop('index', inplace=True)
        df = df.reset_index(drop=True)
        df.to_csv(outfile, header=False, sep=' ')
else:
    if path.exists(filename+".lrn"):
        os.system('rm '+filename+'.lrn')
    df = df.drop(['index'],axis=1)
    varnames = "index "+' '.join(df.columns)
    mask = ["1" for x in range(nvariables+1)]
    mask[0] = "9"
    maskstr = ' '.join(mask)
    with open(filename+".lrn", 'a') as outfile:
        outfile.write("#"+samplestr+"\n")
        outfile.write("%"+str(nsamples)+"\n")
        outfile.write("%"+str(nvariables+1)+"\n")
        outfile.write("%"+maskstr+"\n")
        outfile.write("%"+varnames+"\n")
        # now need to output all columns but not first row
        df.to_csv(outfile, header=False, columns = df.columns[1:], sep=' ')




