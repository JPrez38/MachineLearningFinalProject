#!/usr/bin/env python2.7

import sys,math,operator,time,csv
from copy import deepcopy

import support

import numpy as np
import scipy as sp 
from scipy import interpolate

import matplotlib.pyplot as plt

from sklearn.ensemble import RandomForestRegressor

startTime = time.time()

#------------------------------------------------------------------------
def printUsageAndExit(error):
	if error != "":
		print "!ArgumentError: " + str(error)
	print "Usage: randomForest.py [trainFile] [testFile] [options (optional)"
	print "  Options:"
	print "    --max-depth #           Sets the max depth for the trees"
	print "    --error-margin #        Sets confidence interval"
	print "    --tryall                Tries all max-depths from 1 to --maxDepth"
	print "        --plot              Plots results"
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
			maxDepth = int(sys.argv[sys.argv.index("--max-depth")+1])
		except:
			printUsageAndExit("--max-depth # must be integer value")
	else:
		maxDepth = 10

	if "--error-margin" in sys.argv:
		try:
			errorMargin = float(sys.argv[sys.argv.index("--error-margin")+1])
		except:
			printUsageAndExit("--error-margin must be number")
	else:
		errorMargin = .5


	tryAll = True if "--tryall" in sys.argv else False

	plot = True if "--plot" in sys.argv else False

	return dataReader,testReader,maxDepth,errorMargin,tryAll,plot
#------------------------------------------------------------------------


#arguments
dataReader,testReader,maxDepth,errorMargin,tryAll,plot = checkArgs()

sup = support.support()

#construct data 'n' shit
keys,data,outs,actuals,pops = sup.constructData(dataReader)
testKeys,testData,testOuts,testActuals,testPops = sup.constructData(testReader)

normData,normTestData,maxs = sup.normalize(data,testData)

npData = np.array(normData)
npOuts = np.array(outs)

npTestData = np.array(normTestData)
npTestOuts = np.array(testOuts)

if not tryAll:
	rf = RandomForestRegressor(max_depth=maxDepth)
	rf.fit(npData,npOuts)
	predictions = rf.predict(npTestData)
	misses,error,totalError,totalErrorPercentile = sup.crunchTestResults(predictions,npTestOuts,errorMargin)
	print "Accuracy: " + str(1-error)

else:
	accuracy = []
	for maxDepthIter in range(1,maxDepth+1):
		rf = RandomForestRegressor(max_depth=maxDepthIter)
		rf.fit(npData,npOuts)
		predictions = rf.predict(npTestData)
		misses,error,totalError,totalErrorPercentile = sup.crunchTestResults(predictions,npTestOuts,errorMargin)
		print "maxDepth = " + str(maxDepthIter)
		print " -> Accuracy: " + str(1-error)

		accuracy.append(1-error)

	#results for best depth
	print "\nResults for best depth:"
	print "   -------------------------------------------------------------------"
	print "   | maxDepth =         " + str(accuracy.index(max(accuracy)))
	print "   | Best Accuracy =    " + str(max(accuracy))
	print "   -------------------------------------------------------------------"

	if plot:
		#plot it 
		plt.figure(figsize=(8,6), dpi=80)
		plt.title("Accuracy of Random Forest Regressor within " + str(errorMargin) + " confidence interval")
		plt.xlabel("--max-depth - 1")
		plt.ylabel("Accuracy")
		plt.plot(accuracy, color="blue")
		
		plt.show()