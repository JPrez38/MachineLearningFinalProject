#!/usr/bin/env python2.7

import sys,math,operator,time,csv
from copy import deepcopy

import bayesianRidge,bayesianRidge_crossVal

#----------------------------------------------------------------------------------------
def printUsageAndExit():
	print "Usage: bayesMain.py [train_file] [test_file (only when --crossval is not used)] [options (optional)]"
	print "  Options:"
	print "    --crossval #         Will use cross validation. Leave out the"
	print "                         test_file from args!"

#----------------------------------------------------------------------------------------

if "--crossval" in sys.argv:
	bRidge = bayesianRidge_crossVal.BayesianRidge_crossVal(sys.argv)
	bRidge.run()
else:
	bRidge = bayesianRidge.BayesianRidge(sys.argv)
	bRidge.run()