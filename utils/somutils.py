# utility functions for som processing

def parseBMFile(bmfile):
    bmfp = open(bmfile)
    nrow, ncol = bmfp.readline()[1:-1].split()
    nrow = int(nrow)
    ncol = int(ncol)
    nsamples = int(bmfp.readline()[1:-1])
    bmus = [None]*nsamples
    for line in bmfp:
        data = line[:-1].split()
        bmus[int(data[0])] = [int(data[1]),int(data[2])]
    bmfp.close()
    return nrow, ncol, bmus

def parseLRNHeader(lrnfile):
    lrnfp = open(lrnfile)
    samplenames = lrnfp.readline()[1:-1].split()
    lrnfp.readline()
    lrnfp.readline()
    lmask = lrnfp.readline()[1:-1].split()
    featnames = lrnfp.readline()[1:-1].split()
    featnames = [featnames[i] for i in range(len(featnames)) if lmask[i] == '1']
    lrnfp.close()
    return samplenames, featnames
