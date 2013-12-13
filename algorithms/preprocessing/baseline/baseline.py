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

	return dataReader,testReader
#--------------------------------------------------------------------------

#get arguments
dataReader,testReader = checkArgs()

keys,data,outs,actuals,pops = sup.constructData(dataReader)
testKeys,testData,testOuts,testActuals,testPops = sup.constructData(testReader)


