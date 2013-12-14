#!/usr/bin/env python2.7

import sys,math,operator,time,csv
import random as rand
from copy import deepcopy

startTime = time.time()

#-----------------------------------------------------------------------------------------------------
def printUsageAndExit():
	print "Usage: makeData.py [fullFile] [trainFile] [testFile] [options (optional)]"
	print "  Options:"
	print "    --test-size #               The size of the generated testing set (default 300)"
	print "    --random                    Will take vectors at random"
	print "    --byyear 				   Cuts item by year"
	sys.exit()
#-----------------------------------------------------------------------------------------------------

if len(sys.argv) < 4: 
	printUsageAndExit()

try:
	reader = csv.reader(open(sys.argv[1], 'rU'), quoting=csv.QUOTE_NONE)
	trainFile = open(sys.argv[2],'w')
	testFile = open(sys.argv[3],'w')
except:
	printUsageAndExit()

if "--test-size" in sys.argv:
	try:
		testSize = int(sys.argv[sys.argv.index("--test-size")+1])
	except:
		printUsageAndExit()
else:
	testSize = 300

random = True if "--random" in sys.argv else False


byyear = False	
if "--byyear" in sys.argv:
	byyear = True
	try:
		splityear = int(sys.argv[sys.argv.index("--byyear")+1])
	except:
		printUsageAndExit()
else:
	splityear = 2000


#------------------------------------------------------------------------------------------------------
def constructData(reader):
	data = []

	for index,line in enumerate(reader):
		data.append(line)

	return deepcopy(data)
#------------------------------------------------------------------------------------------------------

def randombuild():
	i=0
	while i < testSize:
		randIndex = rand.randint(0,len(data)-1)
		if randIndex not in testVectorIndicesInOriginalData:
			testData.append(data[randIndex])
			testVectorIndicesInOriginalData.append(randIndex)
			testFile.write(','.join(str(feature) for feature in data[randIndex]) + "\n")
			i+=1
		else:
			continue

	#write remaining to training testFile
	for k in range(0,len(data)):
		if k not in testVectorIndicesInOriginalData:
			trainFile.write(','.join(str(feature) for feature in data[k]) + "\n")

	trainFile.close()
	testFile.close()

def yearbuild():
	for i,pt in enumerate(data):
		if int(pt[1]) > splityear:
			testData.append(data[i])
			testVectorIndicesInOriginalData.append(i)
			testFile.write(','.join(str(feature) for feature in data[i]) + "\n")

	#write remaining to training testFile
	for k in range(0,len(data)):
		if k not in testVectorIndicesInOriginalData:
			trainFile.write(','.join(str(feature) for feature in data[k]) + "\n")

	trainFile.close()
	testFile.close()

data = constructData(reader)
trainingData = []
testData = []

testVectorIndicesInOriginalData = []

#build test data
if byyear:
	yearbuild()

else:
	randombuild()


