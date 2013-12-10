#!/usr/bin/env python2.7

import sys,math,operator,time,csv
from copy import deepcopy

import support

from sklearn import linear_model
from sklearn.naive_bayes import GaussianNB
from sklearn import preprocessing
import numpy as np

class BayesianRidge(object):
	errorMargin = .5
	mID = 1
	normalize = True
	output = False
	outFile = ""

	def __init__(self,args_):
		sys.argv = args_

	#-----------------------------------------------------------------------------------------------------
	def printUsageAndExit(self):
		print "Usage: bayesMain.py [dataFile] [testFile] [options (optional)]"
		print "NO CROSS VALIDATION!"
		print "  Options:"
		print "    --error-margin #         # is percentile (.##) of acceptable loss"
		print "                             (default=.5)"
		#print "    --explicit-breakdown     Will print all test vectors, predictions, and actual values respectively"
		print "    --model #                # id of learning model to fit data to"
		print "                             (default 1)"
		print "        1: Ridge Bayesian Regression"
		#print "        2: Gaussian Naive Bayes"
		print "    --normalize              Will normalize features before fitting model"
		print "    --output [file]          Will output predictions (ordered same"
		print "                             as data input) to file"
		sys.exit()
	#-----------------------------------------------------------------------------------------------------

	#-----------------------------------------------------------------------------------------------------
	def checkArgs(self):
		if len(sys.argv) < 3:
			self.printUsageAndExit()

		try:
			dataReader = csv.reader(open(sys.argv[1], 'rb'), quoting=csv.QUOTE_NONE)
			testReader = csv.reader(open(sys.argv[2], 'rb'), quoting=csv.QUOTE_NONE)
		except:
			self.printUsageAndExit()


		#get options args
		print "-" * 50

		print "Program arguments: "
		if "--error-margin" in sys.argv:
			errorMargin = float(sys.argv[sys.argv.index("--error-margin") + 1])
			if not (errorMargin >= 0.0 and errorMargin <= 1.0):
				self.printUsageAndExit()
		else:
			errorMargin = .5

		if "--explicit-breakdown" in sys.argv:
			breakdown = True
		else:
			breakdown = False

		if "--model" in sys.argv:
			try:
				mID = int(sys.argv[sys.argv.index("--model") + 1])
			except:
				self.printUsageAndExit()
		else:
			mID = 1


		normalize = True if "--normalize" in sys.argv else False


		if "--output" in sys.argv:
			try:
				outFile = open(sys.argv[sys.argv.index("--output") + 1], 'w')
			except:
				self.printUsageAndExit()
			output = True
		else:
			outFile = ""
			output = False


		print "  Acceptable error margin:        " + str(errorMargin)
		print "  Explicit test vector breakdown: " + str(breakdown)
		if mID == 1:
			print "  Training Model:                 Ridge Bayesian Regression"
		elif mID == 2:
			print "  Training Model:                 GaussianNB"
		print "  Normalize features?             " + str(normalize)
		print "  Output predictions?             " + str(output)
		print "  Crossvalidation?                False"

		print "-" * 50
		print ""

		return dataReader,testReader,errorMargin,mID,normalize,output,outFile,breakdown
	#-----------------------------------------------------------------------------------------------------

	#-----------------------------------------------------------------------------------------------------
	def run(self):
		startTime = time.time()

		#check arguments
		dataReader,testReader,errorMargin,mID,normalize,output,outFile,breakdown = self.checkArgs()

		#initialize support routines
		sup = support.support()

		print "TRAINING FILE: " + str(sys.argv[1])
		print "Constructing data lists..."
		keys,data,outs,actuals,pops = sup.constructData(dataReader)
		t2 = time.time()
		print " -> Construction COMPLETE. " + str(t2-startTime) + " seconds."
		print "      Number of complete vectors generated from data: " + str(len(data))

		print "-" * 32

		print "TEST FILE: " + str(sys.argv[2])
		print "Constructing test lists..."
		testKeys,testData,testOuts,testActuals,testPops = sup.constructData(testReader)
		t3 = time.time()
		print " -> Construction COMPLETE. " + str(t3-t2) + " seconds."
		print "      Number of complete vectors generated from data: " + str(len(testData))

		if normalize:
			print "-" * 32
			print "Normalizing features..."
			data,testData,maxs = sup.normalize(data,testData)

			print "  -> Maximums ="
			print maxs

		print "-" * 32

		#BAYES RIDGE
		if mID == 1:
			print "Fitting Bayesian Ridge model to " + str(len(data)) + " vectors:"
			print " -> Using " + str(len(data)) + " vectors."
			model = linear_model.BayesianRidge()
			dataMatrix = np.array(data)
			outsMatrix = np.array(outs)
			model.fit(dataMatrix,outsMatrix)
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

		#convert outputs PERCENTILE -> POPULATION FIGURE
		predictPop = sup.convertPopVals(predictions,testPops)


		print "\nCrunchifying tasty test data stats for review... Yum"
		misses,error,totalError,totalErrorPercentile = sup.crunchTestResults(predictPop,testActuals,errorMargin)
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
		print "      | Using " + str(errorMargin) + " acceptable error margin:"
		print "      |    " + str(len(testData) - misses) + " correct"
		print "      |    " + str(misses) + " incorrect"
		print "      |    " + str(len(testData)) + " total"
		print "      | Prediction Accuracy:      " + str(1 - error)
		print "      | Prediction Inaccuracy:    " + str(error)
		print "      |"
		print "      |        *****Marginal Accuracy Stats******"
		print "      | NOT FOR FINAL EVALUATION PURPOSES"
		#print "      | Total Error:           " + str(totalError)
		print "      | Average Population Error: " + str(float(totalError) / float(len(testData)))
		print "      | Average Error Percentile: " + str(float(totalErrorPercentile) / float(len(testData)))
		print "      -------------------------------------------------------"
		print "  Total Time:            " + str(time.time() - startTime) + " seconds"

		if output:
			print "\n  -> Writing outputs to file: " + str(sys.argv[sys.argv.index("--output") + 1])
			info = [0] * 5
			#model
			info[0] = "Naive Bayesian Ridge" if model==1 else "GaussianNB"
			#numvectors
			info[1] = len(data)
			info[2] = len(testData)
			#average error
			info[3] = str(float(totalError) / float(len(testData)))
			#average percentile error
			info[4] = str(float(totalErrorPercentile) / float(len(testData)))

			sup.writeOutputFile(testKeys,predictions,testOuts,predictPop,testOutPop,info,outFile)


		if breakdown:
			print "-" * 32
			print "EXPLICIT TEST VECTOR BREAKDOWN"
			i=0
			for prediction,actual in zip(predictPop,testOutPop):
				key = (testKeys[i][0],testKeys[i][1])
				print str(key) + "; Prediction: " + str(prediction) + "; Actual: " + str(actual)
				i += 1