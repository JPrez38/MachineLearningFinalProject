import sys,math,operator,time,csv
from copy import deepcopy

import support

from sklearn import linear_model
from sklearn.naive_bayes import GaussianNB
from sklearn import preprocessing
import numpy as np
from sklearn.cross_validation import KFold

class BayesianRidge_crossVal(object):

	def __init__(self,args_):
		sys.argv = args_

		#-----------------------------------------------------------------------------------------------------
	def printUsageAndExit(self):
		print "Usage: bayesMain.py [dataFile] [--crossval #] [options (optional)]"
		print "CROSS VALIDATION!"
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

		try:
			crossvalNum = int(sys.argv[sys.argv.index("--crossval")+1])
		except:
			self.printUsageAndExit()

		print "  Acceptable error margin:        " + str(errorMargin)
		print "  Explicit test vector breakdown: " + str(breakdown)
		if mID == 1:
			print "  Training Model:                 Ridge Bayesian Regression"
		elif mID == 2:
			print "  Training Model:                 GaussianNB"
		print "  Normalize features?             " + str(normalize)
		print "  Output predictions?             " + str(output)
		print "  Crossvalidation?                True, " + str(crossvalNum)

		print "-" * 50
		print ""

		return dataReader,errorMargin,mID,normalize,output,outFile,breakdown,crossvalNum
	#-----------------------------------------------------------------------------------------------------

	#-----------------------------------------------------------------------------------------------------
	def run(self):
		startTime = time.time()

		#check arguments
		dataReader,errorMargin,mID,normalize,output,outFile,breakdown,crossvalNum = self.checkArgs()

		#initialize support routines
		sup = support.support()

		print "TRAINING FILE: " + str(sys.argv[1])
		print "Constructing data lists..."
		keys,data,outs,actuals,pops = sup.constructData(dataReader)
		t2 = time.time()
		print " -> Construction COMPLETE. " + str(t2-startTime) + " seconds."
		print "      Number of complete vectors generated from data: " + str(len(data))

		if normalize:
			print "-" * 32
			print "Normalizing features..."
			data,maxs = sup.normalize_crossval(data)

			print "  -> Maximums ="
			print maxs

		print "-" * 32

		#CREATE SETS FOR CROSS VALIDATION!
		print "Creating crossvalidation sets..."

		dataMatrix = np.array(data)
		outsMatrix = np.array(outs)
		popsMatrix = np.array(pops)

		construct = KFold(len(outsMatrix),n_folds=crossvalNum,indices=False)

		print " -> Sets COMPLETE."
		print "-" * 32

		print "Running crossvalidation..."
		accuracy = []

		iteration = 0
		for trainInd,testInd in construct:
			iteration += 1
			X_train,X_test,y_train,y_test,pop_train,pop_test = dataMatrix[trainInd], dataMatrix[testInd], outsMatrix[trainInd], outsMatrix[testInd], popsMatrix[trainInd], popsMatrix[testInd]
			model = linear_model.BayesianRidge()
			model.fit(X_train,y_train)

			predictions = deepcopy(model.predict(X_test))
			predictPop = sup.convertPopVals(predictions,pop_test)
			misses,error,totalError,totalErrorPercentile = sup.crunchTestResults(predictPop,actuals,errorMargin)
			print " -> Iteration " + str(iteration) + " complete with accuracy " + str(1-error)
			accuracy.append(1-error)

		avgAccuracy = float(sum(accuracy)) / float(iteration)
		print avgAccuracy



		



			
