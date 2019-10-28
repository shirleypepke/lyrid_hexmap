import sys
#%nrow ncol 
#%nvec
#index row col

bmfile = input("Enter a bmu filename (.bm): ")

infile = open(bmfile)
data = infile.readline()[:-1].split()
nrow = int(data[0][1:])
ncol = int(data[1])
print nrow, ncol

nvec = int(infile.readline()[1:-1])

mat = [[0.0 for y in range(ncol)] for x in range(nrow)]
pmat = [[0.0 for y in range(ncol)] for x in range(nrow)]
amat = [[0.0 for y in range(ncol)] for x in range(nrow)]
apmat = [[0.0 for y in range(ncol)] for x in range(nrow)]
hcend = 354 

cmax = 0
index = 0
for line in infile:
	data = line[:-1].split()
	irow = int(data[1])
	icol = int(data[2])
	if index < hcend:
		mat[irow][icol] += 1
	else:
		pmat[irow][icol] += 1
		apmat[irow][icol] = pmat[irow][icol]
	index += 1

# average
for row in range(1,nrow-2,1):
	for col in (1,ncol-2,1):
		print row,col
		apmat[row][col] = pmat[row][col]+pmat[row-1][col]+pmat[row+1][col]+pmat[row][col-1]+pmat[row][col+1]
		apmat[row][col] /= 5.		

#scale between zero and one
xmin = 100 
xmax = -100 

for row in mat:
	for itm in row:
		if itm > xmax:
			xmax = itm
		elif itm < xmin:
			xmin = itm
print(xmin,xmax)
				
outc = open("hcbm.csv",'w')
outc.write("nrow,ncol,intensity\n")
for i in range(nrow):
	for j in range(ncol):
		outc.write(str(i)+","+str(j)+","+str((1.*mat[i][j]-xmin)/(xmax-xmin))+"\n")
outc.close()

#scale between zero and one
xmin = 100 
xmax = -100 

for row in apmat:
	for itm in row:
		if itm > xmax:
			xmax = itm
		elif itm < xmin:
			xmin = itm
				
outc = open("pdbmu.csv",'w')
outc.write("nrow,ncol,intensity\n")
for i in range(nrow):
	for j in range(ncol):
		outc.write(str(i)+","+str(j)+","+str((1.*pmat[i][j]-xmin)/(xmax-xmin))+"\n")
outc.close()
