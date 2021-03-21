# utility functions for som processing
import numpy as np
import math
from math import sqrt

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
    
def mapBMUs(bmfile):
	bmfp = open(bmfile)
	nrow, ncol = bmfp.readline()[1:-1].split()
	nrow = int(nrow)
	ncol = int(ncol)
	nsamples = int(bmfp.readline()[1:-1])
	bmuMap = [[[] for x in range(ncol)] for y in range(nrow)]
	for line in bmfp:
		data = line[:-1].split()
		bmuMap[int(data[1]),int(data[2])].append(int(data[0]))
	return nrow, ncol, bmuMap

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

def parseWTSFile(wtsfile):
    wtsfp = open(wtsfile)
    nrow,ncol = wtsfp.readline()[1:-1].split()
    numfeatures = int(wtsfp.readline()[1:-1])
    nrow,ncol = int(nrow),int(ncol)

    map = [[np.zeros(numfeatures) for y in range(ncol)] for x in range(nrow)]
    for k in range(nrow):
        for l in range(ncol):
            map[k][l] = np.asfarray(wtsfp.readline()[:-1].split(), float)
    wtsfp.close()
    return nrow,ncol,numfeatures,map

"""
def calculateQuantizationError(lrnfile, wtsfile, bmfile):
    bnrow, bncol, bmus = parseBMFile(bmfile)
    nrow,ncol,nfeatures,map = parseWTSFile(wtsfile)
    lrnfp = open(lrnfile)
    samplenames = lrnfp.readline()[1:-1].split()
    lrnfp.readline()
    lrnfp.readline()
    lmask = lrnfp.readline()[1:-1].split()
    featnames = lrnfp.readline()[1:-1].split()
    featnames = [featnames[i] for i in range(len(featnames)) if lmask[i] == '1']
    error = 0.
    for line in lrnfp:
        data = line[:-1].split()
        index = int(data[0])
        sample = np.asfarray(data[1:], float)
        error += np.linalg.norm(map[bmu[index][0]][bmu[index][1]] - sample)
        print(error)
        if index % 100 == 0:
            print(index)
    return error
"""
def getbmu1and2(map, nrow, ncol, sample):
    bmu1 = [0,0]
    bmu2 = [0,0]
    kmin, lmin, kmin2, lmin2 = 0,0,0,0
    distmin, distmin2 = 1.e6, 1.e6

    for k in range(nrow):
        for l in range(ncol):
            dist = np.linalg.norm(map[k][l] - sample)
            if dist < distmin:
                distmin2 = distmin
                kmin2 = kmin
                lmin2 = lmin
                distmin = dist
                kmin = k
                lmin = l
    return distmin, [kmin, lmin], distmin2, [kmin2, lmin2]

def areNeighbors(x1, y1, x2, y2, nrow, ncol, topo):
    if topo == "rectangular":
        if (abs(x1 - x2) + abs(y1-y2)) > 1:
            return 0 # not neighbors
        else:
            return 1
    elif topo == "rectangular-toroid":
        if (min(abs(x1-x2), nrow - abs(x1-x2)) + min(abs(y1-y2), ncol - abs(y1-y2))) > 1:
                return 0
        else:
            return 1

    elif topo == "hexagonal":
        xdist = abs(x1-x2)
        ydist = abs(y1-y2)
        ymin = min(y1,y2)
        if (ydist & 1) :
            if (ymin & 1):
                xdist -= 0.5
            else:
                xdist += 0.5
        dist = sqrt( xdist*xdist + ydist * ydist * 0.75)
        if dist > 1.:
            return 0
        else:
            return 1
            
    elif topo == "hexagonal-toroid":
        xdist = min(abs(x1 - x2), abs(x1-x2+nrow))
        ydist = min(abs(y1-y2), abs(y1-y2+ncol))
        ymin = min(y1, y2)
        if (ydist & 1) :
            if (ymin & 1):
                xdist -= .05
            else:
                xdist += 0.5
        dist = sqrt(xdist*xdist + ydist*ydist*0.75)
        if dist > 1.:
            return 0
        else:
            return 1

def calculateErrors(lrnfile, wtsfile, topo):
    # since need to recalculate bmus anyway, don't use bmfile for this
    nrow,ncol,nfeatures,map = parseWTSFile(wtsfile)
    lrnfp = open(lrnfile)
    samplenames = lrnfp.readline()[1:-1].split()
    lrnfp.readline()
    lrnfp.readline()
    lmask = np.asfarray(lrnfp.readline()[1:-1].split(), int)
    featnames = np.array(lrnfp.readline()[1:-1].split())
    featnames = featnames[lmask==1]
    
    # account for masking
    quantizationError = 0.
    topologicalError = 0
    index = 0
    for line in lrnfp:
        sample = np.asfarray(line[:-1].split(), float)
        sample = sample[lmask==1]
        distmin, bmu1, distmin2, bmu2 = getbmu1and2(map, nrow, ncol, sample)
        quantizationError += distmin
        topologicalError += (1 - areNeighbors(bmu1[0], bmu1[1], bmu2[0], bmu2[1], nrow, ncol, topo))
        index += 1
        if index % 500 == 0:
            print("Processed "+str(index)+" out of "+str(len(samplenames))+" sample errors.")
    topologicalError /= (len(samplenames))
    quantizationError /= (len(samplenames))
    
    return quantizationError, topologicalError

