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

	return dataReader,testReader,errorMargin
#--------------------------------------------------------------------------

#get arguments
dataReader,testReader,errorMargin = checkArgs()

keys,data,outs,actuals,pops = sup.constructData(dataReader)
testKeys,testData,testOuts,testActuals,testPops = sup.constructData(testReader)

npOuts = np.array(outs)

predictions = [np.average(npOuts)] * len(outs)

misses,error,totalError,totalErrorPercentile = sup.crunchTestResults(predictions,testOuts,errorMargin)

#Print accuracy
print "   ------------------------------------------------------------------------"
print "   | Error Margin (Confidence Interval):           " + str(errorMargin)
print "   | Baseline Accuracy (by predicting accuracy):   " + str(1-error)
print "   ------------------------------------------------------------------------"