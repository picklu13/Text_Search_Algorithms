from math import log
from datetime import datetime
from time import gmtime, strftime
from pprint import pprint
from sets import Set
import collections
import json
import math
import re



class Utilities:
	
	TWEET_FILENAME="mars_tweets_small.json"
	invertedDocFrequencyDict={}
	
	def __init_(self):
		print "initializing utiities"
		
		
		
	def readQueryAndConstructQueryDictionary(self,userQuery):
		tupleObtained =self.performTfIdfCalculations(userQuery, False)
		return  tupleObtained
		
	def performTfIdfCalculations(self,lines,isJson):
		docDict={}
		
		termAppearanceDict={}
		termFrequencyDict={}
		docID=0
		for line in lines:
			if(isJson):
				data = json.loads(line)
				docDict[docID]=(data['text'],data['user']['id'])
				listOfWords = re.findall(r"[\w]+", data['text'].lower())
			else:
				listOfWords = line.split()
			for word in listOfWords:
				if word in termAppearanceDict:
					termAppearanceDict[word].add(docID)
					termFreqSubDict = termFrequencyDict[word]
					if docID in termFreqSubDict:
						termFrequencyDict[word][docID]+=1
					else:
						termFrequencyDict[word][docID]=1
				else:
					termAppearanceDict[word]=Set([docID])
					termFrequencyDict[word]={docID:1}
					
			docID+=1
		
		totalCorpusSize= docID
		
		
		if  isJson:
			for key in termAppearanceDict:
				docFrequency = len(termAppearanceDict[key])
				num = totalCorpusSize/float(docFrequency)
				idf = math.log(num,2)  
				self.invertedDocFrequencyDict[key]= idf
			
		return  (termFrequencyDict,self.invertedDocFrequencyDict,totalCorpusSize,docDict)

		
	def readTweetsAndConstructDocDictionary(self,filePath):
		lines = [line.strip() for line in open(filePath)]
		tupleObtained =self.performTfIdfCalculations(lines,True)
		
		return tupleObtained 
		
		
		