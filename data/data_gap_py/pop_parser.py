#!/usr/bin/env python3

import sys,math,operator,time,csv
from copy import deepcopy

startTime = time.time()

dic = {}

reader = csv.reader(open('pop.csv', 'rb'), quoting=csv.QUOTE_NONE)
reader2 = csv.reader(open('fert.csv', 'rb'), quoting=csv.QUOTE_NONE)

for index,line in enumerate(reader):
	if (line[2] == "15 - 19" or line[2] == "\"15 - 19\""):


		if line[3] != "" and line[3] != "0":
			newKey = (line[0],line[1])
			newVal = line[3]

			#print str(newKey) + ":" + str(newVal)

			dic[newKey] = newVal


for index,line in enumerate(reader2):
	key = (line[0],line[1])
	fert = line[2]

	try:
		fertVal = float(fert)

		if key in dic:
			popVal = float(dic[key])

			teenPregoBabyness = (fertVal / 1000) * popVal

			#for testing purposes
			#print "VALS: fertval=" + str(fertVal) + "; popval=" + str(popVal)

			print line[0] + "," + line[1] + "," + str(teenPregoBabyness)
	except: #fertility value is filled out as a non-numerical. cannot be used.
		pass
		#print line[0] + "," + line[1] + "," + "No data"

