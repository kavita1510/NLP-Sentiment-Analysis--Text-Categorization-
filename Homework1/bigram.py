import glob
import os
import math
from unigram import *
from string import split

class ngram:
    
    def __init__(self):
        self.file_type_list = ['txt_sentoken/pos','txt_sentoken/neg']
        
        self.ngram_unknown_dict = {}
        self.total_count = [0,0]
        self.total_count_p = [0,0]
        self.probability_dict = {}
        self.classify_result = {}
        self.ngram_dict = {}
        self.probability_dict_new = {}
        self.ngram_dict_p = {}
        
        self.badWords = ['.', ',', '(', ')', '\'']
    
    def ngram_dict_from_corpus(self, n, start, end):
        for index in range(len(self.file_type_list)):
            j  = -1
            
            for fileobj in glob.iglob(os.path.join(self.file_type_list[index], '*.txt')):  
                j +=1
                if (j>=start and j<=end):
                    continue
                with open(fileobj, 'r') as f:
                    txt = f.read()
                    """ For frequency based calculation """
                    splitted_words = txt.split()
                    #print type(splitted_words)
                    splitted_txt = [item for item in splitted_words if item not in self.badWords]
                    for i in range(len(splitted_txt)-n+1):
                        ngram_str = ' '.join(splitted_txt[i:i+n])
                        #print ngram_str
                        if ngram_str not in self.ngram_dict:
                            ngram_str_list = [0,0]
                            ngram_str_list[index] += 1
                            
                            self.ngram_dict[ngram_str] = ngram_str_list
                            
                        else:
                            self.ngram_dict[ngram_str][index] += 1 
                        self.total_count[index] += 1
                    
                    """ For presence based calculations """
                   
                    #print txt
                    splitted_words = txt.split()
                    #print splitted_words
                    splitted_txt = [item for item in splitted_words if item not in self.badWords]    
                    #print splitted_txt              
                    for i in range(len(splitted_txt)-n+1):
                        ngram_str = ' '.join(splitted_txt[i:i+n])
                        #print ngram_str
                        if ngram_str not in self.ngram_dict_p:
                            ngram_str_list = [0,0]
                            self.ngram_dict_p[ngram_str] = ngram_str_list
                            self.ngram_dict_p[ngram_str][index] += 1
                            self.total_count_p[index] += 1
                                                        
                    if self.ngram_dict_p[ngram_str][index] == 0:
                        self.total_count_p[index] +=1
                        self.ngram_dict_p[ngram_str][index] += 1 
        #print self.ngram_dict_p
        #print self.total_count_p
  
    def ngram_mark_unknown(self):
        
        for key in self.ngram_dict:
            if (self.ngram_dict[key][0] + self.ngram_dict[key][1] == 1):
                if '$$' not in self.ngram_unknown_dict:
                    self.ngram_unknown_dict['$$'] = [0,0]
                self.ngram_unknown_dict['$$'][0] += self.ngram_dict[key][0]
                self.ngram_unknown_dict['$$'][1] += self.ngram_dict[key][1]
            else:
                self.ngram_unknown_dict[key] = self.ngram_dict[key]
        #print self.ngram_unknown_dict
    
    def calculate_probability(self, uni):
        vocab = len(self.ngram_dict)
        #print "The vocab is of size", vocab;
        for key in self.ngram_dict:
            
            uni_of_key = uni[split(key)[0]]
            #print uni_of_key
            
            prob_positive = float(self.ngram_dict[key][0] + 1.0)/float(uni_of_key[0] + vocab)
            
            prob_negative = float(self.ngram_dict[key][1] + 1)/float(uni_of_key[1] + vocab)
            self.probability_dict[key] = [math.log(prob_positive), math.log(prob_negative)]
        
    def test_data_categorize(self, n, start, end):
        success_count = [0, 0]
        for index in range(len(self.file_type_list)):
            j = -1
            for fileobj in glob.iglob(os.path.join(self.file_type_list[index], '*.txt')):
                j +=1
                if (j<start or j>end):
                    continue
                pos_prob = 0
                neg_prob = 0
                with open(fileobj, 'r') as f:
                    txt = f.read()               
                    splitted_txt = txt.split()
                    for i in range(len(splitted_txt)-n+1):
                        ngram_str = ' '.join(splitted_txt[i:i+n])
                        """ Unknown ignored in bigrams"""
                        if ngram_str in self.probability_dict:
                            str_ = ngram_str;
                                                
                            pos_prob += self.probability_dict[str_][0]
                            neg_prob += self.probability_dict[str_][1]
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
        print "Positives:", success_count[0]," Percent Success:", success_count[0]*100/200.0;
        print "negatives:", success_count[1]," Percent Success:", success_count[1]*100/200.0;
        print "\n"
        


if __name__ == "__main__":
    n = 2;
    for i in range(0,5):
    # One test case
        start = i*200
        end = start + 199
        ng = ngram()
        u_obj = LM()
        u_obj.unigrams_presence()
        """ Unigrams countMap gives frequency """
        uni = u_obj.countMap
        ng.ngram_dict_from_corpus(n, start, end)
        #print ng.ngram_dict_p
        #ng.ngram_mark_unknown()
        ng.calculate_probability(uni)
        print "Text Categorization based on frequency count using bigrams"
        ng.test_data_categorize(n, start, end)
        
    #print self.probability_dict
   
