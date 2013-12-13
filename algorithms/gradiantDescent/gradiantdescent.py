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
from sklearn.cross_validation import cross_val_score
from sklearn import svm
from sklearn.datasets import make_blobs
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.lda import LDA

import random as rand

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

def extremeRand(trainData,testData,trainOuts,testOuts):
	clf = ExtraTreesClassifier(n_estimators=5, max_depth=10,
      min_samples_split=1, random_state=2)
	print(clf.fit(trainData,trainOuts))
	predictions = clf.predict(testData)
	print(predictions)
	misses,error = sup.crunchTestResults(predictions,testOuts,.5)
	print(1-error)

def ldapredict(trainData,testData,trainOuts,testOuts):
	clf = LDA()
	print(clf.fit(trainData,trainOuts))
	predictions = clf.predict(testData)
	print(predictions)
	misses,error = sup.crunchTestResults(predictions,testOuts,.5)
	print(1-error)

def randomForest(trainData,testData,trainOuts,testOuts):
	clf = RandomForestClassifier(max_depth=50)
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

avg = np.average(numpyOuts)

avgPredictions = [avg]*len(outs)

avgmisses,avgerror = sup.crunchTestResults(avgPredictions,tstOuts,.5)
print(1-avgerror)


#gradiantDescent(normdata,normTestData,outs,tstOuts)
#svmPredict(normdata,normTestData,outs,tstOuts)
#extremeRand(normdata,normTestData,outs,tstOuts)
#ldapredict(normdata,normTestData,outs,tstOuts)
randomForest(normdata,normTestData,outs,tstOuts)

