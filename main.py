import datetime as dt
import time
import csv
from driver import Driver
import traceback
from threading import Thread

def appendRowToCsv(filename, listOfElements):
	with open(filename, 'a+', newline ='') as writeObj:
		writer = csv.writer(writeObj)
		writer.writerow(listOfElements)



def runExpCal1():
	pass

def runExpCal2():
	pass