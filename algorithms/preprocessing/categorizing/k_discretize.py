#!/usr/bin/env python2.7

# k_cluster.py
# Takes 2 arguments, number of final classifications (k), and input file for training
# Steps:
#	1) Normalize all feature values (including birth-rates)
#	2) Find minimum and maximum birth-rate (now normalized)
#	3) Descretize birth-rates according to "k" input in script args
#		-> groupSize = (MAX-MIN)/k
#		-> Create k groups of size groupSize
#	4) Loops back through datapoints and assigns 1 of k buckets to each point based on normalized birth-rates


import sys,math,operator,time,csv
from copy import deepcopy

startTime = time.time()

dic = {}

if len(sys.argv) != 3:
	print "Usage: k_discretize.py [k_value (positive, real-valued integer)] [input file] > [export file]"
	sys.exit()


def read_data(raw_file):
	try:
		reader = csv.reader(open(raw_file, 'rb'), quoting=csv.QUOTE_NONE)
	except:
		print "!ERROR! File " + str(sys.argv[2]) + " not found!"
		print "Usage: k_discretize.py [k_value (positive, real-valued integer)] [input file] > [export file]"
		sys.exit()

	print "Data read from file " + str(sys.argv[2])

	data = []
	dataLookup = {}

	for index,line in enumerate(reader):
		#lookup
		key = (line[0],line[1])
		val = [line[2],line[3],line[4],line[5],line[6],line[7],line[8],line[9],line[10],line[11],line[12],line[13],line[14]]

		dataLookup[key] = val

		#data list
		data.append(line)

	print "Data read complete. " + str(time.time() - startTime) + " seconds."
	print "  ->Lookup table contains " + str(len(dataLookup)) + " datapoints."
	print "  ->Data table contains " + str(len(data)) + " datapoints."

	return deepcopy(dataLookup),deepcopy(data)

#MAIN
lookupTable,dataList = read_data(sys.argv[2])