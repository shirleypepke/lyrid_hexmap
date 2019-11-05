# Take patient labels such as 'HC.V02' as inputs and create density file that can be processed by postsom.py
# Need to input .lrn source file as well as bmu file names
# map_patient_cats.py <lrnfile> <bmufile> <[label1, label2, etc..]> <outputfile>

import sys

if len(sys.argv) < 5:
    sys.exit("python map_patient_cats.py <lrnfile> <bmufile> <category labels, e.g.:HC.V02,HC.V04,BL> <output file>")

# grab patient labels from lrnfile
lrnfile = sys.argv[1]
bmufile = sys.argv[2]
filter_labels = sys.argv[3].split(",")
outfile = sys.argv[4]

print("Mapping patient labels: ")
print(filter_labels)

lrnfp = open(lrnfile)
patient_labels = lrnfp.readline()[1:].split()
lrnfp.close()

filter_indices = []
for item in filter_labels:
    tmp = [i for i in range(len(patient_labels)) if item in patient_labels[i]]
    filter_indices = filter_indices + tmp

# Now open bmu file and to create filtered density map and output
outfp = open(outfile,'w')
bmfp = open(bmufile)
line1 = bmfp.readline()
line2 = bmfp.readline()
outfp.write(line1)
outfp.write(line2)
for line in bmfp:
    index = int( line[:-1].split()[0])
    if index in filter_indices:
        outfp.write(line)
bmfp.close()
outfp.close()

# open outfile and calculate density
bmfile = outfile

infile = open(bmfile)
data = infile.readline()[:-1].split()
nrow = int(data[0][1:])
ncol = int(data[1])
print(nrow, ncol)

nvec = int(infile.readline()[1:-1])

mat = [[0.0 for y in range(ncol)] for x in range(nrow)]
pmat = [[0.0 for y in range(ncol)] for x in range(nrow)]
amat = [[0.0 for y in range(ncol)] for x in range(nrow)]
apmat = [[0.0 for y in range(ncol)] for x in range(nrow)]

cmax = 0
index = 0
for line in infile:
    data = line[:-1].split()
    irow = int(data[1])
    icol = int(data[2])
    mat[irow][icol] += 1
    index += 1

xmin = 100
xmax = -100

for row in mat:
    for itm in row:
        if itm > xmax:
            xmax = itm
        elif itm < xmin:
            xmin = itm
print(xmin,xmax)

outc = open(outfile+".density.csv",'w')
outc.write("nrow,ncol,intensity\n")
for i in range(nrow):
    for j in range(ncol):
        outc.write(str(i)+","+str(j)+","+str((1.*mat[i][j]-xmin)/(xmax-xmin))+"\n")
#outc.write(str(i)+","+str(j)+","+str(mat[i][j])+"\n")
outc.close()
