#!/usr/bin/env python2.7

import sys,math,operator,time,csv
from copy import deepcopy

import numpy as np
import scipy as sp

import support
sup = support.support()

#--------------------------------------------------------------------------
def printUsageAndExit(error):
	if error != "":
		print "ArgumentError: " + str(error)

	print "Usage: baseline.py [trainFile] [testFile] [options (optional)]"
	print "  Options:"
	print "    --error-margin #         Set error-margin for accuracy evaluation"
	print "    --computation #          Sets the type of baseline to generate"
	print "          1 : Total Average"
	print "          2 : Average Per Country"
	sys.exit()
#--------------------------------------------------------------------------

#--------------------------------------------------------------------------
def checkArgs():
	if len(sys.argv) < 3:
		printUsageAndExit("Insufficient arguments provided. Dumbass.")

	try:
		dataReader = csv.reader(open(sys.argv[1], 'rU'), quoting=csv.QUOTE_NONE)
		testReader = csv.reader(open(sys.argv[2], 'rU'), quoting=csv.QUOTE_NONE)
	except:
		self.printUsageAndExit("Unable to open designated train or test file.")

	if "--error-margin" in sys.argv:
		try:
			errorMargin = float(sys.argv[sys.argv.index("--error-margin")+1])
		except:
			printUsageAndExit("--error-margin must be a number")
	else:
		errorMargin = .5

	try:
		comp = int(sys.argv[sys.argv.index("--computation")+1]) if "--computation" in sys.argv else 1
	except:
		printUsageAndExit("--computation must be a valid integer")

	return dataReader,testReader,errorMargin,comp
#--------------------------------------------------------------------------

#get arguments
dataReader,testReader,errorMargin,comp = checkArgs()

keys,data,outs,actuals,pops = sup.constructData(dataReader)
testKeys,testData,testOuts,testActuals,testPops = sup.constructData(testReader)

npOuts = np.array(outs)


if comp == 1:
	predictions = [np.average(npOuts)] * len(outs)
	misses,error,totalError,totalErrorPercentile = sup.crunchTestResults(predictions,testOuts,errorMargin)

elif comp == 2:
	averages = {}
	currentIndex = 0
	currentSum = 0.0
	numHolder = 0
	for keyIndex,key in enumerate(keys):
		if key[0] == keys[currentIndex][0]:
			currentSum += outs[keyIndex]
			numHolder += 1
		else:
			if numHolder > 0:
				averages[key[0]] = float(currentSum)/float(numHolder)
			else:
				averages[key[0]] = outs[keyIndex]
			currentIndex = keyIndex
			currentSum = 0.0
			numHolder = 0

	print averages

	#construct predictions
	predictions = []
	for key in keys:
		predictions.append(averages[key[0]])

	misses,error,totalError,totalErrorPercentile = sup.crunchTestResults(predictions,outs,errorMargin)



#Print accuracy
print "   ------------------------------------------------------------------------"
print "   | Error Margin (Confidence Interval):           " + str(errorMargin)
print "   | Baseline Accuracy:                            " + str(1-error)
print "   ------------------------------------------------------------------------"