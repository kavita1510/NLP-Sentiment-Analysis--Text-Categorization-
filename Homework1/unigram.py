
from collections import Counter
import glob
import os
import re
import string
import math

class LM:

    def __init__(self):
        self.badWords = ['.', ',', '(', ')']
        """ Vocabulary of all unigram words in the training data """
        self.Unigramdict=[0,0]
        """ Number of pos and neg files each """
        self.noFiles=1000
        """ presenceMap ={unigram :[positive file count, negative file count ]  """
        self.presenceMap={}
        """ countMap ={unigram :[total frequency in pos files, total frequency in neg files ]  """
        self.countMap={}
        """ Total count of positive and negative unigrams , totalCount= [total pos unigrams, total neg unigrams] """
        self.totalCount=[0,0]


    def makeUnigramMaps(self):

        """To make the count and the presence maps from all the text files"""

        paths = ['txt_sentoken/pos', 'txt_sentoken/neg']
        #paths = ['test/test1', 'test/test2']
        for i in range(len(paths)):
            for fileobj in glob.iglob(os.path.join(paths[i], '*.txt')):
                with open (fileobj, 'r') as f:
                    txt = f.read()
                    unigrams = set(txt.split())
                    goodUnigrams = [item for item in unigrams if item not in self.badWords]
                    for unigram in goodUnigrams:
                        if unigram not in self.presenceMap:
                            listPresence = [0,0]
                            listPresence[i] += 1
                            self.Unigramdict[i] +=1
                            self.presenceMap[unigram]=listPresence
                        else:
                            listPresence=self.presenceMap[unigram]
                            if listPresence[i] == 0:
                                self.Unigramdict[i] +=1
                            listPresence[i] += 1
                            self.presenceMap[unigram]=listPresence

                    allUnigrams=txt.split()
                    allgoodUnigrams=[item for item in allUnigrams if item not in self.badWords]
                    for unigram in allgoodUnigrams:
                            if unigram not in self.countMap:
                                listCount = [0,0]
                                listCount[i] += 1
                                self.countMap[unigram] = listCount
                            else:
                                listCount = self.countMap[unigram]
                                listCount[i] += 1
                                self.countMap[unigram] = listCount
                            self.totalCount[i] += 1

    def calculateProbs(self, mapE):
        """ To make the probability maps of both the presence and counts of the unigrams """
        probMap = {}
        if mapE == self.presenceMap:
            for word in mapE:
                probList = mapE[word]
                probMap[word] = [math.log(float(probList[0] + 1) / float(self.noFiles + self.Unigramdict[0])),math.log( float(probList[1] + 1)/float (self.noFiles + self.Unigramdict[1]))]
        if mapE == self.countMap:
            for word in mapE:
                probList = mapE[word]
                probMap[word] = [math.log(float(probList[0] + 1) / float(self.totalCount[0] + self.Unigramdict[0])),math.log( float(probList[1] + 1)/float (self.totalCount[1] + self.Unigramdict[1]))]
        return probMap


w1 = LM()
w1.makeUnigramMaps()
print "Count map", w1.countMap
print   "Count values", w1.totalCount
print "probMapPresence:", w1.calculateProbs (w1.presenceMap)
print "probMapCount:", w1.calculateProbs(w1.countMap)