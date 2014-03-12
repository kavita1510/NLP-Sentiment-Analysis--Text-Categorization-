import glob
import os
import math

class ngram:
    
    def __init__(self):
        self.file_type_list = ['txt_sentoken/pos','txt_sentoken/neg']
        
        self.ngram_unknown_dict = {}
        self.total_count = [0,0]
        self.probability_dict = {}
        self.classify_result = {}
        self.ngram_dict = {}
        self.probability_dict_new = {}
    
    def ngram_dict_from_corpus(self, n, start, end):
        for index in range(len(self.file_type_list)):
            j  = -1
            
            for fileobj in glob.iglob(os.path.join(self.file_type_list[index], '*.txt')):  
                j +=1
                if (j>=start and j<=end):
                    continue
                with open(fileobj, 'r') as f:
                    txt = f.read()
                    splitted_txt = txt.split()
                    
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
        #return self.ngram_dict  
        #print j          
    
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
    
    
    def calculate_probability(self):
        vocab = len(self.ngram_unknown_dict)
        #print "The vocab is of size", vocab;
        for key in self.ngram_unknown_dict:
            prob_positive = float(self.ngram_unknown_dict[key][0] + 1.0)/float(self.total_count[0] + vocab)
            
            prob_negative = float(self.ngram_unknown_dict[key][1] + 1)/float(self.total_count[1] + vocab)
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
                        if ngram_str in self.probability_dict:
                            str_ = ngram_str;
                        else:
                            str_ = '$$'
                        
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
        print success_count


if __name__ == "__main__":
    n = 2;
    for i in range(0,5):
    # One test case
        start = i*200
        end = start + 199
        ng = ngram()
        ng.ngram_dict_from_corpus(n, start, end)
        ng.ngram_mark_unknown()
        ng.calculate_probability()
        ng.test_data_categorize(n, start, end)
    #print self.probability_dict
   
