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
	print "    --error-margin #         # is percentile (.##) of acceptable loss"
	print "    --explicit-breakdown     Will print all test vectors, predictions, and actual values respectively"
	print "    --model #                # id of learning model to fit data to (default 1)"
	print "                             1: Ridge Bayesian Regression"
	print "                             2: Gaussian Naive Bayes"
	print "    --output [file]          Will output predictions (ordered same as data input) to file"
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
	if not (errorMargin >= 0.0 and errorMargin <= 1.0):
		printUsageAndExit()
else:
	errorMargin = .1

if "--explicit-breakdown" in sys.argv:
	breakdown = True
else:
	breakdown = False

if "--model" in sys.argv:
	mID = int(sys.argv[sys.argv.index("--model") + 1])
else:
	mID = 1


if "--output" in sys.argv:
	outFile = open(sys.argv[sys.argv.index("--output") + 1], 'w')
	output = True
else:
	output = False


print "  Acceptable error margin:        " + str(errorMargin)
print "  Explicit test vector breakdown: " + str(breakdown)
if mID == 1:
	print "  Training Model:                 Ridge Bayesian Regression"
elif mID == 2:
	print "  Training Model:                 GaussianNB"
print "  Output predictions?             " + str(output)

print "-" * 50

#----------------------------------------------------------------------------------------------------
def constructData(reader):
	keys = []
	data = []
	outs = []
	pops = []

	for index,vec in enumerate(reader):
		if 'x' not in vec:
			keys.append((vec[0],vec[1]))
			data.append([int(vec[2]),int(vec[3]),float(vec[4]),float(vec[5]),float(vec[6]),float(vec[7]),float(vec[8]),float(vec[9]),float(vec[10]),float(vec[11]),float(vec[12]),float(vec[13])])
			outs.append(float(vec[16]))
			pops.append(int(vec[15]))

	return deepcopy(keys),deepcopy(data),deepcopy(outs),deepcopy(pops)
#----------------------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------------------
def crunchTestResults(predictions,actuals):
	misses = 0
	totalError = 0
	totalErrorPercentile = 0

	for prediction,actual in zip(predictions,actuals):
		margin = math.fabs(actual-prediction)
		if float(margin)/float(actual) > errorMargin:
			misses += 1
		totalError += margin
		totalErrorPercentile += float(margin)/float(actual)

	return misses,float(float(misses)/float(len(actuals))),totalError,totalErrorPercentile
#----------------------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------------------
def writeOutputFile(keysTest, predictions, actuals, predictionsPop, actualsPop):
	outFile.write("KEY:Country,KEY:Year,Predicted,Actual,PredictedPopulation,ActualPopulation,ErrorPercentile" + "\n")
	for key,prediction,actual,predictionPop,actualPop in zip(keysTest,predictions,actuals,predictionsPop,actualsPop):
		outFile.write(str(key[0]) + "," + str(key[1]) + "," + str(prediction) + "," + str(actual) + "," + str(predictionPop) + "," + str(actualPop) + "," + str(float(math.fabs(prediction-actual))/float(actual)) + "\n")

#----------------------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------------------
def convertPopVals(decimals, population):
	converts = []

	for decimal,pop in zip(decimals,population):
		converts.append(float(decimal * pop))

	return deepcopy(converts)
#----------------------------------------------------------------------------------------------------


print "-" * 32

print "TRAINING FILE: " + str(sys.argv[1])
print "Constructing data lists..."
keys,data,outs,pops = constructData(dataReader)
t2 = time.time()
print " -> Construction COMPLETE. " + str(t2-startTime) + " seconds."
print "      Number of complete vectors generated from data: " + str(len(data))

print "-" * 32

print "TEST FILE: " + str(sys.argv[2])
print "Constructing test lists..."
testKeys,testData,testOuts,testPops = constructData(testReader)
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

#convert outputs
trainOutsPop = convertPopVals(outs,pops)
predictPop = convertPopVals(predictions,testPops)
testOutPop = convertPopVals(testOuts,testPops)


print "\nCrunchifying tasty test data stats for review... Yum"
misses,error,totalError,totalErrorPercentile = crunchTestResults(predictPop,testOutPop)
t6 = time.time()
if output: print " -> Wrote predictions to output file: " + str(sys.argv[sys.argv.index("--output") + 1])
print " -> Crunching COMPLETE. " + str(t6-t5) + " seconds."

print "-" * 32

print "ALGORITHM SUMMARY"
print "  Training Vectors:      " + str(len(data)) + " from file: " + str(sys.argv[1])
print "  Testing Vectors:       " + str(len(testData)) + " from file: " + str(sys.argv[2])
print "  Accuracy Summary:      " 
print "      -------------------------------------------------------"
print "      |        *****Correct/Incorrect Stats******"
print "      | " + str(len(testData) - misses) + " correct"
print "      | " + str(misses) + " incorrect"
print "      | " + str(len(testData)) + " total"
print "      | Prediction Accuracy:      " + str(1 - error)
print "      | Prediction Inaccuracy:    " + str(error)
print "      |"
print "      |        *****Marginal Accuracy Stats******"
#print "      | Total Error:           " + str(totalError)
print "      | Average Error:            " + str(float(totalError) / float(len(testData)))
print "      | Average Error Percentile: " + str(float(totalErrorPercentile) / float(len(testData)))
print "      -------------------------------------------------------"
print "  Total Time:            " + str(time.time() - startTime) + " seconds"

if output:
	print "\n  -> Writing outputs to file: " + str(sys.argv[sys.argv.index("--output") + 1])
	writeOutputFile(testKeys,predictions,testOuts,predictPop,testOutPop)


if breakdown:
	print "-" * 32
	print "EXPLICIT TEST VECTOR BREAKDOWN"
	i=0
	for prediction,actual in zip(predictPop,testOutPop):
		key = (testKeys[i][0],testKeys[i][1])
		print str(key) + "; Prediction: " + str(prediction) + "; Actual: " + str(actual)
		i += 1