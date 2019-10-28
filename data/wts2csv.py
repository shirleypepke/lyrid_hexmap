import sys

wtsfile = input("Enter a weights file (.wts): ")

infile = open(wtsfile);
[nrow, ncol] = infile.readline()[1:-1].split()
nrow = int(nrow)
ncol = int(ncol)

nfeats = int(infile.readline()[1:-1])

components = [[] for x in range(nfeats)]

for line in infile:
	data = line[:-1].split()
	for fi in range(nfeats):
		components[fi].append(data[fi])
infile.close()

for fi in range(nfeats):
	outfile = open("ppmi.comp"+str(fi)+".csv",'w')
	outfile.write("nrow,ncol,intensity\n")
	index = 0
	for ir in range(nrow):
		for ic in range(ncol):
			outfile.write(str(ir)+","+str(ic)+","+components[fi][index]+"\n")
			index += 1
	outfile.close()
