
from collections import Counter
import glob
import os
import re
import string
import math

class LM:

    def __init__(self):
# import nltk
# import numpy
   

        self.specials = '-"/.,'  # etc
        self.badWords = ['and', 'the', '.', ',', 'a', 'of','is', 'to', '(', ')', 'it']
        self.totalCount=[0,0]
        self.noFiles=2



    def unigrams_presence(self):

        """To count the words from all the text files in a directory"""
        map={}

        paths = ['txt_sentoken/pos', 'txt_sentoken/neg']

        for i in range(len(paths)):
            for fileobj in glob.iglob(os.path.join(paths[i], '*.txt')):
                with open (fileobj, 'r') as f:
                    txt = f.read()
                    unigrams = set(txt.split())
                    goodUnigrams = [item for item in unigrams if item not in self.badWords]
                    for unigram in goodUnigrams:
                        if unigram not in map:
                            listPresence = [0,0]
                            listPresence[i] += 1
                            self.totalCount[i] +=1
                            map[unigram]=listPresence
                        else:
                            listPresence=map[unigram]
                            if listPresence[i] == 0:
                                self.totalCount[i] +=1
                            listPresence[i] += 1
                            map[unigram]=listPresence
        return map



    def calculateProbs (self, map):
        probMap = {}
        print self.totalCount
        for word in map:
            probList = map[word]
            probMap[word] = [math.log(float(probList[0] + 1) / float(self.noFiles + self.totalCount[0])),math.log( float(probList[1] + 1)/float (self.noFiles + self.totalCount[1]))]
        return probMap


w1 = LM()
presenceMap=w1.unigrams_presence()
print "Presence map", presenceMap
print "count", w1.totalCount
print "probMap:", w1.calculateProbs (presenceMap)
