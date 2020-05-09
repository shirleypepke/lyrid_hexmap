##############################################################
## The following script retrieves and prints out
## significantly enriched (FDR < 1%) GO Processes
## for the given set of proteins.
##
## Requires requests module:
## type "python -m pip install requests" in command line (win)
## or terminal (mac/linux) to install the module
##############################################################

import sys
import argparse
import pandas as pd
import somutils


parser = argparse.ArgumentParser()
parser.add_argument("bmufile", help = "BMU file from SOMOCLU")
parser.add_argument("lrnfile", help = "Lrn file for given bmufile")
parser.add_argument("output_file")
parser.add_argument("-query_stringdb", action="store_false")
parser.add_argument("-string_output", default = 'stringdb.out', help="Filename for output of stringdb enrichments")
parser.add_argument("-sdb_thresh", default = .01, help="optional enrichment threshold for stringdb")
args = parser.parse_args()

sdb_thresh = .01
if args.sdb_thresh:
	sdb_thresh = args.sdb_thresh

stringout = "stringdb.out"
if args.string_output:
	stringout = args.string_output

import requests ## python -m pip install requests
import json

string_api_url = "https://string-db.org/api"
output_format = "json"
method = "enrichment"


##
## Construct the request
##

request_url = "/".join([string_api_url, output_format, method])

##
## Call STRING
##\

def get_string_data(i,j,params,optr1):

	response = requests.post(request_url, data=params)

	##
	## Read and parse the results
	##

	data = json.loads(response.text)

	if not 'Error' in data:
		for row in data:

			term = row["term"]
			preferred_names = ",".join(row["preferredNames"])
			fdr = float(row["fdr"])
			description = row["description"]
			category = row["category"]

			#if category == "Process" and fdr < sdb_thresh:
			if (category == "Function" or category == "Process") and fdr < sdb_thresh:

				## print significant GO Process annotations
				print("\t".join([term, preferred_names, str(fdr), description]))
				optr1.write(str(i)+","+str(j)+",")
				optr1.write("\t".join([term, preferred_names, str(fdr), description]))
				optr1.write("\n")




samplenames, featnames = somutils.parseLRNHeader(args.lrnfile)
print(len(samplenames))

nrows, ncols, bmus = somutils.parseBMFile(args.bmufile)
#invert bmu listing
map = [[[] for x in range(ncols)] for y in range(nrows)]
index = 0
for itm in bmus:
	if 'ENSG' in samplenames[index]:
		samplenames[index] = samplenames[index][:15]
	map[itm[0]][itm[1]].append(samplenames[index])
	index += 1

optr = open(args.output_file,'w')
optr1 = open(stringout,'w')
for i in range(nrows):
	for j in range(ncols):
		if len(map[i][j])>0 and args.query_stringdb == True:
			params = {

				"identifiers" : "%0d".join(map[i][j]), # your protein
				"species" : 9606, # species NCBI identifier
				"caller_identity" : "www.awesome_app.org" # your app name

			}
			get_string_data(i,j,params,optr1)
		optr.write(str(i)+","+str(j))
		for itm in map[i][j]:
			optr.write(","+itm)
		optr.write("\n")

optr.close()
optr1.close()



