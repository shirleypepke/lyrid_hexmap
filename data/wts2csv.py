import sys
import mygene
from os import path

GENES = True
TRANSCRIPTS = False

prefix = input("Enter a weights (.wts) file prefix: ")
wtsfile = prefix + ".som.wts"

infile = open(wtsfile);
[nrow, ncol] = infile.readline()[1:-1].split()
nrow = int(nrow)
ncol = int(ncol)

def convert_symbols(prefix):
    lrnfp = open(prefix+".lrn")
    for i in range(5):
        data = lrnfp.readline()
    featids = data[:-1].split()[1:]
    featids = [elem[:15] for elem in featids]
    lrnfp.close()

    mg = mygene.MyGeneInfo()
    if (GENES):
        stag = 'ensembl.gene'
    elif (TRANSCRIPTS):
        stag = 'ensembl.transcript'
    out = mg.querymany(featids, scopes=stag, fields = 'symbol',species='human')
    if len(out) == len(featids):
        outfile = open(prefix+".symbols",'w')
        for i in range(len(out)):
            if 'symbol' in out[i]:
                outfile.write(out[i]['symbol']+" ")
            else:
                outfile.write(out[i]['query']+" ")
        outfile.write("\n")
        outfile.close()
    else:
        sys.exit("Too many gene symbols returned")

# convert ensembl ids to symbols using mygene file
# check if symbols file exists, if so read in symbols, otherwise query
if not path.exists(prefix+".symbols"):
    convert_symbols(prefix+".lrn")
symfp = open(prefix+".symbols")
feat_names = symfp.readline()[:-1].split()
symfp.close()

nfeats = int(infile.readline()[1:-1])
if not nfeats == len(feat_names):
    sys.exit("Number of features and feature names not equal!")


components = [[] for x in range(nfeats)]

for line in infile:
	data = line[:-1].split()
	for fi in range(nfeats):
		components[fi].append(data[fi])
infile.close()

for fi in range(nfeats):
	outfile = open(feat_names[fi]+".csv",'w')
	outfile.write("nrow,ncol,intensity\n")
	index = 0
	for ir in range(nrow):
		for ic in range(ncol):
			outfile.write(str(ir)+","+str(ic)+","+components[fi][index]+"\n")
			index += 1
	outfile.close()
