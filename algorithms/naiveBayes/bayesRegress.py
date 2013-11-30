#!/usr/bin/env python2.7

import sys,math,operator,time,csv
from copy import deepcopy

from sklearn import linear_model
from sklearn.naive_bayes import GaussianNB
from sklearn import preprocessing

startTime = time.time()

#-----------------------------------------------------------------------------------------------------
def printUsageAndExit():
	print "Usage: bayesRegress.py [dataFile] [testFile] [options (optional)]"
	print "  Options:"
	print "    --error-margin #         # of type float (or int) for calculating prediction error"
	print "    --explicit-breakdown     Will print all test vectors, predictions, and actual values respectively"
	print "    --model #                # id of learning model to fit data to (default 1)"
	print "                             1: Ridge Bayesian Regression"
	print "                             2: Gaussian Naive Bayes"
	sys.exit()
#-----------------------------------------------------------------------------------------------------


if len(sys.argv) < 3:
	printUsageAndExit()

try:
	dataReader = csv.reader(open(sys.argv[1], 'rb'), quoting=csv.QUOTE_NONE)
	testReader = csv.reader(open(sys.argv[2], 'rb'), quoting=csv.QUOTE_NONE)
except:
	printUsageAndExit()


#get options args
print "-" * 50

print "Program arguments: "
if "--error-margin" in sys.argv:
	errorMargin = float(sys.argv[sys.argv.index("--error-margin") + 1])
else:
	errorMargin = 1000.00

if "--explicit-breakdown" in sys.argv:
	breakdown = True
else:
	breakdown = False

if "--model" in sys.argv:
	mID = int(sys.argv[sys.argv.index("--model") + 1])
else:
	mID = 1

print "  Acceptable error margin:        " + str(errorMargin)
print "  Explicit test vector breakdown: " + str(breakdown)
if mID == 1:
	print "  Training Model:                 Ridge Bayesian Regression"
elif mID == 2:
	print "  Training Model:                 GaussianNB"

print "-" * 50

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

#----------------------------------------------------------------------------------------------------
def crunchTestResults(predictions,actuals):
	misses = 0

	for prediction,actual in zip(predictions,actuals):
		margin = math.fabs(actual-prediction)
		if margin > errorMargin:
			misses += 1

	return misses,float(float(misses)/float(len(actuals)))
#----------------------------------------------------------------------------------------------------


print "-" * 32

print "TRAINING FILE: " + str(sys.argv[1])
print "Constructing data lists..."
keys,data,outs = constructData(dataReader)
t2 = time.time()
print " -> Construction COMPLETE. " + str(t2-startTime) + " seconds."
print "      Number of complete vectors generated from data: " + str(len(data))

print "-" * 32

print "TEST FILE: " + str(sys.argv[2])
print "Constructing test lists..."
testKeys,testData,testOuts = constructData(testReader)
t3 = time.time()
print " -> Construction COMPLETE. " + str(t3-t2) + " seconds."
print "      Number of complete vectors generated from data: " + str(len(testData))

print "-" * 32

#BAYES RIDGE
if mID == 1:
	print "Fitting Bayesian Ridge model to " + str(len(data)) + " vectors:"
	print " -> Using " + str(len(data)) + " vectors."
	model = linear_model.BayesianRidge()
	model.fit(data,outs)
	t4 = time.time()
	print " -> Training COMPLETE. " + str(t4-t3) + " seconds."
	print "      Weight vector:\n" + str(model.coef_)

#GAUSSIAN NB
elif mID == 2:
	print "Fitting GaussianNB model to " + str(len(data)) + " vectors:"
	print " -> Using " + str(len(data)) + " vectors."
	model = GaussianNB()
	model.fit(data,outs)
	t4 = time.time()
	print " -> Training COMPLETE. " + str(t4-t3) + " seconds."

print "-" * 32

print "Testing against test file..."
predictions = deepcopy(model.predict(testData))
t5 = time.time()
print " -> Testing COMPLETE. " + str(t5-t4) + " seconds."

print "\nCrunchifying tasty test data stats for review... Yum"
misses,error = crunchTestResults(predictions,testOuts)
t6 = time.time()
print " -> Crunching COMPLETE. " + str(t6-t5) + " seconds."

print "-" * 32

print "BAYESIAN REGRESSION BREAKDOWN"
print "  Training vectors: " + str(len(data)) + " from file: " + str(sys.argv[1])
print "  Testing vectors: " + str(len(testData)) + " from file: " + str(sys.argv[2])
print "  Prediction misses: " + str(misses) + " vectors out of total " + str(len(testData))
print "  Prediction accuracy: " + str(1 - error)

if breakdown:
	print "-" * 32
	print "EXPLICIT TEST VECTOR BREAKDOWN"
	i=0
	for prediction,actual in zip(predictions,testOuts):
		key = (testKeys[i][0],testKeys[i][1])
		print str(key) + "; Prediction: " + str(prediction) + "; Actual: " + str(actual)
		i += 1

