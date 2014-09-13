import json
import re
from collections import OrderedDict
from collections import Set
from time import time,clock
class TaggedPageRank:
	
	dictOfTaggedUser={}
	invertedDict={}
	dictOfUsersInCategories={}
	dictCategories= {
				"social":["social","love","lover","college", "mars","curiosity","twitter","web","news"],
				"technology":["science","tech","technical","software","geek","computers","computer" ],
				"profession":["profession","professional","director","editor","marketing","writer","manager","freelance","ceo","producer","developer"],
				"sports":["sports","games","star","amateur"]
				}
	
	def invertDictOfCategories(self):
		for category in self.dictCategories:
			for word in self.dictCategories[category]:
				self.invertedDict[word]= category
				
		
	def intersect(self,a, b):
		return list(a & b)
	
	def getAdjacencyListForCategory(self, corpusAdjacencyList):
		start=time()
		masterDict ={}
		for userId in corpusAdjacencyList:
			adjacencyOfUser = corpusAdjacencyList[userId]
			if userId in self.dictOfTaggedUser:
				categoriesOfUser = self.dictOfTaggedUser[userId]
				for mentionedUser in adjacencyOfUser:
					if mentionedUser in self.dictOfTaggedUser:
						categoriesOfMentionedUser = self.dictOfTaggedUser[mentionedUser]
						listOfCommontags = self.intersect(categoriesOfUser,categoriesOfMentionedUser)
						for tag in listOfCommontags:
							if tag in masterDict:
								internalDict = masterDict[tag]
								if userId in  internalDict:
									masterDict[tag][userId].append(mentionedUser)
								else:
									masterDict[tag][userId] = [mentionedUser]
							else:
								masterDict[tag]={userId:[mentionedUser] }
							
		print "Master adjacency List built in ",time()-start, " seconds"
		return masterDict	
							
						
				
				
					
					
				
			
		
	
	def __init__(self):
		print "Initializing tagged page rank"
		self.invertDictOfCategories()
	
	
	def tagUsers(self,corpusFile):
		lines = [line.strip() for line in open(corpusFile)] 
		for line  in lines:
			data = json.loads(line)
			user = data["user"]
			userId = user['id']
			if "description" in user:
				listOfWords = re.findall(r"[\w]+", user['description'].lower())
#				loweredList =[x.lower() for x in  listOfWords]
				for word in listOfWords:
					if word in self.invertedDict:
						if userId in self.dictOfTaggedUser:
							self.dictOfTaggedUser[userId].add(self.invertedDict[word])
						else:
							word =self.invertedDict[word]
							self.dictOfTaggedUser[userId] = set([word])
		
		
#		print self.dictOfTaggedUser
					
							
		
	
	
	
	def taggedPageRankUsers(self,corpusFile,corpusAdjacencyList):
#		listOfFrequentWords = self.getListOfMostFrequentWords(corpusFile,corpusAdjacencyList)
		self.tagUsers(corpusFile)
		masterDict = self.getAdjacencyListForCategory(corpusAdjacencyList)
		return masterDict
		
	
	
	
	def getuserScreenNameIndexedDict(self,corpusFile):
		userScreenNameDict={}
		lines = [line.strip() for line in open(corpusFile)] 
		for line  in lines:
			data = json.loads(line)
			screenName= (data["user"]["screen_name"])
			if screenName not in userScreenNameDict:
				userScreenNameDict[screenName] = data["user"]["id"]
		
		return 		userScreenNameDict
			
			
	def printTopFiftyFromDictionary(self,dictObj):
		index =1;
		for key in dictObj:
			print "Key: ",key
			print "Value :",dictObj[key]
			index+=1
			if index >=51:
				break
			 	
	
	def getListOfMostFrequentWordsAndUserDescriptionDict(self,corpusFile):
		termCountDict={}
		userDecriptionDict={}
		userScreenNameDict = self.getuserScreenNameIndexedDict(corpusFile)
		lines = [line.strip() for line in open(corpusFile)] 
		for line in lines:
			data = json.loads(line)
			screenName= (data["user"]["screen_name"])
			user =data['user']
			if 'description' in user:
				
				listOfWords = re.findall(r'[A-Z].\w+', user['description'])
			
				for word in listOfWords:
					if word not in userScreenNameDict:
						if word in termCountDict:
							termCountDict[word]+=1
						else :
							termCountDict[word]=1
						
				
		
		sortedDict = OrderedDict(sorted(termCountDict.items(), key=lambda t: t[1], reverse =True))
		self.printTopFiftyFromDictionary(sortedDict)
		
		
		
