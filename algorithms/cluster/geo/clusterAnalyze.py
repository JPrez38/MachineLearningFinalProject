#!/usr/bin/env python2.7

import sys,math,operator,time,csv
from copy import deepcopy

import numpy as np
import scipy as sp

import matplotlib.pyplot as plt

import support
sup = support.GeoSupport()

#-------------------------------------------------------------------------------------
def printUsageAndExit(error):
	print "-" * 64
	if error != "":
		print "ArgumentError: " + str(error)

	print "Usage: clusterAnalyze.py [clustered output] [options (optional)]"
	print "  Options:"
	print "    "
	print "-" * 64
	sys.exit()
#-------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------
def checkArgs():
	if len(sys.argv) < 2:
		printUsageAndExit("Your arguments are inadequate. And you are an asshole.")

	try:
		reader = csv.reader(open(sys.argv[1], 'rU'), quoting=csv.QUOTE_NONE)
	except:
		printUsageAndExit("Neoope. That file aint right, brah.")

	return reader
#-------------------------------------------------------------------------------------

#get arguments
reader = checkArgs()

data,clusters = sup.constructData(reader)

npData = np.array(data)

infoCountryCluster = []

for clusterID in clusters:
	infoCountryCluster.append([0] * 9)

for index,datapoint in enumerate(data):
	infoCountryCluster[int(datapoint[4])][int(datapoint[3])] += 1

for clusterID in range(0,len(clusters)):
	print "-" * 64
	print "Cluster ID: " + str(int(clusterID))
	for countryID in range(0,9):
		print "  " + str(sup.codeToCountry(countryID)) + ": " + str(infoCountryCluster[int(clusterID)][countryID])

	#pie chart'n'shit
	plt.figure(1,figsize=(6,6))
	labels = ['North America','Central America','South America','Western Europe','Eastern Europe','Africa','Middle East','Asia','South East Asia']
	fracs = infoCountryCluster[clusterID]

	#trim dat shit
	for index,num in enumerate(fracs):
		if num == 0:
			del fracs[index]
			del labels[index]

	plt.pie(fracs,labels=labels,startangle=90)
	plt.title("Fractions of Countries in Cluster " + str(clusterID + 1))
	plt.show()