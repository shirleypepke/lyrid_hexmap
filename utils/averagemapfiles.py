import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("input_file", help = "File containing list of map files to average (one per line)")
parser.add_argument("output_file")
args = parser.parse_args()

fptr = open(args.input_file)
firstfile = fptr.readline()[:-1]
df = pd.read_csv(firstfile, index_col=None)
ndf = 1
for line in fptr:
	dftmp = pd.read_csv(line[:-1],index_col=None)
	df = df + dftmp
	ndf += 1
	
df = df / ndf
df.to_csv(args.output_file,index_col=False)
