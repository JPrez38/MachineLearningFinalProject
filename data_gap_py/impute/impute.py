#!/usr/bin/env python2.7.4

import sys,math,cmath,operator,time,csv
import numpy as np 
from sklearn.preprocessing import Imputer
from sklearn.neighbors import NearestNeighbors
from copy import deepcopy

startTime = time.time()

#SETTINGS

def tran(data, placeHolder):
	#transform data for sciKit
	holder = deepcopy(data)

	for lineIndex,line in enumerate(holder):
		for attIndex,val in enumerate(line):
			if val == 'x':
				holder[lineIndex][attIndex] = placeHolder
	return holder

def impute(data):
	#run the scikit imputer
	imp = Imputer(missing_values='NaN', strategy='mean', axis=0, copy=True)
	imp.fit(data)
	return imp.transform(data)

def computeNN(data2):
	neighbors = []

	#nearest neighneigh
	neighneigh = NearestNeighbors(n_neighbors=1)
	neighneigh.fit(data2)
	for j,item in enumerate(data2):
		neighbor = neighneigh.kneighbors(data2[j],2,return_distance=False)
		neighbors.append(neighbor[0][1])

	return neighbors



if len(sys.argv) != 3: #check args
	print "Usage: impute.py [method='impute','NN', 'both'] [incompleteFile] > [completeFile]"
	sys.exit()
else: #args correct
	reader = csv.reader(open(sys.argv[2], 'rb'), quoting=csv.QUOTE_NONE)

	dataAppend = []
	dataDict = {}
	data = []

	for index,line in enumerate(reader):
		key = (line[0],line[1])
		val = (line[2],line[3],line[4],line[5])
		data.append([line[2],line[3],line[4],line[5]])
	


	if sys.argv[1] == "impute":
		data = tran(data, np.nan)
		transData = impute(data)

		#input new data into dataDict
		#loop over file. add new attributes
		reader2 = csv.reader(open(sys.argv[2], 'rb'), quoting=csv.QUOTE_NONE)
		for i,l in enumerate(reader2):
			for ai,a in enumerate(l):
				if a == 'x':
					l[ai] = transData[i][ai-2]
			dataDict[(l[0],l[1])] = [float(l[2]),float(l[3]),float(l[4]),float(l[5])]
			print str(l[0]) + "," + str(l[1]) + "," + str(l[2]) + "," + str(l[3]) + "," + str(l[4]) + "," + str(l[5])
		
	elif sys.argv[1] == "NN":
		data = tran(data, -1)
		neighbors = computeNN(data)

		#input new data into dataDict
		reader3 = csv.reader(open(sys.argv[2], 'rb'), quoting=csv.QUOTE_NONE)
		for i,l in enumerate(reader3):
			for ai,a in enumerate(l):
				if a == 'x':
					l[ai] = data[neighbors[i]][ai-2]
			dataDict[(l[0],l[1])] = [float(l[2]),float(l[3]),float(l[4]),float(l[5])]
			print str(l[0]) + "," + str(l[1]) + "," + str(l[2]) + "," + str(l[3]) + "," + str(l[4]) + "," + str(l[5])

	else: #BOTH MOODYFLACKA!
		holdData = deepcopy(tran(data, np.nan))
		transData = deepcopy(impute(holdData))

		data2 = []

		#print data
		#print "----------------------------------"

		#print transData

		#print "----------------------------------"

		neighbors = computeNN(transData)

		#input new data into dataDict
		reader3 = csv.reader(open(sys.argv[2], 'rb'), quoting=csv.QUOTE_NONE)
		for i,l in enumerate(reader3):
			for ai,a in enumerate(l):
				if a == 'x':
					l[ai] = transData[neighbors[i]][ai-2]
			dataAppend.append([l[2],l[3],l[4],l[5]])
			#dataDict[(l[0],l[1])] = [float(l[2]),float(l[3]),float(l[4]),float(l[5])]
			print str(l[0]) + "," + str(l[1]) + "," + str(l[2]) + "," + str(l[3]) + "," + str(l[4]) + "," + str(l[5])

print ""
print "Done -> " + str(time.time() - startTime) + "seconds."

		# print "---------------pass 2------------"

		# neighbors2 = computeNN(dataAppend)
		# #input new data into dataDict
		# reader4 = csv.reader(open(sys.argv[2], 'rb'), quoting=csv.QUOTE_NONE)
		# for i,l in enumerate(reader4):
		# 	for ai,a in enumerate(l):
		# 		if a == 'x':
		# 			l[ai] = dataAppend[neighbors[i]][ai-2]
		# 	#dataDict[(l[0],l[1])] = [float(l[2]),float(l[3]),float(l[4]),float(l[5])]
		# 	print str(l[0]) + "," + str(l[1]) + "," + str(l[2]) + "," + str(l[3]) + "," + str(l[4]) + "," + str(l[5])		