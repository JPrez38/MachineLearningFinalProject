import sys,math,operator,time,csv
from copy import deepcopy

import numpy as np
import scipy as sp

import matplotlib.pyplot as plt
import matplotlib.offsetbox as offsetbox

from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import scale
from sklearn.linear_model import SGDRegressor

import random as rand

import support

sup = support.support()

#----------------------------------------------------------------------
def printUsageAndExit(error):
	print "-" * 64
	print "ARGUMENT ERROR: " + str(error)
	print "Usage: kmeans.py [dataFile] [options (optional)]"
	print "  Options:"
	print "    --k #           Sets the number of clusters (default = 5)"
	print "-" * 64
	sys.exit()
#----------------------------------------------------------------------

#----------------------------------------------------------------------
def checkArgs():

	if len(sys.argv) < 2:
		printUsageAndExit("")

	try:
		reader = csv.reader(open(sys.argv[1], 'rU'), quoting=csv.QUOTE_NONE)
	except:
		printUsageAndExit("Error occured opening specified file")

	return reader
#----------------------------------------------------------------------

reader = checkArgs()


print "Constructing data..."
keys,data,outs,actuals,pops = sup.constructData(reader)

print " -> " + str(len(data)) + " vectors generated\n"

normdata,maxs = sup.normalize_crossval(data)

numpyData = np.array(normdata)
numpyOuts = np.array(outs)

print numpyOuts

outsTest = []
for i in range(len(data)):
	outsTest.append(rand.randint(0,1))
print outsTest

clf = SGDRegressor(loss="squared_loss")
clf.fit(numpyData,numpyOuts)