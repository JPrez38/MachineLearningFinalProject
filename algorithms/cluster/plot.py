#!/usr/bin/env python2.7

import sys,math,operator,time,csv
from copy import deepcopy

from sklearn import linear_model
from sklearn import preprocessing
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import matplotlib.offsetbox as offsetbox

import support

startTime = time.time()

#support object
sup = support.support()

#-----------------------------------------------------------------------------------------------------
def printUsageAndExit():
	print "Usage: plot.py [dataFile] [options (optional)]"
	print "  Options:"
	print "   --features #1 #2          Will be used as x-coord,y-coord (default: 2 highest weighted)"
	#print "   --test-all                Will generate a plot for ALL possible feature combos"
	#print "   --predictions [file]      Will take file as input for predictions"
	#print "       --with-predict-error  Will plot with different marker based on error"
	#print "       --with-predictions    Will plot each point with it's prediction from file"
	sys.exit()
#-----------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------
def checkArgs():
	if len(sys.argv) < 2:
		printUsageAndExit()


	print "Program Arguments"
	print "-" * 64
	try:
		dataReader = csv.reader(open(sys.argv[1], 'rb'), quoting=csv.QUOTE_NONE)
		print "Data File:               " + sys.argv[1]
	except:
		printUsageAndExit()

	if "--features" in sys.argv:
		try:
			useFeatureAsX = int(sys.argv[sys.argv.index("--features") + 1])
			useFeatureAsY = int(sys.argv[sys.argv.index("--features") + 2])
			print "Features:                " + str(useFeatureAsX) + "," + str(useFeatureAsY)
		except:
			printUsageAndExit()
	elif "--test-all" in sys.argv:
		print "Testing all feature combos!"
	else:
		useFeatureAsX = ""
		useFeatureAsY = ""
		print "Compute weight vector and use 2 largest weights"

	if "--predictions" in sys.argv:
		try:
			predictReader = csv.reader(open(sys.argv[sys.argv.index("--predictions") + 1]))
			print "Prediction File:         " + sys.argv[sys.argv.index("--predictions") + 1]
		except:
			printUsageAndExit()

		
		if "--with-predict-error" in sys.argv:
			showError = True
		else:
			showError = False
		print "Show Errors in Plot?     " + str(showError)
	else:
		predictReader = ""
		showError = False

	print "-" * 64

	return dataReader,useFeatureAsX,useFeatureAsY,predictReader,showError
#-----------------------------------------------------------------------------------------------------


#get/check args
dataReader,useFeatureAsX,useFeatureAsY,predictReader,showError = checkArgs()

keys,data,outs,actuals,pops = sup.constructData(dataReader)

if "--features" not in sys.argv:
	#train a bayes ridge regression and get the feature weights
	model = linear_model.BayesianRidge()
	model.fit(data,outs)

	weights = deepcopy(model.coef_)

	weights = np.absolute(weights)
	useFeatureAsX = np.where(weights == max(weights))[0][0]
	weights[useFeatureAsX] = 0
	useFeatureAsY = np.where(weights == max(weights))[0][0]

print "x,y features: " + str(useFeatureAsX) + "," + str(useFeatureAsY)

#get all x and y coords
xCoords = []
yCoords = []

print "Plotting " + str(len(data)) + " points..."


labels = ["Minimum age of marriage without parental consent (Female)","Minimum age of marriage without parental consent (Male)","Literacy Rate (Female)","Literacy Rate (Male)","Contraceptive Prevalence (Modern)","Contraceptive Prevalence (Any)","Marriage Percentages (Female)","Marriage Percentages (Male)","Mean Marriage Age (Female)","Mean Marriage Age (Male)","Share of Labor Force (Women)","Gender Ratio"]

for index,point in enumerate(data):
	xCoords.append(data[index][useFeatureAsX])
	yCoords.append(data[index][useFeatureAsY])

#plotting time, baby! wooohooo!
plt.figure(figsize=(8,6), dpi=80)
plt.title("Datapoints Plotted")
plt.xlabel(labels[useFeatureAsX])
plt.ylabel(labels[useFeatureAsY])
plt.plot(xCoords,yCoords,'ro')
plt.show()