import string
import glob
import os

def test_func(n):
    bigram_dict = {}
    file_type_list = ['txt_sentoken/pos','txt_sentoken/neg']
    for index in range(len(file_type_list)):
        print index
        for fileobj in glob.iglob(os.path.join(file_type_list[index], '*.txt')):
        
            with open(fileobj, 'r') as f:
                txt = f.read()
                
                splitted_txt = txt.split()
                
                for i in range(len(splitted_txt)-n+1):
                    ngram_str = ' '.join(splitted_txt[i:i+n])
                    #print ngram_str
                    if ngram_str not in bigram_dict:
                        ngram_str_list = [0,0]
                        ngram_str_list[index] += 1
                        bigram_dict[ngram_str] = ngram_str_list
                    else:
                        bigram_dict[ngram_str][index] += 1 
    return bigram_dict            
               
        
print test_func(2)