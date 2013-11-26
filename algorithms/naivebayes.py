#!/usr/bin/env python2.7

import sys,math,operator,time,csv
from copy import deepcopy

startTime = time.time()

dic = {}

reader = csv.reader(open('pop.csv', 'rb'), quoting=csv.QUOTE_NONE)