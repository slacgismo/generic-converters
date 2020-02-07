import json
import os
import glob
import sys, getopt

jsonfile = glob.glob('./uploads/*.json')
filename_json = jsonfile[0]
filename_txt = filename_json.replace("json", "txt")


with open(filename_json,"r") as f :
	data = json.load(f)
	assert(data['application']=='gridlabd')
	assert(data['version'] >= '4.2.0')

with open(filename_txt, "w") as f :
	f.write("ERROR: json to txt conversion not implemented yet")
