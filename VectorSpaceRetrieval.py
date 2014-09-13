from Utilities import Utilities
from time import time ,clock
import math	
from datetime import datetime
from time import gmtime, strftime
from collections import OrderedDict
from scipy.sparse import coo_matrix

class VectorSpaceRetrieval:
	
	termFrequencyDictOfCorpus={}
	orderingDictOfTerms={}
	corpusSize=0
	docDictWithText={}
	
	def __init__(self):
		print "Initializing Vector Space retrieval"
	
	def getWeightedTFIDFDict(self,termFrequencyDict,idfDict):
		for term in termFrequencyDict:
			if term in idfDict:
				idfOfTerm = idfDict[term]
				for docId in termFrequencyDict[term]:
					termFrequencyDict[term][docId]=   (1.0+math.log((termFrequencyDict[term][docId]),2) )*   idfOfTerm
			#when the query is here			
			else:
				termFrequencyDict[term][0]=0.0
				
		return termFrequencyDict
		
	
	def getDataForTermDocMatrix(self,weightedtermFreqDict):
		rowTerm=[]
		columnDocument=[]
		data=[]
		termIndex=0
		euclideanNormalizedDict={}
		for term in weightedtermFreqDict:
			for docId in weightedtermFreqDict[term]:
				if weightedtermFreqDict[term][docId] !=0.0:
					if docId in euclideanNormalizedDict:
						euclideanNormalizedDict[docId] = euclideanNormalizedDict[docId] + weightedtermFreqDict[term][docId]**2
					else:
						euclideanNormalizedDict[docId] = weightedtermFreqDict[term][docId]**2
					
			termIndex+=1
		
		for docId in euclideanNormalizedDict:
			euclideanNormalizedDict[docId] = math.sqrt(euclideanNormalizedDict[docId] )
		
		termIndex=0
		for term in weightedtermFreqDict:
			for docId in weightedtermFreqDict[term]:
				if weightedtermFreqDict[term][docId] !=0.0:
					rowTerm.append(termIndex)
					columnDocument.append(docId)
					data.append(weightedtermFreqDict[term][docId]/euclideanNormalizedDict[docId])
			termIndex+=1
		
		return (rowTerm,columnDocument,data, euclideanNormalizedDict)
		
	
	def buildPreProcessedData(self,filePath):
		utilityObj = Utilities()
		tupleOfDictionariesAndCorpusSize=utilityObj.readTweetsAndConstructDocDictionary(filePath)
		self.corpusSize = tupleOfDictionariesAndCorpusSize[2]
		self.docDictWithText = tupleOfDictionariesAndCorpusSize[3]
		termDocMatrixFromTweets = self.constructTermDocumentMatrix(tupleOfDictionariesAndCorpusSize)
		return termDocMatrixFromTweets
		
	
	def getSearchResult(self,userQuery,termDocMatrix,vectorRetrievalObjWithPreProcessedData):
		utilityObj = Utilities()
		searchRes={}
		dictQuery={}
		tupleOfDictionariesAndCorpusSize=utilityObj.readQueryAndConstructQueryDictionary([userQuery])
		corpusSize = tupleOfDictionariesAndCorpusSize[2]
		termFreqDictOfQuery = tupleOfDictionariesAndCorpusSize[0]
		sortedTermFreqDictOfQuery = OrderedDict(sorted(termFreqDictOfQuery.items(), key=lambda t: t[0]))
		
		idfDict = tupleOfDictionariesAndCorpusSize[1]
		queryDocMatrix= self.constructTermDocumentMatrix(tupleOfDictionariesAndCorpusSize)
		for index  in range(len(sortedTermFreqDictOfQuery)):
			term = sortedTermFreqDictOfQuery.keys()[index]
			dictQuery[term]=queryDocMatrix[index,0]
			
		cosineSimilarityResult={}
		indexOfQueryTermsInCorpusDict=[]
		
		for i in range(vectorRetrievalObjWithPreProcessedData.corpusSize):
			tempRes=0
			for term  in dictQuery:
				if term in vectorRetrievalObjWithPreProcessedData.termFrequencyDictOfCorpus:
					indexOfTermInSortedCorpusTerms = self.orderingDictOfTerms[term]
					tempRes += termDocMatrix[indexOfTermInSortedCorpusTerms,i] * dictQuery[term]
				
					
			if tempRes>0:
				cosineSimilarityResult[i] = tempRes
			
		sortedResult=sorted(cosineSimilarityResult.items(), key=lambda x: x[1], reverse=True)
			
		if len(cosineSimilarityResult)>50:
			searchRes=sortedResult[0:50]
		else:
			searchRes = sortedResult
			
		return (searchRes,vectorRetrievalObjWithPreProcessedData.docDictWithText,cosineSimilarityResult,sortedResult)
				

		
	def getCosineScoreBetweenDocAndQuery(self,colIndex,columnOfCorpus,dictQuery,vectorRetrievalObjWithPreProcessedData):
		result=0
		for term in dictQuery:
			if term in vectorRetrievalObjWithPreProcessedData.termFrequencyDictOfCorpus:
				indexOfTermInSortedCorpusTerms = (vectorRetrievalObjWithPreProcessedData.termFrequencyDictOfCorpus).keys().index(term)
				result+= columnOfCorpus[indexOfTermInSortedCorpusTerms,0]*dictQuery[term]
			else:
				result =0
				return result
		return result
			
	def constructTermDocumentMatrix(self,tupleOfDictionariesAndCorpusSize):
		
		euclideanNormalizedList=[]
		
		termFreqDict = tupleOfDictionariesAndCorpusSize[0]
		idfDict = tupleOfDictionariesAndCorpusSize[1]
		sortedTermFreqDict = OrderedDict(sorted(termFreqDict.items(), key=lambda t: t[0]))
		corpusSize = tupleOfDictionariesAndCorpusSize[2]
		if corpusSize>1:
			self.termFrequencyDictOfCorpus= sortedTermFreqDict
			index=0
			for term in sortedTermFreqDict:
				self.orderingDictOfTerms[term]=index
				index+=1
		
		weightedTermFrequencyIDFDict = self.getWeightedTFIDFDict(sortedTermFreqDict,idfDict)
		tupleOfDataForMatrix= self.getDataForTermDocMatrix(weightedTermFrequencyIDFDict)
		rowList = tupleOfDataForMatrix[0]
		colList = tupleOfDataForMatrix[1]
		dataList= tupleOfDataForMatrix[2]
		termDocumentMatrix =coo_matrix(   (dataList,(rowList,colList)), shape = ( len(weightedTermFrequencyIDFDict),corpusSize   ))
		lilTermDocMatrix= termDocumentMatrix.tolil()
		
		return lilTermDocMatrix
		
