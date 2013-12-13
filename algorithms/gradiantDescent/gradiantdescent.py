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
<<<<<<< HEAD
from sklearn import svm
=======

import random as rand
>>>>>>> 51b178c003ced5ca16aecaff6810567bccec0c1a

import support

sup = support.support()

#----------------------------------------------------------------------
def printUsageAndExit(error):
	print "-" * 64
	print "ARGUMENT ERROR: " + str(error)
	print "Usage: gradientdescent.py [dataFile] [testFile] [options (optional)]"
	print "  Options:"
	print "-" * 64
	sys.exit()
#----------------------------------------------------------------------

#----------------------------------------------------------------------
def checkArgs():

	if len(sys.argv) < 3:
		printUsageAndExit("")

	try:
		reader = csv.reader(open(sys.argv[1], 'rU'), quoting=csv.QUOTE_NONE)
	except:
		printUsageAndExit("Error occured opening specified file")

	try:
		testReader = csv.reader(open(sys.argv[2], 'rU'), quoting=csv.QUOTE_NONE)
	except:
		printUsageAnExit("Error")

	return reader,testReader
#----------------------------------------------------------------------

def gradiantDescent(trainData,testData,trainOuts,testOuts):
	clf = SGDRegressor(loss="squared_loss")
	print(clf.fit(trainData,trainOuts))
	print(clf.coef_)
	predictions = clf.predict(testData)
	print(predictions)
	misses,error = sup.crunchTestResults(predictions,testOuts,.5)
	print(1-error)

def svmPredict(trainData,testData,trainOuts,testOuts):
	clf = svm.SVR()
	print(clf.fit(trainData,trainOuts))
	predictions = clf.predict(testData)
	print(predictions)
	misses,error = sup.crunchTestResults(predictions,testOuts,.5)
	print(1-error)

reader,testReader = checkArgs()


print "Constructing data..."
keys,data,outs,actuals,pops = sup.constructData(reader)
tstKeys,tstdata,tstOuts,tstActuals,tstPops = sup.constructData(testReader)

print " -> " + str(len(data)) + " vectors generated\n"

normdata,normTestData,maxs = sup.normalize(data,tstdata)

numpyOuts = np.array(outs)

<<<<<<< HEAD
avg = np.average(numpyOuts)

avgPredictions = [avg]*len(outs)

avgmisses,avgerror = sup.crunchTestResults(avgPredictions,tstOuts,.5)
print(1-avgerror)


gradiantDescent(normdata,normTestData,outs,tstOuts)
svmPredict(normdata,normTestData,outs,tstOuts)



=======
print numpyOuts

outsTest = []
for i in range(len(data)):
	outsTest.append(rand.randint(0,1))
print outsTest

clf = SGDRegressor(loss="squared_loss")
clf.fit(numpyData,numpyOuts)
>>>>>>> 51b178c003ced5ca16aecaff6810567bccec0c1a
