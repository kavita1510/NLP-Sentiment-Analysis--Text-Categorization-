import string
import glob
import os

file_type_list = ['txt_sentoken/pos','txt_sentoken/neg']
bigram_unknown_dict = {}
def bigram_dict_from_corpus(n):
    bigram_dict = {}
    
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

def bigram_mark_unknown():
    bigram = bigram_dict_from_corpus(2)
    
    for key in bigram:
        if (bigram[key][0] + bigram[key][1] == 1):
            if '$$' not in bigram_unknown_dict:
                bigram_unknown_dict['$$'] = [0,0]
                bigram_unknown_dict['$$'][0] = bigram[key][0]
                bigram_unknown_dict['$$'][1] = bigram[key][1]
            else:
                bigram_unknown_dict['$$'][0] += bigram[key][0]
                bigram_unknown_dict['$$'][1] += bigram[key][1]
        else:
            bigram_unknown_dict[key] = bigram[key]
    print bigram_unknown_dict
bigram_mark_unknown()


