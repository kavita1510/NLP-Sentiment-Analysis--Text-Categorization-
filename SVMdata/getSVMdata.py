#from liblinearutil import *
import glob
import os
import re
import string
from svmutil import *


class LM:

    def __init__(self):
        self.badWords = ['.', ',', '(', ')','!', '\\','-', '?','+']
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

        self.unigramCountDict={}
        self.fileDictCount={}
        self.fileCountArray=[]



    def makeSVMdata(self,start, end, istraining):
        ID=1
        print "start",start
        print "end", end
        fileName = 'SVMTraindata04.txt'
        fileNameCount = 'SVMTraindataC04.txt'
        if(not istraining):
            fileName = 'SVMTestdata04.txt'
            fileNameCount = 'SVMTestdataC04.txt'


        for i in range(len(self.paths)):
            j = -1

            for fileobj in glob.iglob(os.path.join(self.paths[i], '*.txt')):
                j += 1
                if(not istraining and (j < start or j >  end)):
                    continue;
                elif(istraining and (j >= start and j <=  end)):
                    continue;
                with open (fileobj, 'r') as f:
                    fileDict={}
                    fileCountDict={}
                    txt = f.read()
                    txt.lower()
                    txt = re.sub('[^a-zA-Z0-9\s]',"", txt)

                    """ Make libSVM format files using unigram presence """
                    unigrams = set(txt.split())
                    #goodUnigrams = [item for item in unigrams if item not in self.badWords]
                    goodUnigrams= unigrams

                    for unigram in goodUnigrams:
                        if unigram not in self.unigramDict:
                            if (not istraining):
                                continue;
                            self.unigramDict[unigram]=ID
                            ID +=1
                        fileDict[self.unigramDict[unigram]]=1
                    #self.fileArray.append(fileDict)
                    outfile= open(fileName, 'a')
                    #with outfile:
                    if i == 0:
                        outfile.write("+1 ")
                    else:
                        outfile.write("-1 ")
                    for wordId in sorted(fileDict.iterkeys()):
                        outfile.write(str(wordId)+ ":" + str(fileDict[wordId])+ " ")
                    outfile.write('\n')

                    """ Make libSVM format files using unigram count """
                    allUnigrams=txt.split()
                    #allgoodUnigrams=[item for item in allUnigrams if item not in self.badWords]
                    allgoodUnigrams=allUnigrams
                    for unigram in allgoodUnigrams:
                        if unigram not in self.unigramDict:
                            continue;
                        if self.unigramDict[unigram] not in fileCountDict.keys():
                            fileCountDict[self.unigramDict[unigram]] = 1
                        else:
                            fileCountDict[self.unigramDict[unigram]] += 1
                    #self.fileCountArray.append(fileCountDict)
                    outfile= open(fileNameCount, 'a')
                    #with outfile:
                    if i == 0:
                        outfile.write("+1 ")
                    else:
                        outfile.write("-1 ")
                    for wordId in sorted(fileCountDict.iterkeys()):
                        outfile.write(str(wordId)+ ":" + str(fileCountDict[wordId])+ " ")
                    outfile.write('\n')


w1=LM()
# w1.makeSVMdata(200,399, True)
# w1.makeSVMdata(200,399, False)

w1.makeSVMdata(800,999, True)
w1.makeSVMdata(800,999, False)

# Read data in LIBSVM format

