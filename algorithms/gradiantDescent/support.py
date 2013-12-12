#!/usr/bin/env python2.7

import sys,math,operator,time,csv
from copy import deepcopy

import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import matplotlib.offsetbox as offsetbox

class support(object):

	def __init__(self):
		pass

	#----------------------------------------------------------------------------------------------------
	def constructData(self,reader):
		keys = []
		data = []
		outs = []
		pops = []
		actuals = []

		for index,vec in enumerate(reader):
			if 'x' not in vec:
				keys.append((vec[0],vec[1]))
				data.append([int(vec[2]),int(vec[3]),float(vec[4]),float(vec[5]),float(vec[6]),float(vec[7]),float(vec[8]),float(vec[9]),float(vec[10]),float(vec[11]),float(vec[12]),float(vec[13])])
				outs.append(float(vec[16]))
				actuals.append(float(vec[14]))
				pops.append(int(vec[15]))

		return deepcopy(keys),deepcopy(data),deepcopy(outs),deepcopy(actuals),deepcopy(pops)
	#----------------------------------------------------------------------------------------------------

	#----------------------------------------------------------------------------------------------------
	def crunchTestResults(self,predictions,actuals,errorMargin):
		misses = 0
		totalError = 0
		totalErrorPercentile = 0

		#ERROR CALCULATION. CAN BE CHANGED! -------------------
		for prediction,actual in zip(predictions,actuals):
			margin = math.fabs(actual-prediction)
			if float(margin)/float(actual) > errorMargin:
				misses += 1
		#------------------------------------------------------
			totalError += margin
			totalErrorPercentile += float(margin)/float(actual)

		return misses,float(float(misses)/float(len(actuals))),totalError,totalErrorPercentile
	#----------------------------------------------------------------------------------------------------

	#----------------------------------------------------------------------------------------------------
	def writeOutputFile(self, keysTest, predictions, actuals, predictionsPop, actualsPop, info, outFile):
		#header
		outFile.write("KEY:Country,KEY:Year,Predicted,Actual,PredictedPopulation,ActualPopulation,ErrorPopulation,ErrorPercentile" + "\n")
		
		#test vectors
		for key,prediction,actual,predictionPop,actualPop in zip(keysTest,predictions,actuals,predictionsPop,actualsPop):
			outFile.write(str(key[0]) + "," + str(key[1]) + "," + str(prediction) + "," + str(actual) + "," + str(predictionPop) + "," + str(actualPop) + "," + str(math.fabs(predictionPop-actualPop)) + "," + str(float(math.fabs(prediction-actual))/float(actual)) + "\n")

		#average error
		outFile.write("\n\n,,,,,,Average Pop. Error,Average Percentile Error\n")
		outFile.write(",,,,,," + str(info[3]) + "," + str(info[4]) + "\n")

		#other info
		outFile.write("\n\n,,Algorithm Info\n")
		outFile.write("Algorithm:," + str(info[0]) + "\n")
		outFile.write("# Trained=," + str(info[1]) + "\n")
		outFile.write("# Tested=," + str(info[2]) + "\n")

		outFile.close()
	#----------------------------------------------------------------------------------------------------

	#----------------------------------------------------------------------------------------------------
	def normalize(self,trainData,testData):
		normTrainData = deepcopy(trainData)
		normTestData = deepcopy(testData)

		maxs = [0.0] * 12
		#find maximums
		for indexVector,vector in enumerate(normTrainData):
			for i in range(0,12):
				if vector[i] > maxs[i]:
					maxs[i] = normTrainData[indexVector][i]

		for testIndexVector,testVector in enumerate(normTestData):
			for k in range(0,12):
				if testVector[k] > maxs[k]:
					maxs[k] = normTestData[testIndexVector][k]

		#normalize
		for trainVecInd,trainVec in enumerate(normTrainData):
			for j in range(0,12):
				normTrainData[trainVecInd][j] /= maxs[j]

		for testVecInd,testVec in enumerate(normTestData):
			for l in range(0,12):
				normTestData[testVecInd][l] /= maxs[l]

		return deepcopy(normTrainData),deepcopy(normTestData),deepcopy(maxs)
				
	#----------------------------------------------------------------------------------------------------

	#----------------------------------------------------------------------------------------------------
	def normalize_crossval(self,data):
		normTrainData = deepcopy(data)

		maxs = [0.0] * 12
		#find maximums
		for indexVector,vector in enumerate(normTrainData):
			for i in range(0,12):
				if vector[i] > maxs[i]:
					maxs[i] = normTrainData[indexVector][i]

		#normalize
		for trainVecInd,trainVec in enumerate(normTrainData):
			for j in range(0,12):
				normTrainData[trainVecInd][j] /= maxs[j]

		return deepcopy(normTrainData),deepcopy(maxs)
	#----------------------------------------------------------------------------------------------------

	#----------------------------------------------------------------------------------------------------
	def convertPopVals(self, decimals, population):
		converts = []

		for decimal,pop in zip(decimals,population):
			converts.append(float(decimal * pop))

		return deepcopy(converts)
	#----------------------------------------------------------------------------------------------------

	#----------------------------------------------------------------------------------------------------
	def plot(self, points, xlabel, ylabel, title, legend, continuous):
		plt.figure(figsize=(8,6), dpi=80)
		plt.title(title)
		plt.xlabel(xlabel)
		plt.ylabel(ylabel)
		if continuous:
			plt.plot(points, color="blue")
		else:
			plt.plot(points,'ro')
		plt.show()
		return
	#----------------------------------------------------------------------------------------------------