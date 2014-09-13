
class Integrated:
	def __init__(self):
		print "Initializing integrated"
		
	def getSearchResult(self,cosineSimilarityResult,allSortedResultTupleList,dictionaryOfTweets,pageRankDictSorted,userIdMap):
		
		finalScoreOfDocumentAndTweeterDict={}
		scoredPageRankDict={}
		dictOfDocWithScaledScore={}
		highestCosineSimilarityScore = allSortedResultTupleList[0][1]
		scalingFactorCosine = 1.0/highestCosineSimilarityScore
		for entry in allSortedResultTupleList:
			dictOfDocWithScaledScore [entry[0]] = entry[1]*scalingFactorCosine
		
		rank=1.0
		for user in pageRankDictSorted:
			scoredPageRankDict [user] = 1.0 / rank
			rank+=1
		
		for index in dictionaryOfTweets:
			scoreUser=0
			resultantScore=0
			scoreDoc=0
			twitterID = dictionaryOfTweets[index][1]
			docID =index
			if twitterID in scoredPageRankDict:
				scoreUser = scoredPageRankDict [twitterID]
			if docID in dictOfDocWithScaledScore:
				scoreDoc = dictOfDocWithScaledScore[docID]
			
			resultantScore = (0.5* scoreUser + 0.5*scoreDoc)/2.0
			if resultantScore >0.0:
				finalScoreOfDocumentAndTweeterDict[docID] = resultantScore
		
		return finalScoreOfDocumentAndTweeterDict
				
			
		
		

		  
		
		