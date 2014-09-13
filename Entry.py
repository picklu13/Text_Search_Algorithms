from VectorSpaceRetrieval import VectorSpaceRetrieval
from Integrated import Integrated
from PageRank import PageRank
from TaggedPageRank import TaggedPageRank
import sys 
import os.path
from time import time ,clock
from time import gmtime, strftime
from collections import OrderedDict
from curses.ascii import SO
try:
    import cPickle as pickle
except:
    import pickle


PAGE_RANK_SORTED = "pageRankDict.pkl"
CORPUS_ADJACENCY_LIST= "corpusAdjacencyList.pkl"
USER_DICT_INDEX_AS_KEY ="userDictWithIndexAsKey.pkl"
USER_DICT_NAME_AS_KEY= "userDictWithNameAsKey.pkl"
SORTED_PAGE_RANK = "sortedPageRankList.pkl"




def main():

	if len(sys.argv)!=2:
		print len(sys.argv)
		print ("usage: ./Entry.py corpusFilePath")
		sys.exit(1)	
	corpusFile = sys.argv[1]
	vectorRetrievalObjWithPreProcessedData = VectorSpaceRetrieval()
	start = time()
	termDocMatrix= vectorRetrievalObjWithPreProcessedData.buildPreProcessedData(corpusFile)
	elapsed= time()-start
	print "Vector Space Constructed in ",elapsed ," seconds"
	
	choice=0
	options = 	{	'1':vectorRetrieval,	'2':pageRankedRetrieval	,'3': integrated, '4':exit ,'5' :taggedPageRank }
		
	while(True):
		
		print ("1. Vector Space retrieval ")
		print ("2. Page Ranked Retrieval ")
		print ("3. Integrated Ranking System")
		print ("4. Exit")
		print ("5. Tagged Page Rank")
		
		choice = raw_input("Select Your  Option  [1/2/3/4/5]")
		if choice not in ["1","2","3","5"]:
			choice ='4'
			options[choice]()
		
		elif choice=='1':
			options[choice](termDocMatrix,vectorRetrievalObjWithPreProcessedData)
		elif choice=='2':
			options[choice](corpusFile)
		elif choice=='3':
			options[choice](termDocMatrix,vectorRetrievalObjWithPreProcessedData,corpusFile)
		elif choice=='5':
			options[choice](corpusFile)
		
			


def vectorRetrieval(termDocMatrix,vectorRetrievalObjWithPreProcessedData):
	userQuery = raw_input("Enter the Query: ")
	print "you entered  ", userQuery
	print "Starting Search"
	vectorRetObj= VectorSpaceRetrieval()
	start = time()
	rankedResultTuple= vectorRetObj.getSearchResult(userQuery,termDocMatrix,vectorRetrievalObjWithPreProcessedData)
	rankedResult = rankedResultTuple[0]
	dictionaryOfTweets =rankedResultTuple[1]
	cosineSimilarityResult = rankedResultTuple[2]
	elapsed = (time() - start)
	if len(rankedResult)==0:
		print "No Matching Tweet"
	else:
		rank=1
		for resultTuple in rankedResult:
			print "Rank ",rank
			print "DocID : ",resultTuple[0]
			print "Similarity Score ", resultTuple[1]
			print "Tweet Text : " ,dictionaryOfTweets[resultTuple[0]] [0]
			rank+=1
			print "*"*5


def writeToFilePickle(fileName,object):
	output = open(fileName, 'wb')

# Pickle dictionary using protocol 0.
	pickle.dump(object, output)
	

def pageRankedRetrieval(corpusFile):
	#do something
	if os.path.exists(PAGE_RANK_SORTED)  and os.path.exists(USER_DICT_INDEX_AS_KEY):
		pklSteadyDict = open(PAGE_RANK_SORTED, 'rb')
		sortedSteadyDict = pickle.load(pklSteadyDict)
		pklUserMap =open(USER_DICT_INDEX_AS_KEY, 'rb')
		userIdMap = pickle.load(pklUserMap)
	else:
		pageRankObj = PageRank()
		tupleOfDicts =pageRankObj.constructPageRanks(corpusFile)
		steadyStateDict= tupleOfDicts[0]
		userIdMap = tupleOfDicts[1]
		userRefDictionary = tupleOfDicts[2]
		sortedSteadyDict = OrderedDict(sorted(steadyStateDict.items(), key=lambda t: t[1], reverse =True))
		writeToFilePickle(PAGE_RANK_SORTED, sortedSteadyDict)
		writeToFilePickle(USER_DICT_INDEX_AS_KEY, userIdMap)
		writeToFilePickle(CORPUS_ADJACENCY_LIST, userRefDictionary)
	
	
	index =1
	for userId in sortedSteadyDict:
		print "*"*5
		print "Rank ",index
		print "User ID " ,userId
		if userId in userIdMap:
			print "Name ", userIdMap[userId]
		else:
			print "Name ",""
		index +=1
		if index >=51:
			break
	
