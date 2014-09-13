from math import log
from time import time,clock
from datetime import datetime
from pprint import pprint
#from scipy import sparse as sp, sparse
from sets import Set
import collections
from collections import OrderedDict
import json
import math
import re
#from scipy.sparse.coo import coo_matrix
#from Crypto.SelfTest import SelfTestError


class PageRank:
	
	
	transportationValue=0
	transportationValueForDanglingNodes=0
	dampingFactor=0.9
	
	
	def __init__(self):
		print "Initializing PageRank"
	
	
	def getUserDictionaryAndAllUsersFromTweets(self,corpusFile):
		userReferenceDictionary={}
		userIdNameDict={}
		lines = [line.strip() for line in open(corpusFile)]
		for line in lines:
			data = json.loads(line)
			screenName= (data["user"]["screen_name"])
			screenName = screenName.lower()
			currentUserID= (data["user"]["id"])
			userIdNameDict[currentUserID] = screenName
			userMentionsDictOfCurrentUser = data["entities"]["user_mentions"]
			if len(userMentionsDictOfCurrentUser)>0:
				for i in range(len(userMentionsDictOfCurrentUser)):
					mentionedUser= data["entities"]["user_mentions"][i]["screen_name"]
					mentionedUser = mentionedUser.lower()
					mentionedUserId= data["entities"]["user_mentions"][i]["id"]
					
					if (mentionedUserId)!=currentUserID:
						if currentUserID in userReferenceDictionary:
							userReferenceDictionary[currentUserID].add(mentionedUserId)
						else:
							userReferenceDictionary[currentUserID]=set([mentionedUserId])
						if mentionedUserId not in userReferenceDictionary:
							userReferenceDictionary[mentionedUserId]=set([])
							
		
		return (userReferenceDictionary,userIdNameDict)
	
	def getPageRankByModifiedAlgo(self,adjacencyListDict):
		
		previousPageRankDict ={}
		currentPageRankDict ={}
		lenUserDict =float(len(adjacencyListDict))
		print "Number of Users ",lenUserDict
		for user in adjacencyListDict:
			previousPageRankDict[user]=1.0
			currentPageRankDict[user]=0.0
		
		
		for i in range(10000):	
#			print "Iteration i",i
			for user in adjacencyListDict:
				outGoingList = adjacencyListDict[user]
				for mentionedUser in outGoingList:
					if mentionedUser in currentPageRankDict:
						currentPageRankDict[mentionedUser] +=  (0.9) *( float(previousPageRankDict[user]) /   len(outGoingList))
						
#			print "first for loop in ",time()- start," secs"
			for user in  currentPageRankDict:
				pageRank = currentPageRankDict[user]
				if len(adjacencyListDict[user])==0:
					currentPageRankDict[user]+= ((1.0)/lenUserDict)
				else:
					currentPageRankDict[user]+=0.1 * ((1.0)/lenUserDict)
			
		
			convergedNum =0
			for user in adjacencyListDict :
				if   abs(currentPageRankDict[user] - previousPageRankDict[user]) <0.0000001:
					convergedNum+=1
			if convergedNum == lenUserDict:
				break
					
			previousPageRankDict = currentPageRankDict.copy()
			for user in currentPageRankDict:
				currentPageRankDict[user]=0.0
			 		
#			print previousPageRankDict
		return  previousPageRankDict
	
	
	def constructPageRanks(self,corpusFile):
		tupleOfDictionaries = self.getUserDictionaryAndAllUsersFromTweets(corpusFile)
		userDictionaryMentions = tupleOfDictionaries[0]
		userIdNameDict = tupleOfDictionaries[1]
		steadyDict = self.getPageRankByModifiedAlgo(userDictionaryMentions)
		return (steadyDict,userIdNameDict,userDictionaryMentions)
		
		
	def constructPageRankFromAdjacencyList(self,adjacencyList):
		steadyDict = self.getPageRankByModifiedAlgo(adjacencyList)
		return steadyDict
			
			
		
			
		
		
		'''
#		print transitionMatrix.todense()
		colSizeOfMatrix= transitionMatrix.get_shape()[1]
		equalProb =1.0/colSizeOfMatrix
		row= colSizeOfMatrix*[0]
		col = range(colSizeOfMatrix)
		data = colSizeOfMatrix*[equalProb]
		initialStateMatrix= coo_matrix( (data,(row,col)) , shape= (1, colSizeOfMatrix)  )
		lilInitialState= initialStateMatrix.tolil()
#		print lilInitialState.todense()
		
		rowTeleportationMatrix =range(colSizeOfMatrix)
		colTeleportationmatrix=colSizeOfMatrix *[0]
		dataTeleportationMatrix = colSizeOfMatrix *[self.transportationValue]
		teleportationMatrix =  coo_matrix( (dataTeleportationMatrix,(rowTeleportationMatrix,colTeleportationmatrix)) , shape= ( colSizeOfMatrix,1)  )
		
		print 'for testing '
#		self.getDataWithDenseCalculations(transitionMatrix,equalProb,curStateMatrix)
		
		
		print "real"
		previousStateMatrix= lilInitialState
		lilOfCurrentState =previousStateMatrix.copy()
		for i in range(10):
			print "Iteration ",i," starting at ",datetime.now()
			for index in range(colSizeOfMatrix):
				print "calculate for index ",index
				columnTemp = transitionMatrix.getcol(index)
				teleportationSummed = columnTemp +teleportationMatrix
				tempMatrix= previousStateMatrix * teleportationSummed
#				print tempMatrix.todense()
				lilOfCurrentState[0,index] =tempMatrix[0,0]
			print "Iteration ",i," ending at ",datetime.now()
#			print lilOfCurrentState.todense()
			previousStateMatrix = lilOfCurrentState.copy()
			'''	
			
			
		
		
	
	
		