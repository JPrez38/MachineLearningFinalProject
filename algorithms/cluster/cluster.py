import sys,math,operator,time,csv
from copy import deepcopy

import numpy as np
import scipy as sp

import matplotlib.pyplot as plt
import matplotlib.offsetbox as offsetbox
from mpl_toolkits.mplot3d import Axes3D

from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import scale

import support

sup = support.support()

#----------------------------------------------------------------------
def printUsageAndExit(error):
	print "-" * 64
	print "ARGUMENT ERROR: " + str(error)
	print "Usage: kmeans.py [dataFile] [options (optional)]"
	print "  Options:"
	print "    --k #           Sets the number of clusters (default = 5)"
	print "-" * 64
	sys.exit()
#----------------------------------------------------------------------

#----------------------------------------------------------------------
def checkArgs():

	if len(sys.argv) < 2:
		printUsageAndExit("")

	try:
		reader = csv.reader(open(sys.argv[1], 'rb'), quoting=csv.QUOTE_NONE)
	except:
		printUsageAndExit("Error occured opening specified file")


	if "--k" in sys.argv:
		try:
			k = int(sys.argv[sys.argv.index("--k") + 1])
		except:
			printUsageAndExit("--k # must be an integer")
	else:
		k = 5

	print "Program Arguments"
	print "-" * 64
	print "Data File:        " + str(sys.argv[1])
	print "k =               " + str(k)
	print "-" * 64

	return reader,k
#----------------------------------------------------------------------

#check and get args
reader,k = checkArgs()


print "Constructing data..."
keys,data,outs,actuals,pops = sup.constructData(reader)
print " -> " + str(len(data)) + " vectors generated\n"

numpyData = np.array(data)

pca = PCA(n_components=3)
reducedData = pca.fit_transform(numpyData)

print reducedData

fig = plt.figure()
ax = Axes3D(fig)

#for j in range(0,k):
ax.plot(reducedData[:,0],reducedData[:,1],reducedData[:,2],'o')
plt.show()


kmeans = KMeans(n_clusters=k)
kmeans.fit(reducedData)

labels = kmeans.labels_
centroids = kmeans.cluster_centers_

#2d plot
for i in range(k):
	ds = reducedData[np.where(labels==i)]
	plt.plot(ds[:,0],ds[:,1],'o')
	lines = plt.plot(centroids[i,0],centroids[i,1],'kx')
	plt.setp(lines,ms=15.0)
	plt.setp(lines,mew=2.0)

plt.show()


#3d plot
fig2 = plt.figure()
ax2 = Axes3D*(fig2)