def printPageRankResults(dictionary,userIdMap):
	index =1
	for userId in dictionary:
		print "*"*5
		print "Rank ",index
		print "User ID " ,userId
		if userId in userIdMap:
			print "Name ", userIdMap[userId]
		else:
			print "Name ",""
		index +=1
		if index >=51:
			break


def integrated(termDocMatrix,vectorRetrievalObjWithPreProcessedData,corpusFile):
	userQuery = raw_input("Enter the Query: ")
	print "you   ", userQuery
	print "Starting Search"
	vectorRetObj= VectorSpaceRetrieval()
	start = time()
	rankedResultTuple= vectorRetObj.getSearchResult(userQuery,termDocMatrix,vectorRetrievalObjWithPreProcessedData)
	rankedResult = rankedResultTuple[0]
	dictionaryOfTweets =rankedResultTuple[1]
	cosineSimilarityResult = rankedResultTuple[2]
	allSortedResultTupleList = rankedResultTuple[3]
	
	if os.path.exists(PAGE_RANK_SORTED)  and os.path.exists(USER_DICT_INDEX_AS_KEY):
		pklSteadyDict = open(PAGE_RANK_SORTED, 'rb')
		sortedSteadyDict = pickle.load(pklSteadyDict)
		pklUserMap =open(USER_DICT_INDEX_AS_KEY, 'rb')
		userIdMap = pickle.load(pklUserMap)
		
		
	else:
		pageRankObj = PageRank()
		tupleOfDicts =pageRankObj.constructPageRanks(corpusFile)
		steadyStateDict= tupleOfDicts[0]
		userIdMap = tupleOfDicts[1]
		sortedSteadyDict = OrderedDict(sorted(steadyStateDict.items(), key=lambda t: t[1], reverse =True))
		writeToFilePickle(PAGE_RANK_SORTED, sortedSteadyDict)
		writeToFilePickle(USER_DICT_INDEX_AS_KEY, userIdMap)
	
	
	
	
	integratedSearchObj = Integrated()
	finalScoreDictWithDocIdIndexed= integratedSearchObj.getSearchResult(cosineSimilarityResult,
									allSortedResultTupleList,
									dictionaryOfTweets,
									sortedSteadyDict,
									userIdMap,
									)
	sortedDict = OrderedDict(sorted(finalScoreDictWithDocIdIndexed.items(), key=lambda t: t[1], reverse =True))
	i =1
	for docId in sortedDict:
		print "*"*5
		score = finalScoreDictWithDocIdIndexed[docId]
		print "Text :", dictionaryOfTweets[docId][0]
		print "Tweeter ID : ",dictionaryOfTweets[docId][1]
		if (dictionaryOfTweets[docId][1] in userIdMap):
			print "Tweeter Name ",userIdMap[dictionaryOfTweets[docId][1]]
		else:
			print "Tweeter Name ",""
		i+=1
		if i>=51:
			break
	
def taggedPageRank(corpusFile):
	taggedPageRankObj = TaggedPageRank()
	pageRankObj = PageRank()
	corpusAdjacencyList={}
	userIdMap={}
	if os.path.exists(CORPUS_ADJACENCY_LIST):
		pklAdjacencyList  = open(CORPUS_ADJACENCY_LIST, 'rb')
		corpusAdjacencyList = pickle.load(pklAdjacencyList)
	if os.path.exists(USER_DICT_INDEX_AS_KEY):
		pklUserMap =open(USER_DICT_INDEX_AS_KEY, 'rb')
		userIdMap = pickle.load(pklUserMap)
		
	masterDict = 	taggedPageRankObj.taggedPageRankUsers(corpusFile,corpusAdjacencyList)
	for tag in masterDict:
		print "Calculating Page Rank for Tag:",tag
		steadyDict = pageRankObj.constructPageRankFromAdjacencyList(masterDict[tag])
		sortedSteadyDict = OrderedDict(sorted(steadyDict.items(), key=lambda t: t[1], reverse =True))
		printPageRankResults(sortedSteadyDict, userIdMap)
		
		
	


if __name__ == '__main__':
	main()