import sys,math,cmath,operator,time,csv
from copy import deepcopy

t0 = time.time()

if len(sys.argv) != 2: #check args
	print "Usage: append.py [file]"
	sys.exit()

reader = csv.reader(open(sys.argv[1], 'rb'), quoting=csv.QUOTE_NONE)


numFilled = 0
for index,line in enumerate(reader):
	if line[14] != 'x':
		numFilled += 1

print "File contains " + str(numFilled) + " filled birth rates."
