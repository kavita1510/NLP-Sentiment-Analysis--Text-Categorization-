#from liblinearutil import *
import glob
import os


class LM:

    def __init__(self):
        self.badWords = ['.', ',', '(', ')']
        """ Count of all unique +ve and -ve unigram words in the training data """
        self.UnigramVocab=[0,0]
        """ Number of pos and neg files each """
        self.noFiles=1000
        """ presenceMap ={unigram :[positive file count, negative file count ]  """
        self.presenceMap={}
        """ countMap ={unigram :[total frequency in pos files, total frequency in neg files ]  """
        self.countMap={}
        """ Total count of positive and negative unigrams , totalCount= [total pos unigrams, total neg unigrams] """
        self.totalCount=[0,0]
        """ Array list of all the files """
        self.fileArray=[]
        """Positive and negative file paths """
        self.paths = ['txt_sentoken/pos', 'txt_sentoken/neg']
        """ A unigram dict containg all unigrams with their IDS"""
        self.unigramDict = {}

    def makeUnigramMaps(self):
        """To make the count and the presence maps from all the text files"""
        #self.paths = ['test/test1', 'test/test2']
        for i in range(len(self.paths)):
            for fileobj in glob.iglob(os.path.join(self.paths[i], '*.txt')):
                with open (fileobj, 'r') as f:
                    txt = f.read()
                    unigrams = set(txt.split())
                    goodUnigrams = [item for item in unigrams if item not in self.badWords]
                    for unigram in goodUnigrams:
                        if unigram not in self.presenceMap:
                            listPresence = [0,0]
                            listPresence[i] += 1
                            self.UnigramVocab[i] +=1
                            self.presenceMap[unigram]=listPresence
                        else:
                            listPresence=self.presenceMap[unigram]
                            if listPresence[i] == 0:
                                self.UnigramVocab[i] +=1
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

    def makeSVMdata(self):
        ID=0
        f= open('SVMdata.txt', 'a')
        f.truncate()
        for i in range(len(self.paths)):
            for fileobj in glob.iglob(os.path.join(self.paths[i], '*.txt')):
                with open (fileobj, 'r') as f:
                    fileDict={}
                    txt = f.read()
                    unigrams = set(txt.split())
                    goodUnigrams = [item for item in unigrams if item not in self.badWords]
                    for unigram in goodUnigrams:
                        if unigram not in self.unigramDict:
                            self.unigramDict[unigram]=ID
                            ID +=1
                        fileDict[self.unigramDict[unigram]]=1
                    self.fileArray.append(fileDict)
                    with open('SVMdata.txt', 'a') as f1:
                        if i == 0:
                            f1.write("+1 ")
                        else:
                            f1.write("-1 ")
                        for wordId, p in fileDict.items():
                            f1.write(str(wordId)+ ":1 ")
                        f1.write('\n')

w1=LM()
w1.makeUnigramMaps()
print "Print unigram dictionary:", w1.UnigramVocab
w1.makeSVMdata()
print "Unigram dictionary:", w1.unigramDict
# for item in w1.fileArray:
#     print "->", item
print "size unigramdict", len(w1.unigramDict)

