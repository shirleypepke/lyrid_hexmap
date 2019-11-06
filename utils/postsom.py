import sys
import mygene
from os import path
import numpy as np
import somutils

GENES = True
TRANSCRIPTS = False

def convert_symbols(prefix):
    sampleids, featids = somutils.parseLRNFile(prefix+".lrn")
    featids = [elem[:15] for elem in featids]

    mg = mygene.MyGeneInfo()
    if (GENES):
        stag = 'ensembl.gene'
    elif (TRANSCRIPTS):
        stag = 'ensembl.transcript'
    else:
        print('Using default mapping for genes, but no type specified')
        stag = 'ensembl.gene'
    out = mg.querymany(featids, scopes=stag, fields = 'symbol',species='human')
    if len(out) == len(featids):
        outfile = open(outdir+prefix+".symbols",'w')
        for i in range(len(out)):
            if 'symbol' in out[i]:
                outfile.write(out[i]['symbol']+" ")
            else:
                outfile.write(out[i]['query']+" ")
        outfile.write("\n")
        outfile.close()
    else:
        sys.exit("Too many gene symbols returned")

def process_weightsfile(infile):
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
        print(feat_names[fi])
        outfile = open(outdir+feat_names[fi]+".csv",'w')
        outfile.write("nrow,ncol,intensity\n")
        index = 0
        for ir in range(nrow):
            for ic in range(ncol):
                outfile.write(str(ir)+","+str(ic)+","+components[fi][index]+"\n")
                index += 1
        outfile.close()

# Allow for separate input and output prefixes --> "Enter a som output prefix" -- empty will be interpreted as same
prefix = input("Enter a .lrn file prefix: ")
postfix = input("Enter a .wts file prefix (<return> for same): ")
if len(postfix)==0:
    postfix = prefix
outdir = "./maps/"
wtsfile = postfix + ".wts"

if path.exists(wtsfile):
    infile = open(wtsfile);
    [nrow, ncol] = infile.readline()[1:-1].split()
    nrow = int(nrow)
    ncol = int(ncol)
    process_weightsfile(infile)
else:
    print(wtsfile+" not found.")


# process umx file
def process_umxfile(infile, umxfile):
    outfile = open(outdir+umxfile+".csv",'w')
    outfile.write("nrow,ncol,intensity\n")

    header = infile.readline()[:-1].split();
    nrows = int(header[0][1:])
    ncols = int(header[1])
    print(nrows)
    print(ncols)

    data = infile.read().split()
    data = [float(i) for i in data]
    umax = max(data)
    infile.close()
    infile = open(umxfile)
    infile.readline()

    rowind = 0
    colind = 0
    for line in infile:
        data = line[:-1].split()
        for itm in data:
            outfile.write(str(rowind)+","+str(colind)+","+str(float(itm)/umax)+"\n")
            colind += 1
        colind = 0
        rowind += 1
    infile.close()
    outfile.close()


umxfile = postfix + ".umx"
if path.exists(umxfile):
    infile = open(umxfile)
    process_umxfile(infile, umxfile)
else:
    print(umxfile+ " not found.")


# process bmu file

#%nrow ncol 
#%nvec
#index row col
def process_bmfile(infile):
    nrow, ncol, bmus = somutils.parseBMFile(bmfile)
    nvec = len(bmus)

    mat = np.array([[0.0 for y in range(ncol)] for x in range(nrow)])
    
    for i in range(nvec):
        mat[int(bmus[i][0]),int(bmus[i][1])] += 1

    #scale between zero and one

    outc = open(outdir+"mapbm.csv",'w')
    outc.write("nrow,ncol,intensity\n")
    for i in range(nrow):
        for j in range(ncol):
            outc.write(str(i)+","+str(j)+","+str((1.*mat[i][j]-mat.max())/(mat.max()-mat.min()))+"\n")
    outc.close()


bmfile = postfix + ".bm"
if path.exists(bmfile):
    process_bmfile(bmfile)
else:
    print(bmfile+" not found.")



