#!/usr/bin/env python2.7

import sys,math,operator,time,csv
from copy import deepcopy

from sklearn import linear_model
from sklearn import preprocessing
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import matplotlib.offsetbox as offsetbox

startTime = time.time()

#-----------------------------------------------------------------------------------------------------
def printUsageAndExit():
	print "Usage: plot.py [dataFile] [options (optional)]"
	print "  Options:"
	print "   --features #1 #2       Will be used as x-coord,y-coord (default: 2 highest weighted features)"
	sys.exit()
#-----------------------------------------------------------------------------------------------------

if len(sys.argv) < 2:
	printUsageAndExit()

try:
	dataReader = csv.reader(open(sys.argv[1], 'rb'), quoting=csv.QUOTE_NONE)
except:
	printUsageAndExit()

if "--features" in sys.argv:
	try:
		useFeatureAsX = sys.argv[sys.argv.index("--features") + 1]
		useFeatureAsY = sys.argv[sys.argv.index("--features") + 2]
	except:
		printUsageAndExit()

#----------------------------------------------------------------------------------------------------
def constructData(reader):
	keys = []
	data = []
	outs = []

	for index,vec in enumerate(reader):
		if 'x' not in vec:
			keys.append((vec[0],vec[1]))
			data.append([int(vec[2]),int(vec[3]),float(vec[4]),float(vec[5]),float(vec[6]),float(vec[7]),float(vec[8]),float(vec[9]),float(vec[10]),float(vec[11]),float(vec[12]),float(vec[13])])
			outs.append(float(vec[14]))

	return deepcopy(keys),deepcopy(data),deepcopy(outs)
#----------------------------------------------------------------------------------------------------

keys,data,outs = constructData(dataReader)

if "--features" not in sys.argv:
	#train a bayes ridge regression and get the feature weights
	model = linear_model.BayesianRidge()
	model.fit(data,outs)

	weights = deepcopy(model.coef_)

	weights = np.absolute(weights)
	xCoord = max(weights)
	weights[weights.index(xCoord)] = 0
	yCoord = max(weights)

print "x,y features: " + str(xCoord) + "," + str(yCoord)