
from collections import Counter
import glob
import os
import re
import string
import math
import random

class LM:

    def __init__(self):
        self.badWords = ['.', ',', '(', ')', '\'']
        self.Unigramdict=[0,0]
        self.noFiles=1000
        self.presenceMap={}
        self.weight_vector={}
        self.totalCount=[0,0]
        self.probability_dict_new = {}
        self.paths = ['txt_sentoken/pos', 'txt_sentoken/neg']
        self.probMap = {}
        self.f_vector = {}


    def learning_data(self, start, end):
        
        def fun(fileobj,i, expected_class):
            ##print 'in fun'
            self.f_vector = {}
            with open (fileobj, 'r') as f:
                    txt = f.read()
                    allUnigrams=txt.split()
                    allgoodUnigrams=[item for item in allUnigrams if item not in self.badWords]
                    for unigram in allgoodUnigrams:
                        if unigram not in self.weight_vector :
                            self.weight_vector[unigram] = 0
                            
                        if  unigram not in self.f_vector:
                            self.f_vector[unigram] = 1
                                                   
               
            """ Manipulating the weight vector as per positive or negative"""
            self.compute = 0
            #print self.f_vector
            #print self.weight_vector
            for key in self.f_vector:
                if key in self.weight_vector:
                    self.compute += (self.weight_vector[key] * self.f_vector[key])
            
            self.correction = expected_class - (self.compute*1.0/len(self.f_vector))
            #print self.compute
            #print self.correction
                     
            """ Mistake on positive add to the weight vector """
            """ if self.compute < 0 and i == 0: """
            for key in self.weight_vector:
                if key in self.f_vector:
                    self.weight_vector[key] += (self.f_vector[key] * self.correction)
      
        j = -1
        posfileobjs = list(glob.iglob(os.path.join(self.paths[0], '*.txt')))
        
        negfileobjs = list(glob.iglob(os.path.join(self.paths[1], '*.txt')))
        for i in range(0,1000):
            
            j +=1
            if (j>=start and j<=end):
                continue
            #print j
            self.f_vector = {}
            fun(negfileobjs[i],1, expected_class = -1)
            self.f_vector = {}
            fun(posfileobjs[i],0, expected_class = 1)
    
    
    def test_data_categorize(self,start, end):
        
        """ Categorizing data using reviews """
        success_count = [0, 0]
        
        for index in range(len(self.paths)):
            j = -1
            for fileobj in glob.iglob(os.path.join(self.paths[index], '*.txt')):
                j +=1
                if (j<start or j>end):
                    continue
                self.f_vector = {}
                with open(fileobj, 'r') as f:
                    txt = f.read()
                    allUnigrams=txt.split()
                    allgoodUnigrams=[item for item in allUnigrams if item not in self.badWords]
                    for unigram in allgoodUnigrams:
                            
                        if  unigram not in self.f_vector:
                            self.f_vector[unigram] = 1
                    
                self.compute = 0
                #print self.weight_vector
                
                for key in self.f_vector:
                    if key in self.weight_vector:
                        #print self.weight_vector[key], self.f_vector[key]
                        self.compute += (self.weight_vector[key]* self.f_vector[key])
                #print self.compute
                if self.compute > 0 and index == 0:
                        success_count[index]+=1
                elif self.compute < 0 and index == 1:
                        success_count[index]+=1
                        
    
        
        print "Test data:", start, "-", end
        print "Positives:", success_count[0]," Percent Success:", success_count[0]*100/200.0
        print "negatives:", success_count[1]," Percent Success:", success_count[1]*100/200.0
        print "Average performance:", (success_count[0]*100/200.0 + success_count[1]*100/200.0)/2.0
        print "\n"
        
    
if __name__ == "__main__":
    
    for i in range(0,5):
 
        start = i*200
        end = start + 199
        u_obj = LM()
        #print start, end
        u_obj.learning_data(start,end)
        
        #u_obj.calculateProbs(u_obj.weight_vector)
        #print "Text Categorization based on frequency count using unigrams"
        #print u_obj.weight_vector
        u_obj.test_data_categorize(start, end)
