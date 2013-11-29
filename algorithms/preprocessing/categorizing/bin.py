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
	print "Usage: bin.py [num_bins (positive, real-valued integer)] [input file] > [export file]"
	sys.exit()

try:
	numBins = int(sys.argv[1])
except:
	print "Usage: bin.py [num_bins (positive, real-valued integer)] [input file] > [export file]"
	sys.exit()

def readData(raw_file):
	try:
		reader = csv.reader(open(raw_file, 'rb'), quoting=csv.QUOTE_NONE)
	except:
		print "!ERROR! File " + str(sys.argv[2]) + " not found! Your file was in another castle."
		print "Usage: bin.py [num_bins (positive, real-valued integer)] [input file] > [export file]"
		sys.exit()

	# print "Data read from file " + str(sys.argv[2])

	data = []
	dataLookup = {}

	for index,line in enumerate(reader):
		#lookup
		key = (line[0],line[1])
		val = [line[2],line[3],line[4],line[5],line[6],line[7],line[8],line[9],line[10],line[11],line[12],line[13],line[14]]

		dataLookup[key] = val

		#data list
		data.append(line)

	# print "Data read complete. " + str(time.time() - startTime) + " seconds."
	# print "  ->Lookup table contains " + str(len(dataLookup)) + " datapoints."
	# print "  ->Data table contains " + str(len(data)) + " datapoints."

	return deepcopy(dataLookup),deepcopy(data)


def findMinMax(data):
	mini = 0
	maxi = 0

	for index,vector in enumerate(data):
		if vector[14] != 'x':
			if float(vector[14]) < mini:
				mini = float(vector[14])
			elif float(vector[14]) > maxi:
				maxi = float(vector[14])
		else:
			continue

	return mini,maxi,maxi-mini


def binData(data,bins):
	binnedData = deepcopy(data)

	for index,vector in enumerate(data):
		if vector[14] != 'x':
			for binNum,bin in enumerate(bins):
				if float(vector[14]) < bin:
					binnedData[index].append(binNum+1)
					break
		else:
			binnedData[index].append('noBin')

	return binnedData


#MAIN
lookupTable,dataList = readData(sys.argv[2])

mini,maxi,rang = findMinMax(dataList)
binSize = int(rang / numBins)

bins = []
for i in range(1,numBins):
	bins.append(i * binSize)

binnedData = binData(dataList,bins)

for vec in binnedData:
	print str(vec[0]) + "," + str(vec[1]) + "," + str(vec[2]) + "," + str(vec[3]) + "," + str(vec[4]) + "," + str(vec[5]) + ","  + str(vec[6]) + "," + str(vec[7]) + ","  + str(vec[8]) + "," + str(vec[9]) + "," + str(vec[10]) + "," + str(vec[11]) + ","  + str(vec[12]) + "," + str(vec[13]) + "," + str(vec[14]) + "," + str(vec[15])

