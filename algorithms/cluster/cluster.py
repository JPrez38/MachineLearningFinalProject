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
	print "    --k #             Sets the number of clusters (default = 5)"
	print "    --components #    Sets num_components for PCA (default = 3)"
	print "    --outfile [file]  Gives program a file to output clustered data"
	print "-" * 64
	sys.exit()
#----------------------------------------------------------------------

#----------------------------------------------------------------------
def checkArgs():

	if len(sys.argv) < 2:
		printUsageAndExit("")

	try:
		reader = csv.reader(open(sys.argv[1], 'rU'), quoting=csv.QUOTE_NONE)
	except:
		printUsageAndExit("Error occured opening specified file")


	if "--k" in sys.argv:
		try:
			k = int(sys.argv[sys.argv.index("--k") + 1])
		except:
			printUsageAndExit("--k # must be an integer")
	else:
		k = 5

	if "--components" in sys.argv:
		try:
			components = int(sys.argv[sys.argv.index("--components")+1])
		except:
			printUsageAndExit("--components # must be an integer")
	else:
		components = 3

	if "--output" in sys.argv:
		try:
			outFile = open(sys.argv[sys.argv.index("--output")+1], 'w')
		except:
			printUsageAndExit("Error occured opening output file")
	else:
		outFile = ""

	print "Program Arguments"
	print "-" * 64
	print "Data File:        " + str(sys.argv[1])
	print "k =               " + str(k)
	print "num_components =  " + str(components)
	print "Outfile:          " + str(outFile)
	print "-" * 64

	return reader,k,components,outFile
#----------------------------------------------------------------------

#check and get args
reader,k,components,outFile = checkArgs()


print "Constructing data..."
keys,data,outs,actuals,pops,codes = sup.constructData(reader)
print " -> " + str(len(data)) + " vectors generated\n"

numpyData = np.array(data)
numpyOuts = np.array(outs)

pca = PCA(n_components=components)
reducedData = pca.fit_transform(numpyData)

fig = plt.figure()
ax = Axes3D(fig)

#for j in range(0,k):
ax.plot(reducedData[:,0],reducedData[:,1],reducedData[:,2],'o')
plt.title("Unclustered Reduced Data, Plotted by First 3 PCs")
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
plt.title(str(k) + "-Means Clustered Reduced Data, Plotted by First 2 PCs")
plt.show()


#3d plot
fig2 = plt.figure()
ax2 = Axes3D(fig2)
for j in range(k):
	ds = reducedData[np.where(labels==j)]
	ax2.plot(ds[:,0],ds[:,1],ds[:,2],'o')
lines = ax2.plot(centroids[:,0],centroids[:,1],centroids[:,2],'kx')
plt.setp(lines,ms=15.0)
plt.setp(lines,mew=2.0)
plt.title(str(k) + "-Means Clustered Reduced Data, Plotted by First 3 PCs")
plt.show()


#OUTPUTS
if "--output" in sys.argv:
	for dataKey,dataPoint,dataOut,dataLabel,code in zip(keys,data,outs,labels,codes):
		for key in dataKey:
			outFile.write(str(key) + ",")

		for val in dataPoint:
			outFile.write(str(val) + ",")

		outFile.write(str(dataOut) + ",")
		outFile.write(str(code) + ",")
		outFile.write(str(dataLabel) + "\n")