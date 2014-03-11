
from collections import Counter
import glob
import os
import re
import string

class LM:

    def __init__(self):
# import nltk
# import numpy
        self.cnt = dict()
        self.ngram_counter = dict()
        self.ngram_list = dict()

        self.specials = '-"/.,'  # etc
        self.badWords = ['and', 'the', '.', ',', 'a', 'of','is', 'to', '(', ')', 'it']




    def unigrams_presence(self):

        """To count the words from all the text files in a directory"""
        map={}
        paths = ['test/test1', 'test/test2']

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
                            map[unigram]=listPresence
                        else:
                            listPresence=map[unigram]
                            listPresence[i] += 1
                            map[unigram]=listPresence
        return map



    def calculateProbs (self, counter):
        probability = Counter()
        for word in counter:
            probability[word] = float(counter[word] / 100)
        return probability


w1 = LM()
print "map:" , w1.unigrams_presence()
