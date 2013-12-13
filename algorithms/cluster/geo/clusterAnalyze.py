#!/usr/bin/env python2.7

import sys,math,operator,time,csv
from copy import deepcopy

import numpy as np
import scipy as sp

import support
sup = support.GeoSupport()

#-------------------------------------------------------------------------------------
def printUsageAndExit(error):
	print "-" * 64
	if error != "":
		print "ArgumentError: " + str(error)

	print "Usage: clusterAnalyze.py [clustered output] [options (optional)]"
	print "  Options:"
	print "    "
	print "-" * 64
	sys.exit()
#-------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------
def checkArgs():
	if len(sys.argv) < 2:
		printUsageAndExit("Your arguments are inadequate. And you are an asshole.")

	try:
		reader = csv.reader(open(sys.argv[1], 'rU'), quoting=csv.QUOTE_NONE)
	except:
		printUsageAndExit("Neoope. That file aint right, brah.")

	return reader
#-------------------------------------------------------------------------------------

#get arguments
reader = checkArgs()

data,clusters = sup.constructData(reader)

for clusterID in clusters:
	