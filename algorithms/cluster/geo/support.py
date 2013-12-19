#!/usr/bin/env python2.7

import sys,math,operator,time,csv
from copy import deepcopy

import numpy as np
import scipy as sp

class GeoSupport(object):

	def __init__(self):
		pass

	#--------------------------------------------------------------------------------------------
	def codeToCountry(self, code):
		codeDict = {0 : 'North America',
			1 : 'Central America',
			2 : 'South America',
			3 : 'Western Europe',
			4 : 'Eastern Europe',
			5 : 'Africa',
			6 : 'Middle East',
			7 : 'Asia',
			8 : 'South East Asia'
		}

		return codeDict[code]
	#--------------------------------------------------------------------------------------------

	#--------------------------------------------------------------------------------------------
	def constructData(self, reader):
		data = []

		# Data organization:
		# Each country is an array within the data array that looks like:
		# [[country, year], [features,...], actual percentile, geo code, cluster id]

		cluster = []

		for i,vec in enumerate(reader):
			if 'x' not in vec:
				datapoint = []

				datapoint.append([vec[0],vec[1]])
				datapoint.append([vec[2],vec[3],vec[4],vec[5],vec[6],vec[7],vec[8],vec[9],vec[10],vec[11],vec[12],vec[13]])
				datapoint.append(vec[14]) #output
				datapoint.append(vec[15]) #country code
				datapoint.append(vec[16]) #clusterID

				if vec[16] not in cluster:
					cluster.append(vec[16])

				data.append(datapoint)

		return deepcopy(data),deepcopy(cluster)
	#--------------------------------------------------------------------------------------------