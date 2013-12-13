import sys,math,operator,time,csv
from copy import deepcopy

import support

from sklearn import linear_model
from sklearn.naive_bayes import GaussianNB
from sklearn import preprocessing
import numpy as np
from sklearn.cross_validation import KFold

import scipy as sp
import matplotlib.pyplot as plt
import matplotlib.offsetbox as offsetbox

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
		print "    --plotall                Attempt {2,...,--crossvalidation #} and graph"
		print "                             average accuracy"
		sys.exit()
	#-----------------------------------------------------------------------------------------------------

	#-----------------------------------------------------------------------------------------------------
	def checkArgs(self):
		if len(sys.argv) < 3:
			self.printUsageAndExit()

		try:
			dataReader = csv.reader(open(sys.argv[1], 'rU'), quoting=csv.QUOTE_NONE)
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

		plot = True if "--plotall" in sys.argv else False

		print "  Acceptable error margin:        " + str(errorMargin)
		print "  Explicit test vector breakdown: " + str(breakdown)
		if mID == 1:
			print "  Training Model:                 Ridge Bayesian Regression"
		elif mID == 2:
			print "  Training Model:                 GaussianNB"
		print "  Normalize features?             " + str(normalize)
		print "  Output predictions?             " + str(output)
		print "  Crossvalidation?                True, " + str(crossvalNum)
		print "  Plot all?                       " + str(plot)

		print "-" * 50
		print ""

		return dataReader,errorMargin,mID,normalize,output,outFile,breakdown,crossvalNum,plot
	#-----------------------------------------------------------------------------------------------------

	def crossVal(self,data,outs,pops,actuals,errorMargin,crossvalNum, sup):
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
		return deepcopy(accuracy),avgAccuracy

	#-----------------------------------------------------------------------------------------------------
	def run(self):
		startTime = time.time()

		#check arguments
		dataReader,errorMargin,mID,normalize,output,outFile,breakdown,crossvalNum,plot = self.checkArgs()

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

		if plot:
			accTotal = []
			avgAccuracyTotal = []

			plt.figure(figsize=(8,6), dpi=80)
			plt.title("Test Accuracy of KMeans within " + str(errorMargin) + " Margin")
			plt.xlabel("Crossvalidation Fold #")
			plt.ylabel("Average Accuracy Per Full Pass")
			plt.xticks(np.linspace(0,crossvalNum,crossvalNum+1,endpoint=True))

			colors = ["red","green","blue","orange","pink","purple","yellow","gray","black","turqoise"]

			for i in range(2,crossvalNum+1):
				accuracy,avgAccuracy = self.crossVal(data,outs,pops,actuals,errorMargin,i,sup)
				avgAccuracyTotal.append(avgAccuracy)
				plt.plot(accuracy,color=colors[i-2],label="k = " + str(i))

			plt.legend(loc=4)

			plt.figure(figsize=(8,6), dpi=80)
			plt.title("Test Average Accuracy for All Folds at " + str(errorMargin) + " Error Margin")
			plt.xlabel("--crossval # (k-2)")
			plt.ylabel("Average Accuracy Per Full Pass")
			plt.xticks(np.linspace(0,crossvalNum,crossvalNum+1,endpoint=True))
			plt.plot(avgAccuracyTotal,color="green")

			plt.show()


		else:
			accuracy,avgAccuracy = self.crossVal(data,outs,pops,actuals,errorMargin,crossvalNum, sup)

			#print out test results before graphing
			print "CROSSVALIDATION BREAKDOWN"
			print "  ---------------------------------------------------------------------------"
			print "  | Average Accuracy of Crossvalidation =   " + str(avgAccuracy)
			print "  | KMeans, k =                             " + str(crossvalNum)
			print "  | Test Set Size =                   " + str(len(data)/int(crossvalNum)) + " datapoints"
			print "  ---------------------------------------------------------------------------"

			plt.figure(figsize=(8,6), dpi=80)
			plt.title("Test Accuracy of KMeans within " + str(errorMargin) + " Margin")
			plt.xlabel("Crossvalidation Fold #")
			plt.ylabel("Average Accuracy Per Full Pass")
			plt.xticks(np.linspace(0,len(accuracy),len(accuracy)+1,endpoint=True))
			plt.plot(accuracy,color="green")
			plt.show()

		



			
