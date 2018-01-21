import os
import sys
import io

sys.path.append(os.path.abspath("tools"))




def readListOfLists(inFile,separator=";",firstLinesToIgnore=1,lastEltsToIgnore =1):
	toReturn =[]
	in_file = open(inFile, 'r')
	for line in in_file.readlines()[firstLinesToIgnore:]:
		# print line
		elts = line[:(0 - lastEltsToIgnore)].split(separator)
		toReturn.append(elts)


	return toReturn

def readListOfPairs(inFile,separator=";",firstLinesToIgnore=1,lastEltsToIgnore =1,asFloat=False):
	toReturn =[]
	in_file = open(inFile, 'r')
	for line in in_file.readlines()[firstLinesToIgnore:]:
		# print line
		elts = line[:(0 - lastEltsToIgnore)].split(separator)
		if asFloat:
			toReturn.append((elts[0],float(elts[1])))
		else:
			toReturn.append((elts[0],elts[1]))


	return toReturn

def readCSVasDicOftab(inFile,firstLinesToIgnore=1,lastEltsToIgnore =1,separator=";",asFloat=False):
	dico = {}
	in_file = open(inFile, 'r')
	nbElts = -1
	for line in in_file.readlines()[firstLinesToIgnore:]:
		#print line
		elts = line[:(0-lastEltsToIgnore)].split(separator)
		if elts[0] in dico:
			print("error, key "+elts[0]+" present several times")
		dico[elts[0]] = elts[1:]
		if asFloat:
			dico[elts[0]] = [float(x) for x in dico[elts[0]]]
	return dico

def createParentDirIfNotExist(aFile):
	if not os.path.exists(os.path.dirname(aFile)):
		try:
			os.makedirs(os.path.dirname(aFile))
		except OSError as exc: # Guard against race condition
			#if exc.errno != errno.EEXIST:
				raise
	
def readDictionary(file,firstLinesToIgnore=1,lastEltsToIgnore =1,separator=";",asFloat=True):
	dico = {}
	in_file = open(file, 'r')
	for line in in_file.readlines()[firstLinesToIgnore:]:
		#print line
		elts = line[:0-lastEltsToIgnore].split(separator)
		dico[elts[0]] = elts[1]
	 
	#transform all strings in numbers for lines
	if asFloat:

		for key in dico:
			dico[key] = float(dico[key])
	return dico


def printDictionaryDisplay(dictionary):
	for key in dictionary:
		print (str(key)+"\t"+str(dictionary[key]))

def writeDictionary(dictionary,theFile,header=True,hTitle="value"):
	printDictionary(dictionary, theFile, header=header, hTitle=hTitle)

def tabAsString(tab):
	toW=""
	for el in tab:
		toW += str(el)+"\t"
	toW=toW[:-1]
	return toW


def printDictionary(dictionary,theFile,header=False,hTitle="value"):
	createParentDirIfNotExist(theFile)
	out_file = open(theFile, 'w')
	if header:
		out_file.write("key\t"+hTitle+"\n")
	
	for key in dictionary:
		toW = str(key)
		for el in dictionary[key]:
			toW += "\t" + str(el)
		out_file.write(toW+"\n")
	out_file.close()

def read3files(dirOfFiles):
	INs = readDictionary(dirOfFiles+"/IN.txt")
	OUTs = readDictionary(dirOfFiles+"/OUT.txt")
	flows = readDictionary(dirOfFiles+"/flow.txt")
	return (INs,OUTs,flows)

def printArrayOfArrays(toPrint,separator="\t"):
	for tuple in toPrint:
		toW = ""
		for i in range(len(tuple)):
			toW += str(tuple[i])+separator
		#print toW
		toW = toW[:-1]
		#print toW
		print(toW)

def writeArrayOfArrays(toPrint,file,separator="\t"):
	createParentDirIfNotExist(file)
	out_file = open(file, 'w')
	for tuple in toPrint:
		toW = ""
		for i in range(len(tuple)):
			toW += str(tuple[i])+separator
		#print toW
		toW = toW[:-1]
		#print toW
		out_file.write(toW+"\n")
	out_file.close()

def writeDicOfArray(toPrint,file,separator="\t",header=False,hTitle="TITLE"):
	print("writing file at "+file)
	createParentDirIfNotExist(file)
	out_file = open(file, 'w')
	if header:
		out_file.write("key\t" + hTitle + "\n")

	for k in toPrint.keys():
		toW = k
		for el in toPrint[k]:
			toW+=separator+str(el)
		out_file.write(toW+"\n")
	out_file.close()

def printDicOfArray(toPrint,separator="\t"):
	for k in toPrint.keys():
		toW = str(k)
		for el in toPrint[k]:
			toW+=separator+str(el)
		print (toW)

thresholdRatioToPrint= 0.5

def printArray(toPrint,separator="\t"):
		print (stringFromArray(toPrint,separator="\t"))

def stringFromArray(toPrint, separator="\t"):
	toW = ""
	for el in toPrint:
		toW += separator + str(el)
	return toW
