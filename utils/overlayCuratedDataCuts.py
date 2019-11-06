# Requires a bm file, a lrn file and the Curated Data Cuts csv

import sys
from os import path
import numpy as np
import pandas as pd
import somutils

# this should really be arbitrary dataframe
if not path.exists("CurDatCuts_cc.csv"):
	sys.exit("Cannot locate required file 'CurDatCuts_cc.csv'")

if len(sys.argv) < 5:
	sys.exit("usage: python overlayCuratedDataCuts.py <bmfile> <lrnfile> <var1,var2,var3..> <outfile prefix>")

bmfile = sys.argv[1]
lrnfile = sys.argv[2]
vars = sys.argv[3].split(",")
oprefix = sys.argv[4]

if not path.exists(bmfile):
	sys.exit("File not found: "+bmfile)
if not path.exists(lrnfile):
	sys.exit("File not found: " + lrnfile)

# Need to map curated data values to corresponding bmus according to patient ids by using patid and timepoint. 

# First use bm and lrn files to create dict mapping patient ids from dataframe to cell coordinates, cutting out category labels

patientids, featnames = somutils.parseLRNHeader(lrnfile)
# below converts ids to same form as in Curated Data Cuts file
patientids = [ elem.split(".")[0] + "." + elem.split(".")[2] for elem in patientids]

nrow,ncol,bmus = somutils.parseBMFile(bmfile)

if not len(patientids) == len(bmus):
    sys.exit("Number of bmus not equal to number of samples!")

bmudict = {}
for index in range(len(patientids)):
    bmudict[patientids[index]] = bmus[index]

# read in CurDatCuts
df = pd.read_csv("CurDatCuts_cc.csv",index_col=0)

# Iterate and output maps for given vars, ignore missing values
# Note patients may not be in CurDatCuts
map = np.array([[0. for x in range(ncol)] for y in range(nrow)])
for var in vars:
    if not var in df.columns:
        print(var+" not found in CurDatCuts_cc.csv")
        continue
    else:
        for id in bmudict:
            if id in df.index:
                if np.isnan(df.loc[id,var]) :
                    continue
                else:
                    map[bmudict[id][0], bmudict[id][1]] += float(df.loc[id, var])
        #print(map[bmudict[id][0], bmudict[id][1]])

# normalize values and output
        map = (map - map.min())/(map.max()-map.min())
        outfp = open(oprefix+"."+var+".csv",'w')
        outfp.write("nrow,ncol,intensity\n")
        for ir in range(nrow):
            for ic in range(ncol):
                outfp.write(str(ir)+","+str(ic)+","+str(map[ir,ic])+"\n")
        outfp.close()



