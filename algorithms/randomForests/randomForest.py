#!/usr/bin/env python2.7

import sys,math,operator,time,csv
from copy import deepcopy

import support

import numpy as numpy
import scipy as sp 

from sklearn.ensemble import RandomForestRegressor

startTime = time.time()

#------------------------------------------------------------------------
def printUsageAndExit(error):
	print "Usage: randomForest.py [trainFile] [testFile] [options (optional)"
	print "  Options:"
	print "    --max-depth #           Sets the max depth for the trees"
	sys.exit()
#------------------------------------------------------------------------

#------------------------------------------------------------------------
def checkArgs():
	if len(sys.argv) < 3:
		printUsageAndExit("Your arguments are inadequate and you should feel inadequate.")

	try:
		dataReader = csv.reader(open(sys.argv[1], 'rb'), quoting=csv.QUOTE_NONE)
		testReader = csv.reader(open(sys.argv[2], 'rb'), quoting=csv.QUOTE_NONE)
	except:
		printUsageAndExit("Your arguments are inadequate and you should feel inadequate.")

	if "--max-depth" in sys.argv:
		try:
			maxDepth = 

	return dataReader,testReader
#------------------------------------------------------------------------


#arguments
dataReader,testReader = checkArgs()

sup = support.support()

#construct data 'n' shit
keys,data,outs,actuals,pops = sup.constructData(dataReader)
testKeys,testData,testOuts,testActuals,testPops = sup.constructData(testReader)

npData = np.array(data)
npOuts = np.array(outs)

npTestData = np.array(testData)
npTestOuts = np.array(testOuts)

