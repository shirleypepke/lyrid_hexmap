import sys 

umxfile = input("Enter a umx filename (.umx): ")
infile = open(umxfile)
outfile = open("ppmi.umx.csv",'w')
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
infile = file("ppmi.umx")
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
