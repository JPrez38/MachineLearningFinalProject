#!/usr/bin/env python2.7.4

import sys,math,cmath,operator,time,csv
from copy import deepcopy

t0 = time.time()

if len(sys.argv) != 3: #check args
	print "Usage: append.py [file to append onto] [file to append] > [completeFile]"
	sys.exit()

readerOnto = csv.reader(open(sys.argv[1], 'rb'), quoting=csv.QUOTE_NONE)
readerFrom = csv.reader(open(sys.argv[2], 'rb'), quoting=csv.QUOTE_NONE)

ontoLookup = {}

for index,line in enumerate(readerOnto):
	key = (line[0],line[1])
	val = [line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7],line[8],line[9],line[10],line[11],line[12],line[13],line[14]]
	ontoLookup[key] = val

numAdded = 0
for ind,point in enumerate(readerFrom):
	if (point[0],point[1]) in ontoLookup and ontoLookup[(point[0],point[1])][14] == 'x':
		numAdded += 1
		ontoLookup[(point[0],point[1])][14] = point[2]

for key in ontoLookup:
	item = ontoLookup[key]
	print item[0] + "," + item[1] + "," + item[2] + "," + item[3] + "," + item[4] + "," + item[5] + "," + item[6] + "," + item[7] + "," + item[8] + "," + item[9] + "," + item[10] + "," + item[11] + "," + item[12] + "," + item[13] + "," + item[14]
