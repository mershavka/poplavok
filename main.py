import csv

def appendRowToCsv(filename, listOfElements):
	with open(filename, 'a+', newline ='') as writeObj:
		writer = csv.writer(writeObj)
		writer.writerow(listOfElements)
