from collections import Counter
import glob
import os
import math

class LM:

    def __init__(self):
        self.badWords = ['.', ',', '(', ')', '\'']
        self.Unigramdict=[0,0]
        self.noFiles=1000
        self.presenceMap={}
        self.countMap={}
        self.totalCount=[0,0]
        self.probability_dict_new = {}
        self.paths = ['txt_sentoken/pos', 'txt_sentoken/neg']
        self.probMap = {}


    def unigrams_presence(self, start, end):

        """To count the words from all the text files in a directory"""

        #paths = ['test/test1', 'test/test2']
        for i in range(len(self.paths)):
            j = -1
            for fileobj in glob.iglob(os.path.join(self.paths[i], '*.txt')):
                j +=1
                if (j>=start and j<=end):
                    continue
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

        """ Computing probabilities of unigrams """

        if mapE == self.presenceMap:
            for word in mapE:
                probList = mapE[word]
                self.probMap[word] = [math.log(float(probList[0] + 1) / float(self.noFiles + self.Unigramdict[0])),math.log( float(probList[1] + 1)/float (self.noFiles + self.Unigramdict[1]))]
        if mapE == self.countMap:
            for word in mapE:
                probList = mapE[word]
                self.probMap[word] = [math.log(float(probList[0] + 1) / float(self.totalCount[0] + self.Unigramdict[0])),math.log( float(probList[1] + 1)/float (self.totalCount[1] + self.Unigramdict[1]))]


    def test_data_categorize(self,start, end):

        """ Categorizing data using reviews """
        success_count = [0, 0]
        for index in range(len(self.paths)):
            j = -1
            for fileobj in glob.iglob(os.path.join(self.paths[index], '*.txt')):
                j +=1
                if (j<start or j>end):
                    continue
                pos_prob = 0
                neg_prob = 0
                with open(fileobj, 'r') as f:
                    txt = f.read()
                    allUnigrams=txt.split()
                    allgoodUnigrams=[item for item in allUnigrams if item not in self.badWords]
                    for unigram in allgoodUnigrams:
                            if unigram in self.probMap:
                                pos_prob += self.probMap[unigram][0]
                                neg_prob += self.probMap[unigram][1]
                        #print pos_prob, neg_prob
                #print pos_prob, neg_prob
                if pos_prob > neg_prob:
                    if index == 0:
                        success_count[index]+=1
                else:
                    if index == 1:
                        success_count[index]+=1

                self.probability_dict_new[fileobj]= [pos_prob,neg_prob]


        print "Test data:", start, "-", end
        print "Positives:", success_count[0]," Percent Success:", success_count[0]*100/200.0
        print "negatives:", success_count[1]," Percent Success:", success_count[1]*100/200.0
        print "Average performance:", (success_count[0]*100/200.0 + success_count[1]*100/200.0)/2.0
        print "\n"


if __name__ == "__main__":

    print "Text Categorization based on frequency count using unigrams"
    for i in range(0,5):
        start = i*200
        end = start + 199
        u_obj = LM()
        u_obj.unigrams_presence(start, end)
        u_obj.calculateProbs(u_obj.countMap)
        u_obj.test_data_categorize(start, end)

    print "Text Categorization based on presence using unigrams"
    for i in range(0,5):
        start = i*200
        end = start + 199
        u_obj = LM()
        u_obj.unigrams_presence(start, end)
        u_obj.calculateProbs(u_obj.presenceMap)
        u_obj.test_data_categorize(start, end)