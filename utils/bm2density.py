import sys
from os import path
import somutils
import numpy as np
#%nrow ncol 
#%nvec
#index row col

bmfile = input("Enter a bmu filename (.bm): ")
oprefix = input("Enter output file prefix: ")
if not path.exists(bmfile):
    sys.exit("Cannot find file: "+bmfile)

nrow, ncol, bmus = somutils.parseBMFile(bmfile)
print(nrow, ncol)

nvec = len(bmus)

mat = np.array([[0.0 for y in range(ncol)] for x in range(nrow)])

for vec in bmus:
    mat[int(vec[0]), int(vec[1])] += 1

outc = open(oprefix + ".bmu.csv",'w')
outc.write("nrow,ncol,intensity\n")
for i in range(nrow):
	for j in range(ncol):
		outc.write(str(i)+","+str(j)+","+str((1.*mat[i][j]-mat.min())/(mat.max()-mat.min()))+"\n")
		#outc.write(str(i)+","+str(j)+","+str(mat[i][j])+"\n")
outc.close()

